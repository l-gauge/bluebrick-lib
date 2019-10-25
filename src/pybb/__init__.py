"""pybb - Package for generating Bluebrick track library parts"""

import os

__project__ = 'pybb'
__version__ = '0.1.0'

VERSION = __project__ + '-' + __version__

script_dir = os.path.dirname(__file__)




from .bbhelpers import *
from .bbpart import BBConnexion, BBPart
from .track import Track
from .track_crossing import CrossingTrack
from .track_curve import CurveTrack
from .track_straight import StraightTrack
from .track_switch import SwitchTrack
