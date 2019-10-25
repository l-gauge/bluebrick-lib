#! /usr/bin/env python3
#
# Copyright (C) 2018  Fx Bricks Inc.
# This file is part of the legocad python module.
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# BlueBrick library helper functions

import string
import cairo
import gi
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango
from gi.repository import PangoCairo

from fxgeometry import Rect

BB_SCALE = 8

class BBStyle:

    def __init__(self):
        self.rail_width = 0.5
        self.cap_width = 0.3
        self.border_width = 0.0
        self.fill_color = [0.2, 0.3, 0.5]
        self.rail_color = [1, 1, 1]
        self.cap_color = [1, 1, 1]
        self.text_color = [1, 1, 1]
        self.text_height = 3.5
        self.text_rot = 0
        self.font_normal = "Ikea Sans Heavy " + str(self.text_height)
        self.font_small = "Ikea Sans Heavy " + str(self.text_height/1.5)

    def set_text_height(self, height):
        self.text_height = height
        self.font_normal = "Ikea Sans Heavy " + str(self.text_height)
        self.font_small = "Ikea Sans Heavy " + str(self.text_height/1.5)

    def font_desc_normal(self):
        return Pango.FontDescription(self.font_normal)

    def font_desc_small(self):
        return Pango.FontDescription(self.font_small)

    def FillColor(self, context):
        context.set_source_rgb(self.fill_color[0], self.fill_color[1], self.fill_color[2])
    def RailColor(self, context):
        context.set_source_rgb(self.rail_color[0], self.rail_color[1], self.rail_color[2])
    def CapColor(self, context):
        context.set_source_rgb(self.cap_color[0], self.cap_color[1], self.cap_color[2])
    def TextColor(self, context):
        context.set_source_rgb(self.text_color[0], self.text_color[1], self.text_color[2])

    def SetGrey(self):
        self.fill_color = [0.5, 0.5, 0.5]
        self.rail_color = [1, 1, 1]
        self.cap_color = [1, 1, 1]
        self.text_color = [1, 1, 1]


    def SetMono(self):
        self.border_width = 0.3
        self.fill_color = [1, 1, 1]
        self.rail_color = [0, 0, 0]
        self.cap_color = [0, 0, 0]
        self.text_color = [0, 0, 0]

    @staticmethod
    def RGBFromHex(hexStr):
        if len(hexStr) < 6:
            return 0, 0, 0
        hs = hexStr.lstrip("#")
        if not all(c in string.hexdigits for c in hs):
            return 0, 0, 0
        [rd, gd, bd] = tuple(int(hs[i : i + 2], 16) for i in (0, 2, 4))
        r = float(rd) / 255.0
        g = float(gd) / 255.0
        b = float(bd) / 255.0
        return r, g, b


class BBMetrics:

    def __init__(self):
        self.width = 8
        self.gauge = 5
        self.studRect = Rect()
        self.pixRect = Rect()


def add_xml_element(tree, parent, tag, text):
    e = tree.SubElement(parent, tag)
    e.text = str(text)
