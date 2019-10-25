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
# Crossing LEGO Track class

import math
from math import sin, cos, radians, sqrt, atan
import cairo
import gi
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango
from gi.repository import PangoCairo

from .track import Track

class CrossingTrack(Track):

    def __init__ (self):
        super().__init__()
        self.length = 16
        self.length2 = 16
        self.angle = 90

    def __str__(self):
        print("Crossing Track, %f deg, length %f" % (self.angle, self.length))

    def to_xml(self, fn):
        self.ComputeBBConnections()
        self.part.to_xml(fn)

    def ComputeExtents(self):
        ox, oy = GetBoundingRect(self.length2, self.metrics.width, self.angle)
        if ox > self.length:
            self.dvx = ox - self.length
        else:
            self.dvx = 0.0
        if oy > self.metrics.width:
            self.dvy = oy - self.metrics.width
        else:
            self.dvx = 0.0
        sw = self.length + self.dvx
        sh = self.metrics.width + self.dvy
        self.metrics.studRect.set_size(sw, sh)
        self.metrics.pixRect.set_size(sw * BB_SCALE, sh * BB_SCALE)

    def ComputeBBConnections(self):
        self.ComputeExtents()
        self.part.conn_points = []

        # first (left) connection
        bbc = BBConnexion()
        bbc.position_x = -self.metrics.studRect.width/2 + self.dvx/2
        bbc.position_y = 0.0
        bbc.angle = 180
        bbc.angleToPrev = 180
        bbc.angleToNext = 0
        bbc.connPref = 1
        bbc.electricPlug = 1
        self.part.conn_points.append(bbc)

        # second (right) connection
        bbc2 = BBConnexion()
        bbc2.position_x = self.metrics.studRect.width/2 - self.dvx/2
        bbc2.position_y = 0.0
        bbc2.angle = 0
        bbc2.angleToPrev = 0
        bbc2.angleToNext = 180
        bbc2.connPref = 0
        bbc2.electricPlug = -1
        self.part.conn_points.append(bbc2)

        # diverging route connection left
        bbc3 = BBConnexion()
        bbc3.position_x = self.length2/2 * cos(radians(-self.angle))
        bbc3.position_y = -self.length2/2 * sin(radians(-self.angle))
        bbc3.angle = self.angle
        bbc3.angleToPrev = -self.angle
        bbc3.angleToNext = 180.0 - abs(self.angle)
        bbc3.connPref = 0
        bbc3.electricPlug = 1
        self.part.conn_points.append(bbc3)

        # diverging route connection left
        bbc4 = BBConnexion()
        bbc4.position_x = -self.length2/2 * cos(radians(self.angle))
        bbc4.position_y = -self.length2/2 * sin(radians(self.angle))
        bbc4.angle = -180 + self.angle
        bbc4.angleToPrev = 180 - self.angle
        bbc4.angleToNext = 180.0 - abs(self.angle)
        bbc4.connPref = 0
        bbc4.electricPlug = -1
        self.part.conn_points.append(bbc4)

    def WritePNG(self, filename):

        self.ComputeExtents()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(self.metrics.pixRect.width), int(self.metrics.pixRect.height))
        ctx = cairo.Context(surface)
        ctx.scale(BB_SCALE, BB_SCALE)

        if self.label == "":
            label = "X" + str(self.length)
        else:
            label = self.label
        label_text = PangoCairo.create_layout(ctx)
        label_text.set_text(label, -1)
        label_text.set_font_description(self.style.font_desc_normal())

        ctx.translate(self.metrics.studRect.width/2, self.metrics.studRect.height/2)
        xl = -self.length/2
        xr = xl + self.length
        xl2 = -self.length2/2
        xr2 = xl2 + self.length2
        yt = -self.metrics.width/2
        yb = self.metrics.width/2
        gt = -self.metrics.gauge/2
        gb = self.metrics.gauge/2

        # track rectangle
        ctx.set_line_width(0)
        ctx.move_to(xl, yt)
        ctx.line_to(xr, yt)
        ctx.line_to(xr, yb)
        ctx.line_to(xl, yb)
        ctx.close_path()
        self.style.FillColor(ctx)
        ctx.set_line_width(0)
        ctx.fill_preserve()
        ctx.stroke()

        ctx.save()
        ctx.rotate(radians(self.angle))
        ctx.move_to(xl2, yt)
        ctx.line_to(xr2, yt)
        ctx.line_to(xr2, yb)
        ctx.line_to(xl2, yb)
        ctx.close_path()
        self.style.FillColor(ctx)
        ctx.set_line_width(0)
        ctx.fill_preserve()
        ctx.stroke()
        ctx.restore()

        # rails
        self.style.RailColor(ctx)
        ctx.set_line_width(self.style.rail_width)
        ctx.move_to(xr, gt)
        ctx.line_to(xl, gt)
        ctx.move_to(xl, gb)
        ctx.line_to(xr, gb)
        ctx.stroke()

        ctx.save()
        ctx.set_line_width(self.style.rail_width)
        self.style.RailColor(ctx)
        ctx.rotate(radians(self.angle))
        ctx.move_to(xr2, gt)
        ctx.line_to(xl2, gt)
        ctx.move_to(xl2, gb)
        ctx.line_to(xr2, gb)
        ctx.restore()
        ctx.stroke()

        # end caps
        cw = self.style.cap_width
        self.style.CapColor(ctx)
        ctx.set_line_width(cw)
        ctx.move_to(xl, yt)
        ctx.line_to(xl, yb)
        ctx.move_to(xr, yt)
        ctx.line_to(xr, yb)
        ctx.stroke()

        ctx.save()
        ctx.rotate(radians(self.angle))
        self.style.CapColor(ctx)
        ctx.set_line_width(cw)
        ctx.move_to(xl2, yt)
        ctx.line_to(xl2, yb)
        ctx.move_to(xr2, yt)
        ctx.line_to(xr2, yb)
        ctx.restore()
        ctx.stroke()

        # label
        ctx.set_line_width(0)
        self.style.TextColor(ctx)
        ctx.save()
        ctx.move_to(0, 0)
        PangoCairo.update_layout(ctx, label_text)
        width, height = label_text.get_size()
        fw = float(width)/1024.0
        fh = float(height)/1024.0
        ctx.move_to(-fw/2, -fh/2)
        PangoCairo.update_layout(ctx, label_text)
        PangoCairo.show_layout(ctx, label_text)
        ctx.restore()

        surface.write_to_png(filename)
