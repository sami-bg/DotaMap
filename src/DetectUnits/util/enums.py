from enum import Enum, unique
from dataclasses import dataclass


class Locations(Enum):
	"""
	An enumeration class of all the last known locations of players or structures.
	TODO
	"""
	PLAYER_0 = None
	PLAYER_1 = None
	PLAYER_2 = None
	PLAYER_3 = None
	PLAYER_4 = None
	PLAYER_5 = None
	PLAYER_6 = None
	PLAYER_7 = None
	PLAYER_8 = None
	PLAYER_9 = None

	RADIANT = None
	DIRE = None


class HSVColorThreshold:
	def __init__(self, min_value, max_value):
		self.MIN = min_value
		self.MAX = max_value


class Colors(Enum):
	"""
	An enumeration class of all the relevant HSV color ranges on a DotA map for the standard DotA match.
	Contains player colors, radiant and dire building colors.
	Can act as an iterator, but iterate over __members__.items() to a tuple of aliases and values.
	"""
	# ------- Players : (H, S, V) - (0-179, 0-255, 0-255) -------
	# Blue / Player 0
	_PLAYER0_MIN = _BLUE_PLAYER_MIN = (83, 171, 128)
	_PLAYER0_MAX = _BLUE_PLAYER_MAX = (110, 220, 255)
	# Teal / Player 1
	_PLAYER1_MIN = _TEAL_PLAYER_MIN = (75, 149, 128)
	_PLAYER1_MAX = _TEAL_PLAYER_MAX = (82, 163, 255)
	# Purple / Player 2
	_PLAYER2_MIN = _PURPLE_PLAYER_MIN = (137, 100, 0)
	_PLAYER2_MAX = _PURPLE_PLAYER_MAX = (160, 255, 255)
	# Yellow / Player 3
	_PLAYER3_MIN = _YELLOW_PLAYER_MIN = (27, 200, 0)
	_PLAYER3_MAX = _YELLOW_PLAYER_MAX = (48, 255, 255)
	# Orange / Player 4
	_PLAYER4_MIN = _ORANGE_PLAYER_MIN = (12, 63, 152)
	_PLAYER4_MAX = _ORANGE_PLAYER_MAX = (18, 255, 255)
	# Pink / Player 5
	_PLAYER5_MIN = _PINK_PLAYER_MIN = (159, 30, 93)
	_PLAYER5_MAX = _PINK_PLAYER_MAX = (167, 164, 255)
	# Gray / Player 6
	_PLAYER6_MIN = _GRAY_PLAYER_MIN = (31, 0, 93)
	_PLAYER6_MAX = _GRAY_PLAYER_MAX = (41, 255, 255)
	# LightBlue / Player 7
	_PLAYER7_MIN = _LIGHTBLUE_PLAYER_MIN = (85, 150, 131)
	_PLAYER7_MAX = _LIGHTBLUE_PLAYER_MAX = (99, 255, 255)
	# Green / Player 8
	_PLAYER8_MIN = _GREEN_PLAYER_MIN = (63, 255, 0)
	_PLAYER8_MAX = _GREEN_PLAYER_MAX = (80, 255, 255)
	# Brown / Player 9
	_PLAYER9_MIN = _BROWN_PLAYER_MIN = (18, 255, 0)
	_PLAYER9_MAX = _BROWN_PLAYER_MAX = (19, 255, 255)
	# Structures
	# Dire Red:
	_TEAM2_MIN = _DIRE_MIN = (0, 200, 0)
	_TEAM2_MAX = _DIRE_MAX = (6, 255, 255)
	# Radiant Green:
	_TEAM1_MIN = _RADIANT_MIN = (53, 200, 0)
	_TEAM1_MAX = _RADIANT_MAX = (64, 255, 255)

	PLAYER_BLUE = HSVColorThreshold(_BLUE_PLAYER_MIN, _BLUE_PLAYER_MAX)
	PLAYER_TEAL = HSVColorThreshold(_TEAL_PLAYER_MIN, _TEAL_PLAYER_MAX)
	PLAYER_PURPLE = HSVColorThreshold(_PURPLE_PLAYER_MIN, _PURPLE_PLAYER_MAX)
	PLAYER_YELLOW = HSVColorThreshold(_YELLOW_PLAYER_MIN, _YELLOW_PLAYER_MAX)
	PLAYER_ORANGE = HSVColorThreshold(_ORANGE_PLAYER_MIN, _ORANGE_PLAYER_MAX)
	PLAYER_PINK = HSVColorThreshold(_PINK_PLAYER_MIN, _PINK_PLAYER_MAX)
	PLAYER_GRAY = HSVColorThreshold(_GRAY_PLAYER_MIN, _GRAY_PLAYER_MAX)
	PLAYER_LIGHTBLUE = HSVColorThreshold(_LIGHTBLUE_PLAYER_MIN, _LIGHTBLUE_PLAYER_MAX)
	PLAYER_GREEN = HSVColorThreshold(_GREEN_PLAYER_MIN, _GREEN_PLAYER_MAX)
	PLAYER_BROWN = HSVColorThreshold(_BROWN_PLAYER_MIN, _BROWN_PLAYER_MAX)
	TEAM_RADIANT = HSVColorThreshold(_RADIANT_MIN, _RADIANT_MAX)
	TEAM_DIRE = HSVColorThreshold(_DIRE_MIN, _DIRE_MAX)

	@classmethod
	def get_all(cls):
		"""
		Returns a list of values of all Color enums contained within the Colors class.
		:return:
		"""
		return [cls.PLAYER_BLUE, cls.PLAYER_TEAL, cls.PLAYER_PURPLE, cls.PLAYER_YELLOW, cls.PLAYER_ORANGE,
				cls.PLAYER_PINK, cls.PLAYER_GRAY, cls.PLAYER_LIGHTBLUE, cls.PLAYER_GREEN, cls.PLAYER_BROWN,
				cls.TEAM_RADIANT, cls.TEAM_DIRE]


@unique
class Objects(Enum):
	"""
	An enumeration class of all the map objects (structures, hero icons, etc.)
	Contains color information in the Colors hidden class and approximate location information in the location hidden
	class.
	"""
	# Each enumeration contains data on the colors and approximate location. For players, approximate location is
	#  based off of their location in the last frame (implement this later or something).

	PLAYER_BLUE = (Locations.PLAYER_0, Colors.PLAYER_BLUE)
	PLAYER_TEAL = (Locations.PLAYER_1, Colors.PLAYER_TEAL)
	PLAYER_PURPLE = (Locations.PLAYER_2, Colors.PLAYER_PURPLE)
	PLAYER_YELLOW = (Locations.PLAYER_3, Colors.PLAYER_YELLOW)
	PLAYER_ORANGE = (Locations.PLAYER_4, Colors.PLAYER_ORANGE)
	PLAYER_PINK = (Locations.PLAYER_5, Colors.PLAYER_PINK)
	PLAYER_GRAY = (Locations.PLAYER_6, Colors.PLAYER_GRAY)
	PLAYER_LIGHTBLUE = (Locations.PLAYER_7, Colors.PLAYER_LIGHTBLUE)
	PLAYER_GREEN = (Locations.PLAYER_8, Colors.PLAYER_GREEN)
	PLAYER_BROWN = (Locations.PLAYER_9, Colors.PLAYER_BROWN)

	RADIANT = (Locations.DIRE, Colors.TEAM_RADIANT)
	DIRE = (Locations.RADIANT, Colors.TEAM_DIRE)
