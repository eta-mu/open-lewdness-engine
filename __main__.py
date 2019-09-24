import pygame
import sys
import os
import time
import random
import lxml.etree as ET
import Globals
Globals.init()
from UIElements import *
from DataStructures import *


class App:
	def __init__(self):
		self._running = True
		self._game_display_surf = None
		self.clock = pygame.time.Clock()
		self.targetFrameTime = 1000/Globals.FPS
		self.size = self.display_width, self.display_height = 800, 600
		
		self._story = '' # Root node of the story xml tree
		self._page = '' # Page currently being displayed
	
	
	def on_init(self):
		"""Initialize all PyGame modules, read in files, and load the first page."""
		# Read in the game settings
		self.readSettings()
		
		# Read in the global stats
		self.readStats()

		# Instantiate the player character from the save file
		Globals.PLAYER_CHARACTER = Character(os.path.join(Globals.SAVES_PATH, 'savedata.xml'), Globals.STATS_DICT)
		
		# Initialize game components
		pygame.init()
		self._game_display_surf = pygame.display.set_mode((self.display_width, self.display_height))
		pygame.font.init()
		pygame.display.set_caption('OpenLewdEngine')
		self._running = True
		
		# Set up the first page
		self.turnPage('start', self.display_width, self.display_height)
	
	
	def on_event(self, event):
		"""Handles all PyGame events."""
		if event.type == pygame.QUIT:
			self._running = False
		elif event.type == Globals.NEWPAGE:
			# TODO: modify the event to include metadata to indicate type of page
			# This for loop modifies the exposed variables to the values indicated by the event dictionary's key-value pairs.
			for eventKey, eventValue in event.dict.items():
				# The "name" key is always reserved for the name of the event, so it can be skipped.
				if eventKey != 'name':
					for exposedKey, exposedValue in Globals.EXPOSED_VARIABLES.items():
						if eventKey == exposedKey:
							Globals.EXPOSED_VARIABLES[exposedKey] = eventValue
			# This if-tree either turns the page or loads a new story.
			if event.name.find('.xml') == -1:
				self.turnPage(event.name, self.display_width, self.display_height)
			else:
				self.readStory(event.name, self.display_width, self.display_height)
		elif event.type == Globals.SAVE:
			#TEST\/
			Globals.PLAYER_CHARACTER._addStat('NEWSTAT', '9999')
			Globals.PLAYER_CHARACTER._addStat('Strength', '10', override=True)
			Globals.PLAYER_CHARACTER._addStat('TWOSTAT', 8888)
			#TEST^
			self.saveGame(os.path.join(Globals.SAVES_PATH, 'savedata.xml'))
		else:
		#if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, SCROLLEVENT):
			self._page.handleEvent(event)
	
	
	def on_loop(self):
		"""Executes one full cycle of the game loop."""
		self.on_render()
		self.clock.tick()
		timeDif = self.targetFrameTime - self.clock.get_rawtime()
		if timeDif > 0:
			pygame.time.wait(int(timeDif))
	
	
	def on_render(self):
		"""Renders the game elements."""
		self._game_display_surf.fill(Globals.BLACK)  # Black out the whole display to prevent ghosting.
		self._page.draw(self._game_display_surf)  # Redraw all elements on the screen.
		pygame.display.update()
	
	
	def on_cleanup(self):
		"""Executes all necessary final orders before quitting."""
		pygame.quit()
	
	
	def on_execute(self):
		"""Tries to initalize the game, then manages the game loop, finally cleans up."""
		if self.on_init() == False:
			self._running = False
		
		# Start the clock.
		self.clock.tick()
		
		# The Game Loop:
		while(self._running):
			self.on_loop()
			for event in pygame.event.get():
				self.on_event(event)
		
		self.on_cleanup()
	
	
	def turnPage(self, pageName, gameWidth, gameHeight):
		"""Function for changing to a different Page within a Story.  Also hard-defines which kinds of pages can be created."""
		storyRoot = self._story.getroot()
		for page in storyRoot.findall('page'):
			if page.attrib['name'] == pageName:
				if page.attrib['type'] == 'text':
					self._page = StoryPage(page, storyRoot, gameWidth, gameHeight)
					self._game_display_surf.fill(Globals.BLACK)
				elif page.attrib['type'] == 'menu':
					self._page = MenuPage(page, storyRoot, gameWidth, gameHeight)
					self._game_display_surf.fill(Globals.BLACK)
				elif page.attrib['type'] == 'duel':
					self._page = DuelPage(page, storyRoot, gameWidth, gameHeight)
					self._game_display_surf.fill(Globals.BLACK)
	
	
	def readStory(self, storyName, gameWigth, gameHeight):
		"""Function for changing to (and displaying) a different Story file."""
		try:
			self._story = ET.parse(os.path.join(Globals.STORY_PATH, storyName), Globals.PARSER)
		except IOError as err:
			print("IOError: Cannot find or open {0}!  Error: {1}".format(storyName, err))
			
		self.turnPage('start', self.display_width, self.display_height)
	
	
	def readSettings(self):
		"""Read in Settings.XML during startup."""
		# Reads in the settings file
		try:
			tree = ET.parse(Globals.SETTINGS_PATH, Globals.PARSER)
		except IOError as err:
			print("IOError: Cannot find or open Settings.XML!  Error: {0}".format(err))
			
		root = tree.getroot()
		
		# Find and assign the window widths and heights
		for window in root.findall('window'):
			if window.find('active').text == "True":
				self.display_width = int(window.find('width').text)
				self.display_height = int(window.find('height').text)
				self.size = self.display_width, self.display_height
		
		# Prepare font paths for UI elements to use
		for font in root.findall('font'):
			if font.attrib['variant'] == 'regular':
				Globals.FONT_PATH_REGULAR = os.path.join(Globals.FONT_PATH, font.text)
			elif font.attrib['variant'] == 'italic':
				Globals.FONT_PATH_ITALIC = os.path.join(Globals.FONT_PATH, font.text)
			elif font.attrib['variant'] == 'bold':
				Globals.FONT_PATH_BOLD = os.path.join(Globals.FONT_PATH, font.text)
		
		# Set up the story XML from the file indicated by Settings.XML
		for story in root.findall('story'):
			try:
				self._story = ET.parse(os.path.join(Globals.STORY_PATH, story.find('filename').text), Globals.PARSER)
			except IOError as err:
				print("IOError: Cannot find or open {0}!  Error: {1}".format(storyName, err))
	
	
	def readStats(self):
		"""Read all XML stats lists in from the Stats folder, and put them in the stats dict."""
		# Find the files in _STATS_PATH
		files = []
		try:
			for (dirpath, dirnames, filenames) in os.walk(Globals.STATS_PATH):
				files.extend(filenames)
		except:
			print("Cannot get filenames in directory [0]".format(Globals.STATS_PATH))

		# For each file found, read in the stats
		for statblock in files:
			try:
				tree = ET.parse(os.path.join(Globals.STATS_PATH, statblock), Globals.PARSER)
			except IOError as err:
				print("File {0} was found, but is not parseable".format(statblock))
			
			root = tree.getroot()
			for stat in root.findall('stat'):
				#print(stat.attrib['name'])
				if 'display' in stat.keys():
					if stat.attrib['display'] == 'yes':
						Globals.STATS_DICT[stat.attrib['name']] = [0, True]
					else:
						Globals.STATS_DICT[stat.attrib['name']] = [0, False]
	

	def saveGame(self, filePath):
		"""Write one XML save file, containing the player character data and the larger
		game state, into Saves folder."""
		print('Saving...')
		Globals.PLAYER_CHARACTER._writeSave(filePath)
		print('...saved!')


if __name__ == "__main__":
	theApp = App()
	theApp.on_execute()
	