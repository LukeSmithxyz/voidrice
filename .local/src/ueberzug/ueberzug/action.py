import abc
import enum
import os.path

import attr

import ueberzug.geometry as geometry
import ueberzug.scaling as scaling
import ueberzug.conversion as conversion


@attr.s
class Action(metaclass=abc.ABCMeta):
    """Describes the structure used to define actions classes.

    Defines a general interface used to implement the building of commands
    and their execution.
    """
    action = attr.ib(type=str, default=attr.Factory(
        lambda self: self.get_action_name(), takes_self=True))

    @staticmethod
    @abc.abstractmethod
    def get_action_name():
        """Returns the constant name which is associated to this action."""
        raise NotImplementedError()

    @abc.abstractmethod
    async def apply(self, windows, view, tools):
        """Executes the action on  the passed view and windows."""
        raise NotImplementedError()


@attr.s(kw_only=True)
class Drawable:
    """Defines the attributes of drawable actions."""
    draw = attr.ib(default=True, converter=conversion.to_bool)
    synchronously_draw = attr.ib(default=False, converter=conversion.to_bool)


@attr.s(kw_only=True)
class Identifiable:
    """Defines the attributes of actions
    which are associated to an identifier.
    """
    identifier = attr.ib(type=str)


@attr.s(kw_only=True)
class DrawAction(Action, Drawable, metaclass=abc.ABCMeta):
    """Defines actions which redraws all windows."""
    # pylint: disable=abstract-method
    __redraw_scheduled = False

    @staticmethod
    def schedule_redraw(windows):
        """Creates a async function which redraws every window
        if there is no unexecuted function
        (returned by this function)
        which does the same.

        Args:
            windows (batch.BatchList of ui.OverlayWindow):
                the windows to be redrawn

        Returns:
            function: the redraw function or None
        """
        if not DrawAction.__redraw_scheduled:
            DrawAction.__redraw_scheduled = True

            async def redraw():
                windows.draw()
                DrawAction.__redraw_scheduled = False
            return redraw()
        return None

    async def apply(self, windows, view, tools):
        if self.draw:
            import asyncio
            if self.synchronously_draw:
                windows.draw()
                # force coroutine switch
                await asyncio.sleep(0)
                return

            function = self.schedule_redraw(windows)
            if function:
                asyncio.ensure_future(function)


@attr.s(kw_only=True)
class ImageAction(DrawAction, Identifiable, metaclass=abc.ABCMeta):
    """Defines actions which are related to images."""
    # pylint: disable=abstract-method
    pass


