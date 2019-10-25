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
# BlueBrick library part class

from pathlib import Path
import xml.etree.ElementTree as et
import xml.dom.minidom as minidom

from .bbhelpers import add_xml_element

class BBConnexion:

    def __init__(self):
        self.type = 1
        self.position_x = 0
        self.position_y = 0
        self.angle = 0
        self.angleToPrev = 0
        self.angleToNext = 0
        self.connPref = 1
        self.electricPlug = 1

    def to_xml(self, tree, parent):
        c = tree.SubElement(parent, 'connexion')
        add_xml_element(tree, c, 'type', self.type)
        pos = tree.SubElement(c, 'position')
        add_xml_element(tree, pos, 'x', self.position_x)
        add_xml_element(tree, pos, 'y', self.position_y)
        add_xml_element(tree, c, 'angle', self.angle)
        add_xml_element(tree, c, 'angleToPrev', self.angleToPrev)
        add_xml_element(tree, c, 'angleToNext', self.angleToNext)
        add_xml_element(tree, c, 'nextConnexionPreference', self.connPref)
        add_xml_element(tree, c, 'electricPlug', self.electricPlug)


class BBPart(object):

    def __init__(self):
        self.author = 'L-Gauge.org'
        self.descriptions = { 'en': 'Placeholder description in English'}
        self.snapmargin = { 'left' : 0.0,
                            'right' : 0.0,
                            'top' : 0.0,
                            'bottom' : 0.0 }
        self.conn_points = []
        self.colour = 0

    def to_xml(self, filename):
        root = et.Element('part')
        add_xml_element(et, root, 'Author', self.author)
        desc = et.SubElement(root, 'Description')
        for lang, description in self.descriptions.items():
            add_xml_element(et, desc, lang, description)
        snap = et.SubElement(root, 'SnapMargin')
        for dir, margin in self.snapmargin.items():
            add_xml_element(et, snap, dir, margin)
        conn = et.SubElement(root, 'ConnexionList')
        for connexion in self.conn_points:
            connexion.to_xml(et, conn)
        tree = et.ElementTree(root)

        xmlstr = minidom.parseString(et.tostring(root, encoding='utf-8')).toprettyxml(indent="   ", encoding='utf-8')
        with open(filename, "w") as f:
            f.write(xmlstr.decode('utf-8'))
