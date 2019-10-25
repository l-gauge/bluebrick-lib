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
# Straight LEGO Track class

import math
from math import sin, cos, radians, sqrt, atan
import cairo
import gi
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango
from gi.repository import PangoCairo

from .track import *


class StraightTrack(Track):

    def __init__ (self, length=16):
        super().__init__()
        self.length = length  # studs

    def __str__(self):
        print("Straight Track, length %d studs" % (self.length))

    def to_xml(self, fn):
        self.ComputeBBConnections()
        self.part.to_xml(fn)

    def ComputeBBConnections(self):
        self.part.conn_points = []

        # first (left) connection
        bbc = BBConnexion()
        bbc.position_x = -self.length/2
        bbc.position_y = 0
        bbc.angle = 180
        bbc.angleToPrev = 180.0
        bbc.angleToNext = 180.0
        bbc.connPref = 1
        bbc.electricPlug = 1
        self.part.conn_points.append(bbc)

        # second (right) connection
        bbc2 = BBConnexion()
        bbc2.position_x = self.length/2
        bbc2.position_y = 0
        bbc2.angle = 0
        bbc2.angleToPrev = 180.0
        bbc2.angleToNext = 180.0
        bbc2.connPref = 0
        bbc2.electricPlug = -1
        self.part.conn_points.append(bbc2)


    def WritePNG(self, filename):

        self.metrics.pixRect.set_size(self.length * BB_SCALE, self.metrics.width * BB_SCALE)
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(self.metrics.pixRect.width), int(self.metrics.pixRect.height))
        ctx = cairo.Context(surface)
        ctx.scale(BB_SCALE, BB_SCALE)

        if self.label == '':
            label = "S" + str(self.length)
        else:
            label = self.label
        label_text = PangoCairo.create_layout(ctx)
        label_text.set_text(label, -1)
        label_text.set_font_description(self.style.font_desc_normal())

        # track rectangle
        ctx.set_line_width(self.style.border_width)
        self.style.CapColor(ctx)
        ctx.rectangle(0, 0, self.length, self.metrics.width)
        self.style.FillColor(ctx)
        ctx.fill_preserve()
        ctx.stroke()

        # rails
        self.style.RailColor(ctx)
        ctx.set_line_width(self.style.rail_width)
        ctx.move_to(0, self.metrics.width/2 - self.metrics.gauge/2)
        ctx.line_to(self.length, self.metrics.width/2 - self.metrics.gauge/2)
        ctx.move_to(0, self.metrics.width/2 + self.metrics.gauge/2)
        ctx.line_to(self.length, self.metrics.width/2 + self.metrics.gauge/2)
        ctx.stroke()

        if self.style.border_width > 0:
            self.style.CapColor(ctx)
            bw = self.style.border_width
            ctx.set_line_width(bw)
            ctx.move_to(0, self.metrics.width - bw/2)
            ctx.line_to(self.length, self.metrics.width - bw/2)
            ctx.move_to(0, bw/2)
            ctx.line_to(self.length, bw/2)
            ctx.stroke()

        # end caps
        cw = self.style.cap_width
        self.style.CapColor(ctx)
        ctx.set_line_width(cw)
        ctx.move_to(cw/2, 0)
        ctx.line_to(cw/2, self.metrics.width)
        ctx.move_to(self.length - cw/2, 0)
        ctx.line_to(self.length - cw/2, self.metrics.width)
        ctx.stroke()

        # label
        ctx.set_line_width(0)
        self.style.TextColor(ctx)
        xc = self.length / 2
        yc = self.metrics.width / 2
        ctx.save()
        ctx.move_to(xc, yc)
        PangoCairo.update_layout(ctx, label_text)
        width, height = label_text.get_size()
        fw = float(width)/1024.0
        fh = float(height)/1024.0
        if (fw > self.length):
            label_text.set_font_description(self.style.font_desc_small())
            ctx.move_to(xc+fh/3, yc-fw/3)
            ctx.rotate(radians(90))
        else:
            ctx.rotate(radians(0))
            ctx.move_to(xc-fw/2, yc-fh/2)
        PangoCairo.update_layout(ctx, label_text)
        PangoCairo.show_layout(ctx, label_text)
        ctx.restore()

        surface.write_to_png(filename)
