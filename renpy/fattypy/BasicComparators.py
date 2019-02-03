# Copyright 2019 Grotlover2 <grotover2@live.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This file contains the definitions for the basic comparators provided with fattypy
from renpy.fattypy.DDCharacter import DDCharacter


# Used to hold some common checking code
class BaseComparator:
    def __init__(self, attribute_name):
        self.attribute = attribute_name

    def eval(self, dd_char):
        if not isinstance(dd_char, DDCharacter):
            raise TypeError("Comparator can only be used on a DDCharacter object")

        return self.attribute in dd_char


class EquivalenceComparator(BaseComparator):
    def __init__(self, attribute_name, value):
        BaseComparator.__init__(self, attribute_name)

        self.value = value

    def eval(self, dd_char):
        if BaseComparator.eval(self, dd_char):
            return dd_char[self.attribute] == self.value

        return False  # lets be pessimistic and assume we are going to fail


class LessThanComparator(BaseComparator):
    def __init__(self, attribute_name, value):
        BaseComparator.__init__(self, attribute_name)

        self.value = value

    def eval(self, dd_char):
        if BaseComparator.eval(self, dd_char):
            return dd_char[self.attribute] < self.value

        return False  # lets be pessimistic and assume we are going to fail


class GreaterThanComparator(BaseComparator):
    def __init__(self, attribute_name, value):
        BaseComparator.__init__(self, attribute_name)

        self.value = value

    def eval(self, dd_char):
        if BaseComparator.eval(self, dd_char):
            return dd_char[self.attribute] > self.value

        return False  # lets be pessimistic and assume we are going to fail


class RangeComparator(BaseComparator):
    def __init__(self, attribute_name, min_value, max_value):
        BaseComparator.__init__(self, attribute_name)

        self.min = min_value
        self.max = max_value

    def eval(self, dd_char):
        if BaseComparator.eval(self, dd_char):
            return self.min <= dd_char[self.attribute] <= self.max

        return False  # lets be pessimistic and assume we are going to fail
