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

# This file contains the implementation of the Dynamically Displayable (DD) Character object. This modified
# ADVCharacter object uses set "attributes" stored in an external store to auto generate image tags for display.

import ast
import renpy
from renpy.character import ADVCharacter, NotSet


class DDCharacter(ADVCharacter):
    def __init__(self, name=NotSet, kind=None, **properties):

        self.comparators = list()
        if kind is None:
            kind = renpy.defaultstore.dd

        if "image" in properties:
            self.defaultImage = properties["image"]
        else:
            self.defaultImage = None

        ADVCharacter.__init__(self, name, kind, **properties)

        def get_property(n, clone):
            if n in properties:
                return properties.pop(n)
            elif clone:
                return getattr(kind, n)

        attr_raw = get_property("attributes", False)

        # set attribute defaults
        if attr_raw is not None:
            # get the tuple pairs
            for pair in attr_raw.split():

                if '=' in pair:
                    attribute_name, value = pair.split('=', 1)
                elif ',' in pair:
                    attribute_name, value = pair.split(',', 1)
                else:
                    attribute_name = pair.strip()
                    value = ""

                self[attribute_name] = self.eval_value(value)

        # TODO: Come back and make code that will load the kinds comparator list
        #  instead of keeping a copy of the raw list
        self.img_tag_map = get_property("img_tag_map", True)

        # check if the first element of the img_tag_map is a tuple. If it is we can assume the rest are and if not we
        # can assume only one map was passed
        if self.img_tag_map is not None:
            if len(self.img_tag_map) > 0 and isinstance(self.img_tag_map[0], tuple):
                for c_map in self.img_tag_map:
                    self.register_comparator(c_map)
            else:
                self.register_comparator(self.img_tag_map)

    def __setitem__(self, attribute, value):
        # first time through if this character is not in the store add it
        if self.name not in renpy.defaultstore.characterAttributes.keys():
            renpy.defaultstore.characterAttributes[self.name] = dict()

        attributes_dict = renpy.defaultstore.characterAttributes[self.name]

        # only update if the value will change or a new attribute is being added
        if attribute not in attributes_dict.keys() or attributes_dict[attribute] != value:
            attributes_dict[attribute] = value

            # update the image tag with the new value if it was set
            if self.image_tag is not None:
                self.image_tag = self.get_img_tag()

    def __getitem__(self, attribute):
        attributes_dict = renpy.defaultstore.characterAttributes.get(self.name)

        if attributes_dict is None:
            return None

        return attributes_dict.get(attribute)

    def __contains__(self, attribute):
        attributes_dict = renpy.defaultstore.characterAttributes.get(self.name)

        if attributes_dict is not None and attribute in attributes_dict.keys():
            return True

        return False

    def __delitem__(self, attribute):
        attributes_dict = renpy.defaultstore.characterAttributes.get(self.name)

        if attributes_dict is not None:
            del attributes_dict[attribute]

    # Used to prevent __len__ from being used for truth testing on the object
    def __nonzero__(self):
        return True

    def __len__(self):
        attributes_dict = renpy.defaultstore.characterAttributes.get(self.name)

        if attributes_dict is None:
            return 0

        return len(attributes_dict)

    def show(self, name=None, at_list=[], layer=None, what=None, zorder=None, tag=None, behind=[], atl=None,
             transient=False, munge_name=True):
        from renpy.exports import show

        found_img_tag = tuple(self.get_img_tag().split())

        name = found_img_tag + name[1:]

        # set the image tag for the display say command if set
        if self.image_tag is not None:
            self.image_tag = found_img_tag

        show(name, at_list, layer, what, zorder, tag, behind, atl, transient, munge_name)

    def hide(self, name, layer=None):
        from renpy.exports import hide

        found_img_tag = tuple(self.get_img_tag().split())

        name = found_img_tag + name[1:]

        hide(name, layer)

    def register_comparator(self, comparator):

        if not isinstance(comparator, tuple):
            comparator = tuple(comparator.split(','))

        self.comparators.append(comparator)

    def eval_comparators(self):
        image_tag = None

        for comparator in self.comparators:
            all_eval_true = True
            for operation in comparator[0:-1]:
                if not operation.eval(self):
                    all_eval_true = False
                    break

            if all_eval_true:
                image_tag = comparator[-1]
                break

        return image_tag

    def get_img_tag(self):
        # check if an image tag was found
        img_tag = self.eval_comparators()

        # check if a image tag was not found
        if img_tag is None:
            if self.defaultImage is not None:
                img_tag = self.defaultImage
            else:
                img_tag = "DDCharacter(" + self.name + ")"

        return img_tag.strip()

    def eval_value(self, value):
        # check if white space or empty and try to evaluate it to a python type

        if isinstance(value, unicode):
            value = value.strip()
            if not value:
                value = None
            else:
                try:
                    value = ast.literal_eval(value)
                except ValueError:
                    value = value

        return value
