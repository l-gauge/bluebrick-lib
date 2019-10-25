# system modules
import math, os.path
import sys
import pytest
from math import pi

# my modules
from pybb import *

SCR_PATH = os.path.dirname(os.path.realpath(__file__))
OUT_PATH = os.path.normpath(SCR_PATH + os.path.sep + "../LGauge")
COLOR_PATH = os.path.normpath(OUT_PATH + os.path.sep + "color")
MONO_PATH = os.path.normpath(OUT_PATH + os.path.sep + "mono")
sys.path.append(SCR_PATH)
sys.path.append(OUT_PATH)

straights = [
  {'label': 'S1.6', 'length': 1.6, 'color': '606060'},
  {'label': 'S4', 'length': 4, 'color': '606060'},
  {'label': 'S8', 'length': 8, 'color': '606060'},
  {'label': 'S16', 'length': 16, 'color': '606060'},
  {'label': 'S32', 'length': 32, 'color': '606060'},
]

curves = [
  {'label': 'R40', 'radius': 40, 'sector': 22.5, 'color': 'FB0207'},
  {'label': 'R40.5', 'radius': 40, 'sector': 11.25, 'color': 'FB0207'},
  {'label': 'R56', 'radius': 56, 'sector': 22.5, 'color': '800002'},
  {'label': 'R64P', 'radius': 64, 'sector': 22.62, 'color': 'FD8008'},
  {'label': 'R72', 'radius': 72, 'sector': 22.5, 'color': '804003'},
  {'label': 'R72.5', 'radius': 72, 'sector': 11.25, 'color': '804003'},
  {'label': 'R88', 'radius': 88, 'sector': 11.25, 'color': '118040'},
  {'label': 'R104', 'radius': 104, 'sector': 11.25, 'color': '074080'},
  {'label': 'R120', 'radius': 120, 'sector': 11.25, 'color': '800040'},
  {'label': 'R136', 'radius': 136, 'sector': 11.25, 'color': '400080'},
  {'label': 'R152', 'radius': 152, 'sector': 11.25, 'color': 'DC0972'},
]

switches = [
  {'label': 'P32L', 'length': 32, 'vee': 22.62, 'dir': 'L', 'div': 8, 'color': '191919'},
  {'label': 'P32R', 'length': 32, 'vee': 22.62, 'dir': 'R', 'div': 8, 'color': '191919'},
  {'label': 'P40L', 'length': 40, 'vee': 22.62, 'dir': 'L', 'div': 0, 'color': '191919'},
  {'label': 'P40R', 'length': 40, 'vee': 22.62, 'dir': 'R', 'div': 0, 'color': '191919'},
]

def ConvertToGIF(filename):
    cmd = "convert " + filename + ".png " + filename + ".gif"
    res = os.system(cmd)
    cmd = "rm " + filename + ".png"
    res = os.system(cmd)

def write_files(track, out_path):
    track.WritePNG(out_path + ".png")
    track.to_xml(out_path + ".xml")
    ConvertToGIF(out_path)

for straight in straights:
    t = StraightTrack(straight['length'])
    if straight['length'] < 8:
        t.style.set_text_height(3.0)
    if straight['length'] < 4:
        t.style.set_text_height(2.0)
    t.label = straight['label']
    t.style.fill_color = BBStyle.RGBFromHex(straight['color'])
    t.part.descriptions['en'] = "%s straight track" % straight['label']
    t.colour = 72
    fn = COLOR_PATH + os.path.sep + straight['label'] + ".72"
    write_files(t, fn)

    t.style.SetMono()
    t.colour = 15
    fn = MONO_PATH + os.path.sep + straight['label'] + ".15"
    write_files(t, fn)

for curve in curves:
    t = CurveTrack(curve['radius'], curve['sector'])
    t.label = curve['label']
    if '40.5' in curve['label']:
        t.style.set_text_height(2.75)
    t.style.fill_color = BBStyle.RGBFromHex(curve['color'])
    t.part.descriptions['en'] = "%s curve track, %.2f deg sector" % (curve['label'], curve['sector'])
    fn = COLOR_PATH + os.path.sep + curve['label'] + ".72"
    t.colour = 72
    write_files(t, fn)

    t.style.SetMono()
    t.colour = 15
    fn = MONO_PATH + os.path.sep + curve['label'] + ".15"
    write_files(t, fn)

for switch in switches:
    t = SwitchTrack(switch['length'], switch['vee'], switch['dir'])
    t.label = switch['label']
    t.style.fill_color = BBStyle.RGBFromHex(switch['color'])
    t.part.descriptions['en'] = "Switch track %d studs long, %.2f deg diverging" % (switch['length'], switch['vee'])
    fn = COLOR_PATH + os.path.sep + switch['label'] + ".72"
    t.colour = 72
    write_files(t, fn)

    t.style.SetMono()
    t.colour = 15
    fn = MONO_PATH + os.path.sep + switch['label'] + ".15"
    write_files(t, fn)
