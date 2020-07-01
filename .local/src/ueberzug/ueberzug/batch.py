"""This module defines util classes
which allow to execute operations
for each element of a list of objects of the same class.
"""
import abc
import collections.abc


class SubclassingMeta(abc.ABCMeta):
    """Metaclass which creates a subclass for each instance.

    As decorators only work
    if the class object contains the declarations,
    we need to create a subclass for each different type
    if we want to dynamically use them.
    """
    SUBCLASS_IDENTIFIER = '__subclassed__'

    def __call__(cls, *args, **kwargs):
        if hasattr(cls, SubclassingMeta.SUBCLASS_IDENTIFIER):
            return super().__call__(*args, **kwargs)

        subclass = type(cls.__name__, (cls,), {
            SubclassingMeta.SUBCLASS_IDENTIFIER:
            SubclassingMeta.SUBCLASS_IDENTIFIER})
        return subclass(*args, **kwargs)


class BatchList(collections.abc.MutableSequence, metaclass=SubclassingMeta):
    """BatchList provides the execution of methods and field access
    for each element of a list of instances of the same class
    in a similar way to one of these instances it would.
    """
    __attributes_declared = False

    class BatchMember:
        def __init__(self, outer, name):
            """
            Args:
                outer (BatchList): Outer class instance
            """
            self.outer = outer
            self.name = name

    class BatchField(BatchMember):
        def __get__(self, owner_instance, owner_class):
            return BatchList([instance.__getattribute__(self.name)
                              for instance in self.outer])

        def __set__(self, owner_instance, value):
            for instance in self.outer:
                instance.__setattr__(self.name, value)

        def __delete__(self, instance):
            for instance in self.outer:
                instance.__delattr__(self.name)

    class BatchMethod(BatchMember):
        def __call__(self, *args, **kwargs):
            return BatchList(
                [instance.__getattribute__(self.name)(*args, **kwargs)
                 for instance in self.outer])

    def __init__(self, collection: list):
        """
        Args:
            collection (List): List of target instances
        """
        self.__collection = collection.copy()
        self.__initialized = False
        self.__type = None
        self.entered = False
        self.__attributes_declared = True
        self.__init_members__()

    def __call__(self, *args, **kwargs):
        if self.__initialized:
            raise TypeError("'%s' object is not callable" % self.__type)
        return BatchList([])

    def __getattr__(self, name):
        if self.__initialized:
            return AttributeError("'%s' object has no attribute '%s'"
                                  % (self.__type, name))
        return BatchList([])

    def __setattr__(self, name, value):
        if (not self.__attributes_declared or
                self.__initialized or
                not isinstance(getattr(self, name), BatchList)):
            super().__setattr__(name, value)

    def __init_members__(self):
        if self.__collection and not self.__initialized:
            # Note: We can't simply use the class,
            #       as the attributes exists only after the instantiation
            self.__initialized = True
            instance = self.__collection[0]
            self.__type = type(instance)
            self.__init_attributes__(instance)
            self.__init_methods__(instance)

    def __declare_decorator__(self, name, decorator):
        setattr(type(self), name, decorator)

    def __init_attributes__(self, target_instance):
        attributes = (vars(target_instance)
                      if hasattr(target_instance, '__dict__')
                      else [])

        for name in filter(lambda name: not name.startswith('_'),
                           attributes):
            self.__declare_decorator__(name, BatchList.BatchField(self, name))

    def __init_methods__(self, target_instance):
        for name, value in filter(lambda i: not i[0].startswith('_'),
                                  vars(type(target_instance)).items()):
            if callable(value):
                self.__declare_decorator__(
                    name, BatchList.BatchMethod(self, name))
            else:
                # should be an decorator
                self.__declare_decorator__(
                    name, BatchList.BatchField(self, name))

    def __enter__(self):
        self.entered = True
        return BatchList([instance.__enter__() for instance in self])

    def __exit__(self, *args):
        for instance in self:
            instance.__exit__(*args)

    def __iadd__(self, other):
        if self.entered:
            for i in other:
                i.__enter__()
        self.__collection.__iadd__(other)
        self.__init_members__()
        return self

    def append(self, item):
        if self.entered:
            item.__enter__()
        self.__collection.append(item)
        self.__init_members__()

    def insert(self, index, item):
        if self.entered:
            item.__enter__()
        self.__collection.insert(index, item)
        self.__init_members__()

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def __add__(self, other):
        return BatchList(self.__collection.__add__(other))

    def reverse(self):
        self.__collection.reverse()

    def clear(self):
        if self.entered:
            for i in self.__collection:
                i.__exit__(None, None, None)
        self.__collection.clear()

    def copy(self):
        return BatchList(self.__collection.copy())

    def pop(self, *args):
        result = self.__collection.pop(*args)

        if self.entered:
            result.__exit__(None, None, None)

        return result

    def remove(self, value):
        if self.entered:
            value.__exit__(None, None, None)
        return self.__collection.remove(value)

    def __isub__(self, other):
        for i in other:
            self.remove(i)
        return self

    def __sub__(self, other):
        copied = self.copy()
        copied -= other
        return copied

    def __len__(self):
        return len(self.__collection)

    def __delitem__(self, key):
        return self.pop(key)

    def __setitem__(self, key, value):
        self.pop(key)
        self.insert(key, value)

    def __getitem__(self, key):
        return self.__collection[key]

    def count(self, *args, **kwargs):
        return self.__collection.count(*args, **kwargs)

    def index(self, *args, **kwargs):
        return self.__collection.index(*args, **kwargs)

    def __iter__(self):
        return iter(self.__collection)

    def __contains__(self, item):
        return item in self.__collection

    def __reversed__(self):
        return reversed(self.__collection)


if __name__ == '__main__':
    class FooBar:
        def __init__(self, a, b, c):
            self.mhm = a
            self.b = b
            self.c = c

        def ok(self):
            return self.b

        @property
        def prop(self):
            return self.c

    # print attributes
    # print(vars(FooBar()))
    # print properties and methods
    # print(vars(FooBar).keys())
    blist = BatchList([FooBar('foo', 'bar', 'yay')])
    blist += [FooBar('foobar', 'barfoo', 'yay foobar')]
    print('mhm', blist.mhm)
    print('prop', blist.prop)
    # print('ok', blist.ok)
    print('ok call', blist.ok())