@attr.s(kw_only=True)
class AddImageAction(ImageAction):
    """Displays the image according to the passed option.
    If there's already an image with the given identifier
    it's going to be replaced.
    """

    x = attr.ib(type=int, converter=int)
    y = attr.ib(type=int, converter=int)
    path = attr.ib(type=str)
    width = attr.ib(type=int, converter=int, default=0)
    height = attr.ib(type=int, converter=int, default=0)
    scaling_position_x = attr.ib(type=float, converter=float, default=0)
    scaling_position_y = attr.ib(type=float, converter=float, default=0)
    scaler = attr.ib(
        type=str, default=scaling.ContainImageScaler.get_scaler_name())
    # deprecated
    max_width = attr.ib(type=int, converter=int, default=0)
    max_height = attr.ib(type=int, converter=int, default=0)

    @staticmethod
    def get_action_name():
        return 'add'

    def __attrs_post_init__(self):
        self.width = self.max_width or self.width
        self.height = self.max_height or self.height
        # attrs doesn't support overriding the init method
        # pylint: disable=attribute-defined-outside-init
        self.__scaler_class = None
        self.__last_modified = None

    @property
    def scaler_class(self):
        """scaling.ImageScaler: the used scaler class of this placement"""
        if self.__scaler_class is None:
            self.__scaler_class = \
                scaling.ScalerOption(self.scaler).scaler_class
        return self.__scaler_class

    @property
    def last_modified(self):
        """float: the last modified time of the image"""
        if self.__last_modified is None:
            self.__last_modified = os.path.getmtime(self.path)
        return self.__last_modified

    def is_same_image(self, old_placement):
        """Determines whether the placement contains the same image
        after applying the changes of this command.

        Args:
            old_placement (ui.OverlayWindow.Placement):
                the old data of the placement

        Returns:
            bool: True if it's the same file
        """
        return old_placement and not (
            old_placement.last_modified < self.last_modified
            or self.path != old_placement.path)

    def is_full_reload_required(self, old_placement,
                                screen_columns, screen_rows):
        """Determines whether it's required to fully reload
        the image of the placement to properly render the placement.

        Args:
            old_placement (ui.OverlayWindow.Placement):
                the old data of the placement
            screen_columns (float):
                the maximum amount of columns the screen can display
            screen_rows (float):
                the maximum amount of rows the screen can display

        Returns:
            bool: True if the image should be reloaded
        """
        return old_placement and (
            (not self.scaler_class.is_indulgent_resizing()
             and old_placement.scaler.is_indulgent_resizing())
            or (old_placement.width <= screen_columns < self.width)
            or (old_placement.height <= screen_rows < self.height))

    def is_partly_reload_required(self, old_placement,
                                  screen_columns, screen_rows):
        """Determines whether it's required to partly reload
        the image of the placement to render the placement more quickly.

        Args:
            old_placement (ui.OverlayWindow.Placement):
                the old data of the placement
            screen_columns (float):
                the maximum amount of columns the screen can display
            screen_rows (float):
                the maximum amount of rows the screen can display

        Returns:
            bool: True if the image should be reloaded
        """
        return old_placement and (
            (self.scaler_class.is_indulgent_resizing()
             and not old_placement.scaler.is_indulgent_resizing())
            or (self.width <= screen_columns < old_placement.width)
            or (self.height <= screen_rows < old_placement.height))

    async def apply(self, windows, view, tools):
        try:
            import ueberzug.ui as ui
            import ueberzug.loading as loading
            old_placement = view.media.pop(self.identifier, None)
            cache = old_placement and old_placement.cache
            image = old_placement and old_placement.image

            max_font_width = max(map(
                lambda i: i or 0, windows.parent_info.font_width or [0]))
            max_font_height = max(map(
                lambda i: i or 0, windows.parent_info.font_height or [0]))
            font_size_available = max_font_width and max_font_height
            screen_columns = (font_size_available and
                              view.screen_width / max_font_width)
            screen_rows = (font_size_available and
                           view.screen_height / max_font_height)

            # By default images are only stored up to a resolution which
            # is about as big as the screen resolution.
            # (loading.CoverPostLoadImageProcessor)
            # The principle of spatial locality does not apply to
            # resize operations of images with big resolutions
            # which is why those operations should be applied
            # to a resized version of those images.
            # Sometimes we still need all pixels e.g.
            # if the image scaler crop is used.
            # So sometimes it's required to fully load them
            # and sometimes it's not required anymore which is
            # why they should be partly reloaded
            # (to speed up the resize operations again).
            if (not self.is_same_image(old_placement)
                    or (font_size_available and self.is_full_reload_required(
                        old_placement, screen_columns, screen_rows))
                    or (font_size_available and self.is_partly_reload_required(
                        old_placement, screen_columns, screen_rows))):
                upper_bound_size = None
                image_post_load_processor = None
                if (self.scaler_class != scaling.CropImageScaler and
                        font_size_available):
                    upper_bound_size = (
                        max_font_width * self.width,
                        max_font_height * self.height)
                if (self.scaler_class != scaling.CropImageScaler
                        and font_size_available
                        and self.width <= screen_columns
                        and self.height <= screen_rows):
                    image_post_load_processor = \
                        loading.CoverPostLoadImageProcessor(
                            view.screen_width, view.screen_height)
                image = tools.loader.load(
                    self.path, upper_bound_size, image_post_load_processor)
                cache = None

            view.media[self.identifier] = ui.OverlayWindow.Placement(
                self.x, self.y, self.width, self.height,
                geometry.Point(self.scaling_position_x,
                               self.scaling_position_y),
                self.scaler_class(),
                self.path, image, self.last_modified, cache)
        finally:
            await super().apply(windows, view, tools)


@attr.s(kw_only=True)
class RemoveImageAction(ImageAction):
    """Removes the image with the passed identifier."""

    @staticmethod
    def get_action_name():
        return 'remove'

    async def apply(self, windows, view, tools):
        try:
            if self.identifier in view.media:
                del view.media[self.identifier]
        finally:
            await super().apply(windows, view, tools)


@enum.unique
class Command(str, enum.Enum):
    ADD = AddImageAction
    REMOVE = RemoveImageAction

    def __new__(cls, action_class):
        inst = str.__new__(cls)
        inst._value_ = action_class.get_action_name()
        inst.action_class = action_class
        return inst
