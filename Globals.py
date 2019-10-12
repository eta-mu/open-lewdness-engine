import pygame
import sys
import os
import lxml.etree


def init():
	# Global Events
	global SCROLLEVENT
	SCROLLEVENT = pygame.USEREVENT + 1
	global NEWPAGE
	NEWPAGE = pygame.USEREVENT + 2
	global SAVE
	SAVE = pygame.USEREVENT + 3

	# XML Parser
	global PARSER
	PARSER = lxml.etree.XMLParser(remove_blank_text=True)

	# Game Settings
	global FPS
	FPS = 60
	
	# Global Colors
	global BLACK
	BLACK = (0, 0, 0)
	global DARKGRAY
	DARKGRAY = (64, 64, 64)
	global GRAY
	GRAY = (128, 128, 128)
	global LIGHTGRAY
	LIGHTGRAY = (212, 208, 200)
	global WHITE
	WHITE = (255, 255, 255)
	global RED
	RED = (200, 0, 0)
	global BRIGHTRED
	BRIGHTRED = (255, 0, 0)
	global LIGHTRED
	LIGHTRED = (225, 25, 25)
	global PALERED
	PALERED = (255, 200, 200)
	global DIMRED
	DIMRED = (102, 0, 0)
	global DARKRED
	DARKRED = (153, 0, 0)
	global ORANGE
	ORANGE = (200, 100, 0)
	global YELLOW
	YELLOW = (200, 200, 0)
	global GREEN
	GREEN = (0, 200, 0)
	global BRIGHTGREEN
	BRIGHTGREEN = (0, 255, 0)
	global BLUE
	BLUE = (0, 0, 200)
	global INDIGO
	INDIGO = (39, 0, 51)
	global VIOLET
	VIOLET = (139, 0, 255)
	global BROWN
	BROWN = (210, 105, 30)

	# Global Paths
	global CARDS_PATH
	CARDS_PATH = 'Cards'
	global FONT_PATH
	FONT_PATH = 'Fonts'
	global FONT_PATH_REGULAR
	FONT_PATH_REGULAR = ''
	global FONT_PATH_ITALIC
	FONT_PATH_ITALIC = ''
	global FONT_PATH_BOLD
	FONT_PATH_BOLD = ''
	global IMAGE_PATH
	IMAGE_PATH = 'Images'
	global SAVES_PATH
	SAVES_PATH = 'Saves'
	global SETTINGS_PATH
	SETTINGS_PATH = 'Settings.XML'
	global STATS_PATH
	STATS_PATH = 'Stats'
	global STORY_PATH
	STORY_PATH = 'Stories'
	global DIRECTORY
	DIRECTORY = os.path.dirname(__file__)

	# Assorted Globals
	global FONT_SIZE
	FONT_SIZE = 22
	global TEXT_COLOR
	TEXT_COLOR = (0,0,0)
	global BG_COLOR
	BG_COLOR = (212, 208, 200)
	
	global STATS_DICT
	STATS_DICT = {}
	
	# All variables exposed to the Story.  Cannot contain the key "name"
	global EXPOSED_VARIABLES
	EXPOSED_VARIABLES = {}
	global PLAYER_CHARACTER