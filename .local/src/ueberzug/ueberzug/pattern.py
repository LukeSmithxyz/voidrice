class LazyConstant:
    def __init__(self, function):
        self.value = None
        self.function = function

    def __get__(self, instance, owner):
        if self.value is None:
            self.value = self.function()
        return self.value

    def __set__(self, instance, value):
        raise AttributeError("can't set attribute")
