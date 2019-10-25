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
# Switch/Turnout LEGO Track class

import math
from math import sin, cos, radians, sqrt, atan
import cairo
import gi
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango
from gi.repository import PangoCairo

from .track import *


class SwitchTrack(Track):

    def __init__ (self, length=40, vee=22.5, dir='L'):
        super().__init__()
        self.length = length
        self.vee = vee
        self.dir = dir
        self.dvx = 0
        self.dvy = 0

    def __str__(self):
        print("Switch Track, length %d studs, %f deg vee %s" % (self.length, self.vee, self.dir))

    def to_xml(self, fn):
        self.ComputeBBConnections()
        self.part.to_xml(fn)

    def ComputeBBConnections(self):
        self.ComputeExtents()
        self.part.conn_points = []
        if self.dir == 'L':
            oy = self.metrics.studRect.height/2 - self.metrics.width/2
            cy = oy - self.metrics.width
            an = 180.0
            ap = 0.0
            av = -self.vee
        elif self.dir == 'R':
            oy = -self.metrics.studRect.height/2 + self.metrics.width/2
            cy = oy + self.metrics.width
            ap = 180.0
            an = 0.0
            av = self.vee
        elif self.dir == 'Y':
            oy = 0
            cy = oy + self.metrics.width
            ap = 180.0
            an = 0.0
            av = self.vee

        # first (left) connection
        bbc = BBConnexion()
        bbc.position_x = -self.metrics.studRect.width/2
        bbc.position_y = oy
        bbc.angle = 180
        bbc.angleToPrev = ap
        bbc.angleToNext = an
        bbc.connPref = 1
        bbc.electricPlug = 1
        self.part.conn_points.append(bbc)

        # second (right) connection
        if (self.dir != 'Y'):
            bbc2 = BBConnexion()
            bbc2.position_x = self.metrics.studRect.width/2 - self.dvx
            bbc2.position_y = oy
            bbc2.angle = 0
            bbc2.angleToPrev = an
            bbc2.angleToNext = ap
            bbc2.connPref = 0
            bbc2.electricPlug = -1
            self.part.conn_points.append(bbc2)

        # diverging route connection
        bbc3 = BBConnexion()
        bbc3.position_x = self.metrics.studRect.width/2 - self.dvx
        bbc3.position_y = cy
        bbc3.angle = av
        bbc3.angleToPrev = -av
        bbc3.angleToNext = 180.0 - abs(av)
        bbc3.connPref = 0
        bbc3.electricPlug = -1
        self.part.conn_points.append(bbc3)

        # other Y diverging route connection
        if (self.dir == 'Y'):
            bbc4 = BBConnexion()
            bbc4.position_x = self.metrics.studRect.width/2 - self.dvx
            bbc4.position_y = oy - self.metrics.width
            bbc4.angle = -av
            bbc4.angleToPrev = av
            bbc4.angleToNext = 180.0 - abs(av)
            bbc4.connPref = 0
            bbc4.electricPlug = -1
            self.part.conn_points.append(bbc4)


    def ComputeExtents(self):
        thr = radians(self.vee)
        self.dvx = abs(self.metrics.width/2 * sin(thr))
        self.dvy = abs(self.metrics.width/2 * cos(thr))

        sw =  self.length + self.dvx
        sh = 2 * self.metrics.width - (self.metrics.width/2 - self.dvy)
        if (self.dir == 'Y'):
            sh = 2 * self.metrics.width + 2* self.dvy
