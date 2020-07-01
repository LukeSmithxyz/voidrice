import sys
import struct
import fcntl
import termios
import math


class TerminalInfo:
    @staticmethod
    def get_size(fd_pty=None):
        """Determines the columns, rows, width (px),
        height (px) of the terminal.

        Returns:
            tuple of int: cols, rows, width, height
        """
        fd_pty = fd_pty or sys.stdout.fileno()
        farg = struct.pack("HHHH", 0, 0, 0, 0)
        fretint = fcntl.ioctl(fd_pty, termios.TIOCGWINSZ, farg)
        rows, cols, xpixels, ypixels = struct.unpack("HHHH", fretint)
        return cols, rows, xpixels, ypixels

    @staticmethod
    def __guess_padding(chars, pixels):
        # (this won't work all the time but
        # it's still better than disrespecting padding all the time)
        # let's assume the padding is the same on both sides:
        # let font_width = floor(xpixels / cols)
        # (xpixels - padding)/cols = font_size
        # <=> (xpixels - padding) = font_width * cols
        # <=> - padding = font_width * cols - xpixels
        # <=> padding = - font_width * cols + xpixels
        font_size = math.floor(pixels / chars)
        padding = (- font_size * chars + pixels) / 2
        return padding

    @staticmethod
    def __guess_font_size(chars, pixels, padding):
        return (pixels - 2 * padding) / chars

    def __init__(self, pty=None):
        self.pty = pty
        self.font_width = None
        self.font_height = None
        self.padding_vertical = None
        self.padding_horizontal = None

    @property
    def ready(self):
        """bool: True if the information
        of every attribute has been calculated.
        """
        return all((self.font_width, self.font_height,
                    self.padding_vertical, self.padding_horizontal))

    def reset(self):
        """Resets the font size and padding."""
        self.font_width = None
        self.font_height = None
        self.padding_vertical = None
        self.padding_horizontal = None

    def calculate_sizes(self, fallback_width, fallback_height):
        """Calculates the values for font_{width,height} and
        padding_{horizontal,vertical}.
        """
        if isinstance(self.pty, (int, type(None))):
            self.__calculate_sizes(self.pty, fallback_width, fallback_height)
        else:
            with open(self.pty) as fd_pty:
                self.__calculate_sizes(fd_pty, fallback_width, fallback_height)

    def __calculate_sizes(self, fd_pty, fallback_width, fallback_height):
        cols, rows, xpixels, ypixels = TerminalInfo.get_size(fd_pty)
        xpixels = xpixels or fallback_width
        ypixels = ypixels or fallback_height
        padding_horizontal = self.__guess_padding(cols, xpixels)
        padding_vertical = self.__guess_padding(rows, ypixels)
        self.padding_horizontal = max(padding_horizontal, padding_vertical)
        self.padding_vertical = self.padding_horizontal
        self.font_width = self.__guess_font_size(
            cols, xpixels, self.padding_horizontal)
        self.font_height = self.__guess_font_size(
            rows, ypixels, self.padding_vertical)

        if xpixels < fallback_width and ypixels < fallback_height:
            # some terminal emulators return the size of the text area
            # instead of the size of the whole window
            # -----
            # we're still missing information
            # e.g.:
            #   we know the size of the text area but
            #   we still don't know the margin of the text area to the edges
            #   (a character has a specific size so:
            #    there's some additional varying space
            #    if the character size isn't a divider of
            #    (window size - padding))
            #   -> it's okay not to know it
            #      if the terminal emulator centers the text area
            #      (kitty seems to do that)
            #   -> it's not okay not to know it
            #      if the terminal emulator just
            #      adds the additional space to the right margin
            #      (which will most likely be done)
            #      (stterm seems to do that)
            self.padding_horizontal = 1/2 * (fallback_width - xpixels)
            self.padding_vertical = 1/2 * (fallback_height - ypixels)
            self.font_width = xpixels / cols
            self.font_height = ypixels / rows
