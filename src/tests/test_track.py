# system modules
import math, os.path
import sys
import pytest
from math import pi

# my modules
from pybb import *

OUTPUT_PATH = "./files/"

straights = [
  {'label': 'S8', 'length': 8, 'color': '404040'},
  {'label': 'S16', 'length': 16, 'color': '404040'},
]

curves = [
  {'label': 'R40', 'radius': 40, 'sector': 22.5, 'color': 'FB0207'},
  {'label': 'R88', 'radius': 88, 'sector': 11.25, 'color': '118040'},
]


def test_straights():
    for straight in straights:
        st = StraightTrack(straight['length'])
        st.label = straight['label']
        st.style.fill_color = BBStyle.RGBFromHex(straight['color'])
        st.part.descriptions['en'] = "Straight track %d studs long" % straight['length']
        st.WritePNG(OUTPUT_PATH + straight['label'] + ".72.png")
        st.to_xml(OUTPUT_PATH + straight['label'] + ".72.xml")

def test_curves():
    for curve in curves:
        st = CurveTrack(curve['radius'], curve['sector'])
        st.label = curve['label']
        st.style.fill_color = BBStyle.RGBFromHex(curve['color'])
        st.part.descriptions['en'] = "Curve track %d stud radius, %.2f deg sector" % (curve['radius'], curve['sector'])
        st.WritePNG(OUTPUT_PATH + curve['label'] + ".72.png")
        st.to_xml(OUTPUT_PATH + curve['label'] + ".72.xml")