#        print (sh)
        self.metrics.studRect.set_size(sw, sh)
        self.metrics.pixRect.set_size(sw * BB_SCALE, sh * BB_SCALE)

    def WritePNG(self, filename):
        thr = radians(self.vee)
        self.ComputeExtents()
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(self.metrics.pixRect.width), int(self.metrics.pixRect.height))
        ctx = cairo.Context(surface)
        ctx.scale(BB_SCALE, BB_SCALE)

        if self.label == '':
            label = "P" + str(self.length) + str(self.dir)
        else:
            label = self.label
        label_text = PangoCairo.create_layout(ctx)
        label_text.set_text(label, -1)
        label_text.set_font_description(self.style.font_desc_normal())

        # track rectangle
        if self.dir == 'L':
            oy = self.metrics.studRect.height - self.metrics.width
        elif self.dir == 'Y':
            oy = self.metrics.studRect.height/2 - self.metrics.width/2
        else:
            oy = 0
        if self.dir != 'Y':
            ctx.set_line_width(0)
            ctx.rectangle(0, oy, self.length, self.metrics.width)
            self.style.FillColor(ctx)
            ctx.set_line_width(0)
            ctx.fill_preserve()
            ctx.stroke()

        # diverging route
        if self.dir == 'L' or self.dir == 'Y':
            if self.dir == 'L':
                oy = self.metrics.studRect.height - self.metrics.width
            elif self.dir == 'Y':
                oy = self.metrics.studRect.height/2 - self.metrics.width/2
            cy = self.metrics.width/2
            dx = self.dvx
            gx = abs(self.metrics.gauge/2 * sin(thr))
            gy = abs(self.metrics.gauge/2 * cos(thr))
            bx = abs((self.metrics.width/2 - self.style.border_width/2) * sin(thr))
            by = abs((self.metrics.width/2 - self.style.border_width/2) * cos(thr))

            rm = 1.667
            go = (self.metrics.width - self.metrics.gauge) / 2
            cx = self.length
            ctx.set_line_width(0)
            ctx.move_to(cx - dx, cy - self.dvy)
            ctx.line_to(cx + dx, cy + self.dvy)
            ctx.curve_to(cx + dx, cy + self.dvy, cx/rm, oy+self.metrics.width, 0, oy+self.metrics.width)
            ctx.line_to(0, oy)
            ctx.curve_to(0, oy, cx/rm, oy, cx - dx, cy - self.dvy)
            ctx.close_path()
            self.style.FillColor(ctx)
            ctx.set_line_width(0)
            ctx.fill_preserve()
            ctx.stroke()

        if self.dir == 'R' or self.dir == 'Y':
            if self.dir == 'R':
                oy = 0
                cy = self.metrics.studRect.height/2 + self.metrics.width/2
            elif self.dir == 'Y':
                oy = self.metrics.studRect.height/2 - self.metrics.width/2
                cy = self.metrics.studRect.height/2 + self.metrics.width
            dx = -self.dvx
            gx = -abs(self.metrics.gauge/2 * sin(thr))
            gy = abs(self.metrics.gauge/2 * cos(thr))
            bx = -abs((self.metrics.width/2 - self.style.border_width/2) * sin(thr))
            by = abs((self.metrics.width/2 - self.style.border_width/2) * cos(thr))

            rm = 1.667
            go = (self.metrics.width - self.metrics.gauge) / 2
            cx = self.length
            ctx.set_line_width(0)
            ctx.move_to(cx - dx, cy - self.dvy)
            ctx.line_to(cx + dx, cy + self.dvy)
            ctx.curve_to(cx + dx, cy + self.dvy, cx/rm, oy+self.metrics.width, 0, oy+self.metrics.width)
            ctx.line_to(0, oy)
            ctx.curve_to(0, oy, cx/rm, oy, cx - dx, cy - self.dvy)
            ctx.close_path()
            self.style.FillColor(ctx)
            ctx.set_line_width(0)
            ctx.fill_preserve()
            ctx.stroke()

        # diverging route
        if self.dir == 'L' or self.dir == 'Y':
            if self.dir == 'L':
                oy = self.metrics.studRect.height - self.metrics.width
            elif self.dir == 'Y':
                oy = self.metrics.studRect.height/2 - self.metrics.width/2
            cy = self.metrics.width/2
            dx = self.dvx
            gx = abs(self.metrics.gauge/2 * sin(thr))
            gy = abs(self.metrics.gauge/2 * cos(thr))
            bx = abs((self.metrics.width/2 - self.style.border_width/2) * sin(thr))
            by = abs((self.metrics.width/2 - self.style.border_width/2) * cos(thr))

            # outer rail
            self.style.RailColor(ctx)
            if self.dir != 'Y':
                ctx.move_to(0, oy+self.metrics.width/2 - self.metrics.gauge/2)
                ctx.line_to(self.length, oy+self.metrics.width/2 - self.metrics.gauge/2)
            ctx.set_line_width(self.style.rail_width)
            ctx.stroke()
            ctx.curve_to(cx + gx, cy + gy, cx/rm, oy+self.metrics.width-go, 0, oy+self.metrics.width-go)
            ctx.stroke()

            # inner rail
            if self.dir != 'Y':
                ctx.move_to(0, oy+self.metrics.width/2 + self.metrics.gauge/2)
                ctx.line_to(self.length, oy+self.metrics.width/2 + self.metrics.gauge/2)
            ctx.set_line_width(self.style.rail_width)
            ctx.stroke()
            ctx.curve_to(0, oy+go, cx/rm, oy+go, cx - gx, cy - gy)
            ctx.stroke()

        if self.dir == 'R' or self.dir == 'Y':
            if self.dir == 'R':
                oy = 0
                cy = self.metrics.studRect.height/2 + self.metrics.width/2
            elif self.dir == 'Y':
                oy = self.metrics.studRect.height/2 - self.metrics.width/2
                cy = self.metrics.studRect.height/2 + self.metrics.width
            dx = -self.dvx
            gx = -abs(self.metrics.gauge/2 * sin(thr))
            gy = abs(self.metrics.gauge/2 * cos(thr))
            bx = -abs((self.metrics.width/2 - self.style.border_width/2) * sin(thr))
            by = abs((self.metrics.width/2 - self.style.border_width/2) * cos(thr))

            # outer rail
            self.style.RailColor(ctx)
            if self.dir != 'Y':
                ctx.move_to(0, oy+self.metrics.width/2 - self.metrics.gauge/2)
                ctx.line_to(self.length, oy+self.metrics.width/2 - self.metrics.gauge/2)
            ctx.set_line_width(self.style.rail_width)
            ctx.stroke()
            ctx.curve_to(cx + gx, cy + gy, cx/rm, oy+self.metrics.width-go, 0, oy+self.metrics.width-go)
            ctx.stroke()

            # inner rail
            if self.dir != 'Y':
                ctx.move_to(0, oy+self.metrics.width/2 + self.metrics.gauge/2)
                ctx.line_to(self.length, oy+self.metrics.width/2 + self.metrics.gauge/2)
            ctx.set_line_width(self.style.rail_width)
            ctx.stroke()
            ctx.curve_to(0, oy+go, cx/rm, oy+go, cx - gx, cy - gy)
            ctx.stroke()

        if self.style.border_width > 0:
            self.style.CapColor(ctx)
            ctx.set_line_width(self.style.border_width)
            if self.dir == 'L' or self.dir == 'Y':
                ctx.move_to(0, oy+self.metrics.width - self.style.border_width/2)
                ctx.line_to(self.length, oy+self.metrics.width - self.style.border_width/2)
            if self.dir == 'R' or self.dir == 'Y':
                ctx.move_to(0, self.style.border_width/2)
                ctx.line_to(self.length, self.style.border_width/2)
            ctx.stroke()
            bo = self.style.border_width / 2
            if self.dir == 'L' or self.dir == 'Y':
                ctx.curve_to(0, oy-bo, cx/rm, oy-bo, cx - dx, cy - self.dvy-bo)
            if self.dir == 'R' or self.dir == 'Y':
                ctx.curve_to(cx + bx, cy + by, cx/rm, oy+self.metrics.width-bo, 0, oy+self.metrics.width-bo)
            ctx.stroke()


        # end caps
        cw = self.style.cap_width
        self.style.CapColor(ctx)
        ctx.set_line_width(cw)
        ctx.move_to(cw/2, oy)
        ctx.line_to(cw/2, oy+self.metrics.width)
        if self.dir != 'Y':
            ctx.move_to(self.length - cw/2, oy)
            ctx.line_to(self.length - cw/2, oy+self.metrics.width)
        ctx.move_to(cx - dx, cy - self.dvy)
        ctx.line_to(cx + dx, cy + self.dvy)
        if self.dir == 'Y':
            oy = self.metrics.studRect.height/2 - self.metrics.width/2
            cy = self.metrics.width/2
            ctx.move_to(cx - dx, cy + self.dvy)
            ctx.line_to(cx + dx, cy - self.dvy)
        ctx.stroke()

        # label
        ctx.set_line_width(0)
        self.style.TextColor(ctx)
        xc = self.length / 5
        yc = self.metrics.width / 2 + oy
        ctx.save()
        ctx.move_to(xc, yc)
        PangoCairo.update_layout(ctx, label_text)
        width, height = label_text.get_size()
        fw = float(width)/1024.0
        fh = float(height)/1024.0
        if (fw > self.length):
            label_text.set_font_description(self.style.font_desc_small())
            ctx.move_to(xc+fh/4, yc-fw/4)
            ctx.rotate(radians(90))
        else:
            ctx.rotate(radians(0))
            ctx.move_to(xc-fw/2, yc-fh/2)
        PangoCairo.update_layout(ctx, label_text)
        PangoCairo.show_layout(ctx, label_text)
        ctx.restore()

        surface.write_to_png(filename)
