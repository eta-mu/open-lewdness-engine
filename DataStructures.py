import pygame
from pygame.locals import *
import os
import lxml.etree as ET
import Globals
import UIElements

TEXTIN = pygame.USEREVENT + 3

class Page:
	"""
	The class for displaying an in-game screen.

	Args:
		page:				An XML tree containing the information which is to be represented on the screen.  TODO: Consider replacing this arg with a search of the story variable.
		story:				The full XML tree.  Passed in to this class so that Points can be found and filled with variables.
		exposedVariables:	A global dictionary of all exposed variables which can be referenced across the whole game.
		gameWidth:			An integer denoting the width of the game window.
		gameHeight:			An integer denoting the height of the game window.
		fontPathReg:			The directroy path for the regular in-game font.
		fontPathIta:			The directroy path for the italic in-game font.
		fontPathBol:			The directroy path for the bold in-game font.
		fontSize:				An integer denoting the generic font size.

	Returns:
		nothing

	Raises:
		nothing
	"""
	
	def __init__(self, page, story, gameWidth, gameHeight):
		self.name = page.attrib
		self.game_width = gameWidth
		self.game_height = gameHeight
		if Globals.FONT_PATH_REGULAR == None: print('WARNING BAD FONT PATH')
		self.paragraphs = []
		self.action_buttons = []
		self.progress_bars = []
		self.text_input_box = []
		self.images = []
	
	def handleEvent(self, eventObj):
		if eventObj.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, Globals.SCROLLEVENT):
			for button in self.action_buttons:
				button.handleEvent(eventObj)
			self.scroll_box.handleEvent(eventObj)
		for box in self.text_input_box:
			box.handleEvent(eventObj)
	
	def printPage():
		"""Print out a transcript of the text in the scroll box on the page."""
		print(self.paragraphs)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class DuelPage(Page):
	"""
	The class for displaying the card game mechanics.

	Args:
		page:				An XML tree containing the information which is to be represented on the screen.  TODO: Consider replacing this arg with a search of the story variable.
		story:				The full XML tree.  Passed in to this class so that Points can be found and filled with variables.
		exposedVariables:	A global dictionary of all exposed variables which can be referenced across the whole game.
		gameWidth:			An integer denoting the width of the game window.
		gameHeight:			An integer denoting the height of the game window.
		fontPathReg:			The directroy path for the regular in-game font.
		fontPathIta:			The directroy path for the italic in-game font.
		fontPathBol:			The directroy path for the bold in-game font.
		fontSize:				An integer denoting the generic font size.

	Returns:
		nothing

	Raises:
		nothing
	"""
	
	def __init__(self, page, story, gameWidth, gameHeight):
		Page.__init__(self, page, story, gameWidth, gameHeight)
		self.checkInput = False	 # Flag to avoid checking for text input if no input is requested.
		
		# This is a dictionary containing the exact placement of potential cards.
		# I hate this implementation even more, and it must be fixed TODO.
		self._HAND = {
			'1': pygame.Rect(
				self.game_width * (1 / 2) - self.game_width * (4 / 50),
				self.game_height * (16 / 24),
				64,
				89
				)
		}

		self.cards = [UIElements.OLECard(self._HAND['1'], "Test Card")]
	
	def draw(self, gameDisplay):
		"""Invoke the draw command for each element present on the page."""
		# Draw the buttons
		for card in self.cards:
			card.draw(gameDisplay)
	
	def handleEvent(self, eventObj):
		if eventObj.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, Globals.SCROLLEVENT):
			for card in self.cards:
				card.handleEvent(eventObj)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class MenuPage(Page):
	"""
	The class for displaying an out-of-game menu.

	Args:
		page:				An XML tree containing the information which is to be represented on the screen.  TODO: Consider replacing this arg with a search of the story variable.
		story:				The full XML tree.  Passed in to this class so that Points can be found and filled with variables.
		exposedVariables:	A global dictionary of all exposed variables which can be referenced across the whole game.
		gameWidth:			An integer denoting the width of the game window.
		gameHeight:			An integer denoting the height of the game window.
		fontPathReg:			The directroy path for the regular in-game font.
		fontPathIta:			The directroy path for the italic in-game font.
		fontPathBol:			The directroy path for the bold in-game font.
		fontSize:				An integer denoting the generic font size.

	Returns:
		nothing

	Raises:
		nothing
	"""
	
	def __init__(self, page, story, gameWidth, gameHeight):
		Page.__init__(self, page, story, gameWidth, gameHeight)
		self.checkInput = False	# Flag to avoid checking for text input if no input is requested.
		
		# This is a dictionary containing the exact placement of potential buttons.  I hate this implementation.
		self._BUTTON_DIRECTORY = {
			'1': pygame.Rect(
				self.game_width * (1 / 2) - self.game_width * (4 / 50),
				self.game_height * (10 / 24),
				self.game_width * (8 / 50),
				self.game_height * (4 / 50)
				),
			'2': pygame.Rect(
				self.game_width * (1 / 2) - self.game_width * (4 / 50),
				self.game_height * (13 / 24),
				self.game_width * (8 / 50),
				self.game_height * (4 / 50)
				),
			'3': pygame.Rect(
				self.game_width * (1 / 2) - self.game_width * (4 / 50),
				self.game_height * (16 / 24),
				self.game_width * (8 / 50),
				self.game_height * (4 / 50)
				),
			'4': pygame.Rect(
				self.game_width * (1 / 2) - self.game_width * (4 / 50),
				self.game_height * (19 / 24),
				self.game_width * (8 / 50),
				self.game_height * (4 / 50)
				)
		}
		
		# Read all buttons into action_buttons.
		for b in page.findall('button'):
			if b.find('transition').text == 'quitgame':
				self.action_buttons.append(UIElements.OLEButton(self._BUTTON_DIRECTORY[b.find('location').text],
																						b.find('message').text,
																						font=pygame.font.Font(Globals.FONT_PATH_REGULAR, Globals.FONT_SIZE),
																						event=pygame.event.Event(QUIT)
																						))
			elif b.find('transition').text == 'savegame':
				self.action_buttons.append(UIElements.OLEButton(self._BUTTON_DIRECTORY[b.find('location').text],
																						b.find('message').text,
																						font=pygame.font.Font(Globals.FONT_PATH_REGULAR, Globals.FONT_SIZE),
																						event=pygame.event.Event(Globals.SAVE)
																						))
			else:
				self.action_buttons.append(UIElements.OLEButton(self._BUTTON_DIRECTORY[b.find('location').text],
																						b.find('message').text,
																						font=pygame.font.Font(Globals.FONT_PATH_REGULAR, Globals.FONT_SIZE),
																						event=pygame.event.Event(Globals.NEWPAGE, {'name':b.find('transition').text})
																						))
	
	def draw(self, gameDisplay):
		"""Invoke the draw command for each element present on the page."""
		# Draw the buttons
		for button in self.action_buttons:
			button.draw(gameDisplay)
	
	def handleEvent(self, eventObj):
		if eventObj.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, Globals.SCROLLEVENT):
			for button in self.action_buttons:
				button.handleEvent(eventObj)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class StoryPage(Page):
	"""
	The class for displaying an in-game text or dialog screen.

	Args:
		page:				An XML tree containing the information which is to be represented on the screen.  TODO: Consider replacing this arg with a search of the story variable.
		story:				The full XML tree.  Passed in to this class so that Points can be found and filled with variables.
		exposedVariables:	A global dictionary of all exposed variables which can be referenced across the whole game.
		gameWidth:			An integer denoting the width of the game window.
		gameHeight:			An integer denoting the height of the game window.
		fontPathReg:			The directroy path for the regular in-game font.
		fontPathIta:			The directroy path for the italic in-game font.
		fontPathBol:			The directroy path for the bold in-game font.
		fontSize:				An integer denoting the generic font size.

	Returns:
		nothing

	Raises:
		nothing
	"""
	
	def __init__(self, page, story, gameWidth, gameHeight):
		Page.__init__(self, page, story, gameWidth, gameHeight)
		self.checkInput = False	# Flag to avoid checking for text input if no input is requested.
		
		# This is the precise rectangular space given to the scroll box.
		self.scroll_box_rect = pygame.Rect(self.game_width * (7 / 32), 16, int(self.game_width * (5 / 8)), self.game_height - (self.game_height * (1 / 16)))
		
		# This is the space given to the text input box.
		self.input_box_rect = pygame.Rect(self.game_width * (8 / 32), self.game_height * (15 / 16), int(self.game_width * (18 / 32)), 48)
		
		# This is a dictionary containing the exact placement of potential buttons.  I hate this implementation.
		self._BUTTON_DIRECTORY = {
			'1': pygame.Rect(
				self.scroll_box_rect.right + self.game_width * (1 / 200),
				self.game_height * (1 / 50),
				self.game_width * (97 / 100) - self.scroll_box_rect.right + self.game_width * (1 / 50),
				self.game_height * (4 / 50)
				),
			'2': pygame.Rect(
				self.scroll_box_rect.right + self.game_width * (1 / 200),
				self.game_height * (6 / 50),
				self.game_width * (97 / 100) - self.scroll_box_rect.right + self.game_width * (1 / 50),
				self.game_height * (4 / 50)
				),
			'3': pygame.Rect(
				self.scroll_box_rect.right + self.game_width * (1 / 200),
				self.game_height * (11 / 50),
				self.game_width * (97 / 100) - self.scroll_box_rect.right + self.game_width * (1 / 50),
				self.game_height * (4 / 50)
				),
			'4': pygame.Rect(
				self.scroll_box_rect.right + self.game_width * (1 / 200),
				self.game_height * (16 / 50),
				self.game_width * (97 / 100) - self.scroll_box_rect.right + self.game_width * (1 / 50),
				self.game_height * (4 / 50)
				)
		}
		
		# TODO: Read external varaibles into the page.
		
		# Parse and prepare the XML paragraphs for display as in-game text.
		self.prepareParagraphs(page, story)
		
		# Create background.
		#self.background = OLEBackground()
		
		# Create scroll box.
		self.scroll_box = UIElements.OLEScrollBox(self.scroll_box_rect, self.paragraphs, Globals.FONT_PATH_REGULAR, fontSize=Globals.FONT_SIZE)
		
		# Read all buttons into action_buttons.
		for b in page.findall('button'):
			if b.find('transition').text == 'quitgame':
				self.action_buttons.append(UIElements.OLEButton(self._BUTTON_DIRECTORY[b.find('location').text],
																						b.find('message').text,
																						font=pygame.font.Font(Globals.FONT_PATH_REGULAR, Globals.FONT_SIZE),
																						event=pygame.event.Event(QUIT)
																						))
			else:
				self.action_buttons.append(UIElements.OLEButton(self._BUTTON_DIRECTORY[b.find('location').text],
																						b.find('message').text,
																						font=pygame.font.Font(Globals.FONT_PATH_REGULAR, Globals.FONT_SIZE),
																						event=pygame.event.Event(Globals.NEWPAGE, {'name':b.find('transition').text})
																						))
		
		# Look for a possible input box, and create it if found.
		input = page.find('input')
		if input is not None:
			variable = input.find('variable')
			if variable is not None:
				self.text_input_box.append(UIElements.OLEInputBox(self.input_box_rect,
																							variable.text,
																							font=pygame.font.Font(Globals.FONT_PATH_REGULAR, Globals.FONT_SIZE),
																							event=pygame.event.Event(Globals.NEWPAGE, {'name':input.find('transition').text})
																							))
				checkInput = True
		
		# Load a progress bar for each stat.
		# There are 8 possible bars.
		maxBars = 8
		bars = 0
		for k, v in Globals.EXPOSED_VARIABLES.items():
			if v[1] == True:
				self.progress_bars.append(UIElements.OLEProgressBar(
					rect=pygame.Rect(
						self.game_width * (1 / 200),
						self.game_height * ((4 + (bars * 7)) / 200),
						self.scroll_box_rect.left - self.game_width * (4 / 50),
						self.game_height * (6 / 100)
					),
					message=k,
					value=int(v[0]),
					fontPath=Globals.FONT_PATH_REGULAR,
					fontSize=14
					))
				bars += 2

	def draw(self, gameDisplay):
		"""Invoke the draw command for each element present on the page."""
		# Draw the scroll box
		self.scroll_box.draw(gameDisplay)
		# Draw the buttons
		for button in self.action_buttons:
			button.draw(gameDisplay)
		# Draw the input box
		for box in self.text_input_box:
			box.draw(gameDisplay)
		# Draw the progress bars
		for bar in self.progress_bars:
			bar.draw(gameDisplay, "n")
	
	def handleEvent(self, eventObj):
		if eventObj.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, Globals.SCROLLEVENT):
			for button in self.action_buttons:
				button.handleEvent(eventObj)
			self.scroll_box.handleEvent(eventObj)
		for box in self.text_input_box:
			box.handleEvent(eventObj)

	def prepareParagraphs(self, page, story):
		"""Read all paragraph text into lists of DataWord objects, ordered from first to last.  Append these lists to the master list self.paragraphs"""
		pages = 0
		more = True
		found = False
		while more == True:
			found = False
			for p in page.findall('paragraph'):
				if int(p.attrib['number']) == pages:
					temp_paragraph_text = p.text.split()
					injected_paragraph_text = self.processPoints(page, story, temp_paragraph_text)
					final_paragraph_text = self.formatTextandPoints(page, injected_paragraph_text)
					self.paragraphs.append(final_paragraph_text)
					pages += 1
					found = True
			if found == False:
				more = False
	
	def processPoints(self, page, story, text):
		"""Take in an unformatted list of strings, and replace all Points with the appropriate sequence of strings.  Return an unformatted list of strings."""
		# TODO: Find a more elegant solution to parsing punctuation
		wordlist = []
		for word in text:
			if (word[0] == '['):
				# If the word is a point, change it.
				if (word[-1] == ']'):
					# No punctuation.
					for point in story.findall('point'):
						if point.attrib['name'] == word[1:-1]:
							variable = point.find('variable')
							if point.find('option') == None:
								# Replace point with raw variable data.
								wordlist.append(Globals.EXPOSED_VARIABLES[variable.text])
							else:
								for option in point.findall('option'):
									# Replace point with correct option's data.
									if option.attrib['name'] == Globals.EXPOSED_VARIABLES[variable.text]:
										wordlist.append(option.text)
				elif (word[-2] == ']'):
					# Yes punctuation.
					for point in story.findall('point'):
						if point.attrib['name'] == word[1:-2]:
							variable = point.find('variable')
							if point.find('option') == None:
								# Replace point with raw variable data.
								wordlist.append(Globals.EXPOSED_VARIABLES[variable.text] + word[-1])
							else:
								for option in point.findall('option'):
									# Replace point with correct option's data.
									if option.attrib['name'] == Globals.EXPOSED_VARIABLES[variable.text]:
										wordlist.append(option.text + word[-1])
			else:
				# If the word is not a point, skip it.
				wordlist.append(word)
		return wordlist
	
	def formatTextandPoints(self, page, text):
		"""Take in an unformatted list of strings.  Return a list of completed DataWord objects.  Find all of the customization tags within the text, remove them, and note their desired effects within each string's respective DataWord."""
		# TODO: Find a further cleaner way to detect and remove formatting tags.
		wordlist = text
		ret_list = []
		word_format = None
		word_underline = None
		word_color = Globals.TEXT_COLOR
		color_dict = {
			'rd': Globals.RED,
			'or': Globals.ORANGE,
			'yl': Globals.YELLOW,
			'gn': Globals.GREEN,
			'bu': Globals.BLUE,
			'ig': Globals.INDIGO,
			'vi': Globals.VIOLET,
			'wh': Globals.WHITE,
			'gy': Globals.GRAY,
			'br': Globals.BROWN
		}
		
		for word in wordlist:
			front_stripped = False
			rear_stripped = False
			temp_word = word
			temp_word_format = None
			temp_word_underline = None
			
			# Strip any leading tags
			while front_stripped == False:
				if len(temp_word) > 0:
					if (temp_word[0] == '*') and (word_format == None):
						word_format = 'italic'
						temp_word_format = word_format
						temp_word = temp_word[1:]
					elif (temp_word[0] == '*') and (word_format == 'italic'):
						word_format = 'bold'
						temp_word_format = word_format
						temp_word = temp_word[1:]
					elif temp_word[0] == '_':
						word_underline = True
						temp_word_underline = word_underline
						temp_word = temp_word[1:]
					elif (temp_word[0] == '{') and len(temp_word) >= 4:
						if temp_word[3] == '}':
							word_color = color_dict[ temp_word[1:3] ]
							temp_word = temp_word[4:]
						else:
							front_stripped = True
					else:
						front_stripped = True
				else:
					front_stripped = True
			
			remove_format = False
			remove_color = False
			# Strip any trailing tags
			while rear_stripped == False:
				if len(temp_word) > 0:
					# Bold case
					if (len(temp_word) >= 3) and (word_format == 'bold'):
						if (temp_word[-2:] == '**'):
							remove_format = True
							temp_word = temp_word[:-2]
						elif (temp_word[-3:-1] == '**'):
							remove_format = True
							temp_word = temp_word[:-3] + temp_word[-1]
						else:
							rear_stripped = True
					# Italic case
					elif (len(temp_word) >= 2) and (word_format == 'italic'):
						if (temp_word[-1:] == '*'):
							remove_format = True
							temp_word = temp_word[:-1]
						elif (temp_word[-2:-1] == '*'):
							remove_format = True
							temp_word = temp_word[:-2] + temp_word[-1]
						else:
							rear_stripped = True
					# Underline case
					elif (len(temp_word) >= 2) and word_underline:
						if temp_word[-1:] == '_':
							remove_format = True
							temp_word = temp_word[:-1]
						elif (temp_word[-2:-1] == '_'):
							remove_format = True
							temp_word = temp_word[:-2] + temp_word[-1]
						else:
							rear_stripped = True
					# Color case
					elif (temp_word[-1:] == '}') and (len(temp_word) >= 4):
						if (temp_word[-3:] == '{/}'):
							remove_color = True
							temp_word = temp_word[:-3]
						else:
							rear_stripped = True
					else:
						rear_stripped = True
				else:
					rear_stripped = True
			
			# Apply formatting tags via creating a DataWord, unless no word remains
			if len(temp_word) > 0:
				if word_format == 'italic':
					data = DataWord(temp_word, pygame.font.Font(Globals.FONT_PATH_ITALIC, Globals.FONT_SIZE), temp_word_underline, word_color)
				elif word_format == 'bold':
					data = DataWord(temp_word, pygame.font.Font(Globals.FONT_PATH_BOLD, Globals.FONT_SIZE), temp_word_underline, word_color)
				else:
					data = DataWord(temp_word, pygame.font.Font(Globals.FONT_PATH_REGULAR, Globals.FONT_SIZE), temp_word_underline, word_color)
				ret_list.append(data)
			if remove_format == True:
				word_format = None
			if remove_color == True:
				word_color = Globals.TEXT_COLOR
		return ret_list

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class ActionPage(Page):
	"""
	The class for displaying an out-of-game menu.

	Args:
		page:				An XML tree containing the information which is to be represented on the screen.  TODO: Consider replacing this arg with a search of the story variable.
		story:				The full XML tree.  Passed in to this class so that Points can be found and filled with variables.
		exposedVariables:	A global dictionary of all exposed variables which can be referenced across the whole game.
		gameWidth:			An integer denoting the width of the game window.
		gameHeight:			An integer denoting the height of the game window.
		fontPathReg:			The directroy path for the regular in-game font.
		fontPathIta:			The directroy path for the italic in-game font.
		fontPathBol:			The directroy path for the bold in-game font.
		fontSize:				An integer denoting the generic font size.

	Returns:
		nothing

	Raises:
		nothing
	"""
	
	def __init__(self, page, story, gameWidth, gameHeight):
		Page.__init__(self, page, story, gameWidth, gameHeight)
		self.checkInput = False									# Flag to avoid checking for text input if no input is requested.

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class DataWord:
	def __init__(self, word, font, underline, color):
		self.word = word
		self.font = font
		self.underline = underline
		self.color = color
		if self.color == None:
			self.color = Globals.TEXT_COLOR
		
		def __str__(self):
			return self.word
		
		def __repr__(self):
			return self.word

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class GameState:
	def __init__(self, playerCharacter):
		self.player = playerCharacter
		self.player_location
		self.active_quests = []
		self.complete_quests = []

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class Character:
	def __init__(self, savePath, globalStats):
		self.name = None
		self.body_parts = []
		self.stats = {}
		self.deck = {}

		self.readSave(savePath)
		#self.loadStats(globalStats)
		
	def readSave(self, savePath):
		"""Read character stats from file into the stats dictionary"""
		root = ET.parse(savePath, Globals.PARSER).getroot()
		
		character = root.find('character')
		self.name = character.attrib['name']
		for stat in character.findall('stat'):
			self.stats[stat.attrib['name']] = stat.text.replace('\n','').replace('\t','')
		
		savedDeck = root.find('deck')
		for card in savedDeck.findall('card'):
			self.deck[card.attrib['name']] = Card(os.path.join(Globals.CARDS_PATH, card.attrib['name'] + '.xml'))
	
	def loadStats(self, globalStats):
		"""Create the list of stats by cross-referencing the save file and global stats"""
		"""TODO: This function bugs out the values in self.stats, and does nothing due to STATS_DICT being unimplemented"""
		temp = {}
		for kg, vg in globalStats.items():
			for k, v in self.stats.items():
				if kg == k:
					temp[kg] = vg
		self.stats = temp

	def _addStat(self, newStatName, newStatValue, override=False):
		"""Append a new stat to the stats dict"""
		if newStatName in self.stats:
			if override == False:
				return False
			else:
				self.stats[newStatName] = str(newStatValue)
				return True
		else:
			self.stats[newStatName] = str(newStatValue)
			return True
	
	def _expose(self, exposedStats):
		"""Add all data from the character into the given dictionary exposedStats"""
		# From name string
		exposedStats['PC Name'] = self.name
		# From the stats dictionary
		for s, v in self.stats.items():
			exposedStats[s] = v
	
	def _writeSave(self, saveFilePath):
		"""Write or overwrite the character stats into the save directory"""
		saveTree = ET.parse(saveFilePath, Globals.PARSER)
		root = saveTree.getroot()
		character = root.find('character')
		character.attrib['name'] = self.name
		print(self.stats)
		
		for stat, value in self.stats.items():
			print(stat, ":", value)
			statExists = False
			for oldStat in character.findall('stat'):
				if oldStat.attrib['name'] == stat:
					statExists = True
					oldStat.text = value
			if statExists == False:
				newStat = character.makeelement('stat', {'name': stat})
				newStat.text = value
				character.append(newStat)

		saveTree.write(saveFilePath, pretty_print=True)
	
		"""
		self.hp
		self.lust
		self.lucidity
		self.corruption
		self.race
		self.gender
		self.height
		self.weight
		self.money = {}
		
		self.strength
		self.endurance
		self.quickness
		self.insight
		self.libido
		self.sexiness
		self.sensitivity
		
		self.treasury
		self.orgone_energy
		self.surreal_energy
		self.psychic_energy
		self.mystic_energy
		
		self.armor
		self.ward
		self.flame_resist
		self.frost_resist
		self.toxic_resist
		
		self.inventory = []
		self.effects = []
		self.primary
		self.secondary
		self.headgear
		self.neckwear
		self.overclothes
		self.gloves
		self.top
		self.bottom
		self.waist
		self.shoes
		self.rings = []
		self.rings_allowed
		""" 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class BodyPart:
	def __init__(self, partsTree = [], partName = '', partsDict = {}):
		if partsTree == []:
			self.name = partName
			self.qualities = partsDict
		else:
			self.name = partsTree.find('name').text
			self.qualities = dict()
			for p in partsTree.findall('qualities'):
				self.qualities[p.attrib] = p.text

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class Card:
	def __init__(self, cardPath = None):
		self._name = None
		self._background = None
		self._flavor_text = None
		self._image = None
		self._red = None
		self._green = None
		self._yellow = None
		self._blue = None
		self._side_effects = None
		
		root = ET.parse(cardPath, Globals.PARSER).getroot()
		card_data = root.find('card')
		if card_data == None:
			raise Exception("No card data found for: " + cardPath)

		self._name = card_data.attrib['name']
		self._background = card_data.find('background')
		self._flavor_text = card_data.find('flavortext')
		self._image = card_data.find('image')
		self._red = card_data.find('red')
		self._green = card_data.find('green')
		self._yellow = card_data.find('yellow')
		self._blue = card_data.find('blue')
		self._side_effects = card_data.find('sideeffects')
		
