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
# Curved LEGO Track class

import math
from math import sin, cos, radians, sqrt, atan
import cairo
import gi
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango
from gi.repository import PangoCairo

from .track import *


class CurveTrack(Track):

    def __init__ (self, radius=40, theta=22.5):
        super().__init__()
        self.radius = radius    # studs
        self.theta = theta      # sector angle in degrees
        self.nTies = 3

    def __str__(self):
        print("Curved Track, radius %d studs with %.2f deg sector angle" % (self.radius, self.theta))

    def to_xml(self, fn):
        self.ComputeBBConnections()
        self.part.to_xml(fn)

    def ComputeExtents(self):
        rpw2 = self.radius + self.metrics.width / 2
        rmw2 = self.radius - self.metrics.width / 2
        thr = -radians(self.theta)
        rdx = self.radius - (self.radius * cos(radians(self.theta)))
        sw = self.metrics.width + rdx + self.style.border_width
        sh = abs(rpw2 * sin(thr))
        self.metrics.studRect.set_size(sw, sh)
        self.metrics.pixRect.set_size(sw * BB_SCALE, sh * BB_SCALE)

    def ComputeBBConnections(self):
        self.part.conn_points = []
        self.ComputeExtents()
        w2 = self.metrics.studRect.width/2
        h2 = self.metrics.studRect.height/2
        rdx = self.radius - (self.radius * cos(radians(self.theta)))
        rdy = (self.radius + self.metrics.width/2 - self.style.border_width/2) * sin(radians(self.theta))
        rdy -= self.radius * sin(radians(self.theta))
        a1 = 90.0
        a2 = -90.0 - self.theta

        # first (bottom) connection
        bbc = BBConnexion()
        bbc.position_x = w2 - (self.metrics.width/2 + self.style.border_width/2)
        bbc.position_y = h2
        bbc.angle = a1
        bbc.angleToPrev = (a1 - a2)
        bbc.angleToNext = (a1 + a2) + 180.0
        bbc.connPref = 1
        bbc.electricPlug = 1
        self.part.conn_points.append(bbc)

        # second (top) connection
        bbc2 = BBConnexion()
        bbc2.position_x = w2 - (self.metrics.width/2 + self.style.border_width/2) - rdx
        bbc2.position_y = -h2 + rdy
        bbc2.angle = a2
        bbc2.angleToPrev = (a1 + a2) + 180.0
        bbc2.angleToNext = (a1 - a2)
        bbc2.connPref = 0
        bbc2.electricPlug = -1
        self.part.conn_points.append(bbc2)

    def WritePNG(self, filename):

        rpw2 = self.radius + self.metrics.width / 2
        rmw2 = self.radius - self.metrics.width / 2
        thr = -radians(self.theta)
        self.ComputeExtents()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(self.metrics.pixRect.width), int(self.metrics.pixRect.height))
        ctx = cairo.Context(surface)
        ctx.scale(BB_SCALE, BB_SCALE)
        rdx = self.radius - (self.radius * cos(radians(self.theta)))
        ctx.translate(-self.radius + self.metrics.width/2 + rdx, self.metrics.studRect.height)

        if self.label == '':
            label = "R" + str(self.radius)
        else:
            label = self.label
        label_text = PangoCairo.create_layout(ctx)
        label_text.set_text(label, -1)
        label_text.set_font_description(self.style.font_desc_normal())

        # track sector
        ctx.set_line_width(0)
        ctx.move_to(rpw2, 0)
        ctx.line_to(rmw2, 0)
        ctx.arc_negative(0,0, self.radius + self.metrics.width/2, 0, thr)
        ctx.line_to(rmw2 * cos(thr), rmw2 * sin(thr))
        ctx.arc(0,0, self.radius - self.metrics.width/2, thr, 0)
        ctx.close_path()
        self.style.FillColor(ctx)
        ctx.fill_preserve()
        ctx.stroke()

        # outer rail
        self.style.RailColor(ctx)
        ctx.arc_negative(0, 0, self.radius + self.metrics.gauge/2, 0, radians(-self.theta))
        ctx.set_line_width(self.style.rail_width)
        ctx.stroke()
        # inner rail
        ctx.arc_negative(0, 0, self.radius - self.metrics.gauge/2, 0, radians(-self.theta))
        ctx.set_line_width(self.style.rail_width)
        ctx.stroke()

        if self.style.border_width > 0:
            self.style.CapColor(ctx)
            ctx.set_line_width(self.style.border_width)
            ctx.arc_negative(0, 0, self.radius + self.metrics.width/2 - self.style.border_width/2, 0, radians(-self.theta))
            ctx.stroke()
            ctx.arc_negative(0, 0, self.radius - self.metrics.width/2, 0, radians(-self.theta))
            ctx.stroke()

        # end caps
        cw = self.style.cap_width
        self.style.CapColor(ctx)
        ctx.set_line_width(cw)
        ctx.move_to(rpw2, -cw/2)
        ctx.line_to(rmw2, -cw/2)
        ctx.move_to(rmw2 * cos(thr)-cw/2, rmw2 * sin(thr)+cw/2)
        ctx.line_to(rpw2 * cos(thr)+cw/2, rpw2 * sin(thr)+cw/2)
        ctx.stroke()

        # label
        ctx.set_line_width(0)
        self.style.TextColor(ctx)
        xc = self.radius * cos(thr/2)
        yc = self.radius * sin(thr/2)
        ctx.save()
        ctx.move_to(xc, yc)
        PangoCairo.update_layout(ctx, label_text)
        width, height = label_text.get_size()
        fw = float(width)/1024.0
        fh = float(height)/1024.0
        x = xc + fh/2 + (fw/2*sin(thr/2))
        y = yc - fw/2
        ctx.move_to(x, y)
        ctx.rotate(radians(90 - self.theta/2))
        PangoCairo.update_layout(ctx, label_text)
        PangoCairo.show_layout(ctx, label_text)
        ctx.restore()

        surface.write_to_png(filename)
