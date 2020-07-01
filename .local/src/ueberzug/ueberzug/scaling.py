"""Modul which implements class and functions
all about scaling images.
"""
import abc
import enum

import ueberzug.geometry as geometry


class ImageScaler(metaclass=abc.ABCMeta):
    """Describes the structure used to define image scaler classes.

    Defines a general interface used to implement different ways
    of scaling images to specific sizes.
    """

    @staticmethod
    @abc.abstractmethod
    def get_scaler_name():
        """Returns:
            str: the constant name which is associated to this scaler.
        """
        raise NotImplementedError()

    @staticmethod
    @abc.abstractmethod
    def is_indulgent_resizing():
        """This method specifies whether the
        algorithm returns noticeable different results for
        the same image with different sizes (bigger than the
        maximum size which is passed to the scale method).

        Returns:
            bool: False if the results differ
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def calculate_resolution(self, image, width: int, height: int):
        """Calculates the final resolution of the scaled image.

        Args:
            image (PIL.Image): the image which should be scaled
            width (int): maximum width that can be taken
            height (int): maximum height that can be taken

        Returns:
            tuple: final width: int, final height: int
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def scale(self, image, position: geometry.Point,
              width: int, height: int):
        """Scales the image according to the respective implementation.

        Args:
            image (PIL.Image): the image which should be scaled
            position (geometry.Position): the centered position, if possible
                Specified as factor of the image size,
                so it should be an element of [0, 1].
            width (int): maximum width that can be taken
            height (int): maximum height that can be taken

        Returns:
            PIL.Image: the scaled image
        """
        raise NotImplementedError()


class OffsetImageScaler(ImageScaler, metaclass=abc.ABCMeta):
    """Extension of the ImageScaler class by Offset specific functions."""
    # pylint can't detect abstract subclasses
    # pylint: disable=abstract-method

    @staticmethod
    def get_offset(position: float, target_size: float, image_size: float):
        """Calculates a offset which contains the position
        in a range from offset to offset + target_size.

        Args:
            position (float): the centered position, if possible
                Specified as factor of the image size,
                so it should be an element of [0, 1].
            target_size (int): the image size of the wanted result
            image_size (int): the image size

        Returns:
            int: the offset
        """
        return int(min(max(0, position * image_size - target_size / 2),
                       image_size - target_size))


class MinSizeImageScaler(ImageScaler):
    """Partial implementation of an ImageScaler.
    Subclasses calculate the final resolution of the scaled image
    as the minimum value of the image size and the maximum size.
    """
    # pylint: disable=abstract-method

    def calculate_resolution(self, image, width: int, height: int):
        return (min(width, image.width),
                min(height, image.height))


class CropImageScaler(MinSizeImageScaler, OffsetImageScaler):
    """Implementation of the ImageScaler
    which crops out the maximum image size.
    """

    @staticmethod
    def get_scaler_name():
        return "crop"

    @staticmethod
    def is_indulgent_resizing():
        return False

    def scale(self, image, position: geometry.Point,
              width: int, height: int):
        width, height = self.calculate_resolution(image, width, height)
        image_width, image_height = image.width, image.height
        offset_x = self.get_offset(position.x, width, image_width)
        offset_y = self.get_offset(position.y, height, image_height)
        return image \
            .crop((offset_x, offset_y,
                   offset_x + width, offset_y + height))


class DistortImageScaler(ImageScaler):
    """Implementation of the ImageScaler
    which distorts the image to the maximum image size.
    """

    @staticmethod
    def get_scaler_name():
        return "distort"

    @staticmethod
    def is_indulgent_resizing():
        return True

    def calculate_resolution(self, image, width: int, height: int):
        return width, height

    def scale(self, image, position: geometry.Point,
              width: int, height: int):
        import PIL.Image
        width, height = self.calculate_resolution(image, width, height)
        return image.resize((width, height), PIL.Image.ANTIALIAS)


class FitContainImageScaler(DistortImageScaler):
    """Implementation of the ImageScaler
    which resizes the image that either
    the width matches the maximum width
    or the height matches the maximum height
    while keeping the image ratio.
    """

    @staticmethod
    def get_scaler_name():
        return "fit_contain"

    @staticmethod
    def is_indulgent_resizing():
        return True

    def calculate_resolution(self, image, width: int, height: int):
        factor = min(width / image.width, height / image.height)
        return int(image.width * factor), int(image.height * factor)


class ContainImageScaler(FitContainImageScaler):
    """Implementation of the ImageScaler
    which resizes the image to a size <= the maximum size
    while keeping the image ratio.
    """

    @staticmethod
    def get_scaler_name():
        return "contain"

    @staticmethod
    def is_indulgent_resizing():
        return True

    def calculate_resolution(self, image, width: int, height: int):
        return super().calculate_resolution(
            image, min(width, image.width), min(height, image.height))


class ForcedCoverImageScaler(DistortImageScaler, OffsetImageScaler):
    """Implementation of the ImageScaler
    which resizes the image to cover the entire area which should be filled
    while keeping the image ratio.
    If the image is smaller than the desired size
    it will be stretched to reach the desired size.
    If the ratio of the area differs
    from the image ratio the edges will be cut off.
    """

    @staticmethod
    def get_scaler_name():
        return "forced_cover"

    @staticmethod
    def is_indulgent_resizing():
        return True

    def scale(self, image, position: geometry.Point,
              width: int, height: int):
        import PIL.Image
        width, height = self.calculate_resolution(image, width, height)
        image_width, image_height = image.width, image.height
        if width / image_width > height / image_height:
            image_height = int(image_height * width / image_width)
            image_width = width
        else:
            image_width = int(image_width * height / image_height)
            image_height = height
        offset_x = self.get_offset(position.x, width, image_width)
        offset_y = self.get_offset(position.y, height, image_height)

        return image \
            .resize((image_width, image_height), PIL.Image.ANTIALIAS) \
            .crop((offset_x, offset_y,
                   offset_x + width, offset_y + height))


class CoverImageScaler(MinSizeImageScaler, ForcedCoverImageScaler):
    """The same as ForcedCoverImageScaler but images won't be stretched
    if they are smaller than the area which should be filled.
    """

    @staticmethod
    def get_scaler_name():
        return "cover"

    @staticmethod
    def is_indulgent_resizing():
        return True


@enum.unique
class ScalerOption(str, enum.Enum):
    """Enum which lists the useable ImageScaler classes."""
    DISTORT = DistortImageScaler
    CROP = CropImageScaler
    FIT_CONTAIN = FitContainImageScaler
    CONTAIN = ContainImageScaler
    FORCED_COVER = ForcedCoverImageScaler
    COVER = CoverImageScaler

    def __new__(cls, scaler_class):
        inst = str.__new__(cls)
        # Based on an official example
        # https://docs.python.org/3/library/enum.html#using-a-custom-new
        # So.. stfu pylint
        # pylint: disable=protected-access
        inst._value_ = scaler_class.get_scaler_name()
        inst.scaler_class = scaler_class
        return inst
