# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Functions that make the user's life easier.

import renpy.display
import contextlib
import time
import colorsys

class Color(tuple):
    """
    """

    _rgb = None
    _hls = None
    _hsv = None
    _alpha = None

    def __new__(cls, color=None, hls=None, hsv=None, rgb=None, alpha=1.0):

        if color is not None:
            c = color

            if isinstance(c, tuple) and len(c) == 4:
                if isinstance(c, Color):
                    return c

                return tuple.__new__(cls, c)

            if c is None:
                return None

            if isinstance(c, basestring):
                if c[0] == '#':
                    c = c[1:]

                if len(c) == 6:
                    r = int(c[0]+c[1], 16)
                    g = int(c[2]+c[3], 16)
                    b = int(c[4]+c[5], 16)
                    a = int(alpha * 255)
                elif len(c) == 8:
                    r = int(c[0]+c[1], 16)
                    g = int(c[2]+c[3], 16)
                    b = int(c[4]+c[5], 16)
                    a = int(c[6]+c[7], 16)
                elif len(c) == 3:
                    r = int(c[0], 16) * 0x11
                    g = int(c[1], 16) * 0x11
                    b = int(c[2], 16) * 0x11
                    a = int(alpha * 255)
                elif len(c) == 4:
                    r = int(c[0], 16) * 0x11
                    g = int(c[1], 16) * 0x11
                    b = int(c[2], 16) * 0x11
                    a = int(c[3], 16) * 0x11
                else:
                    raise Exception("Color string must be 3, 4, 6, or 8 hex digits long.")

                return tuple.__new__(cls, (r, g, b, a))

        if hsv is not None:
            rgb = colorsys.hsv_to_rgb(*hsv)

        if hls is not None:
            hsv = None
            rgb = colorsys.hls_to_rgb(*hsv)

        if rgb:
            r = int(rgb[0] * 255)
            g = int(rgb[0] * 255)
            b = int(rgb[0] * 255)
            a = int(alpha * 255)

            rv = tuple.__new__(cls, (r, g, b, a))
            rv._rgb = rgb
            rv._hls = hls
            rv._hsv = hsv
            rv._alpha = alpha

            return rv

        raise Exception("Not a color: %r" % (c,))

    def __repr__(self):
        return "<Color #{:02x}{:02x}{:02x}{:02x}>".format(
            self[0],
            self[1],
            self[2],
            self[3],
            )

    def __getnewargs__(self):
        return (tuple(self), )

    @property
    def rgb(self):
        if self._rgb is None:
            self._rgb = (
                self[0] / 255.0,
                self[1] / 255.0,
                self[2] / 255.0,
                )

        return self._rgb

    @property
    def hls(self):
        if self._hls is None:
            self._hls = colorsys.rgb_to_hls(*self.rgb)

        return self._hls

    @property
    def hsv(self):
        if self._hsv is None:
            self._hsv = colorsys.rgb_to_hsv(*self.rgb)

        return self._hsv

    @property
    def alpha(self):
        if self._alpha is None:
            self._alpha = self[3] / 255.0

        return self._alpha


color = Color

def displayable_or_none(d):

    if isinstance(d, renpy.display.core.Displayable):
        return d

    if d is None:
        return d

    if isinstance(d, basestring):
        if d[0] == '#':
            return renpy.store.Solid(d)
        elif "." in d:
            return renpy.store.Image(d)
        elif not d:
            raise Exception("Displayable cannot be an empty string.")
        else:
            return renpy.store.ImageReference(tuple(d.split()))

    # We assume the user knows what he's doing in this case.
    if hasattr(d, 'parameterize'):
        return d

    if d is True or d is False:
        return d

    raise Exception("Not a displayable: %r" % (d,))

def displayable(d):
    """
    :doc: udd_utility
    :name: renpy.displayable

    This takes `d`, which may be a displayable object or a string. If it's
    a string, it converts that string into a displayable using the usual
    rules.
    """


    if isinstance(d, renpy.display.core.Displayable):
        return d

    if isinstance(d, basestring):
        if not d:
            raise Exception("An empty string cannot be used as a displayable.")
        elif d[0] == '#':
            return renpy.store.Solid(d)
        elif "." in d:
            return renpy.store.Image(d)
        else:
            return renpy.store.ImageReference(tuple(d.split()))

    # We assume the user knows what he's doing in this case.
    if hasattr(d, 'parameterize'):
        return d

    if d is True or d is False:
        return d

    raise Exception("Not a displayable: %r" % (d,))

def predict(d):
    d = renpy.easy.displayable_or_none(d)

    if d is not None:
        renpy.display.predict.displayable(d)

@contextlib.contextmanager
def timed(name):
    start = time.time()
    yield
    print "{0}: {1:.2f} ms".format(name, (time.time() - start) * 1000.0)

