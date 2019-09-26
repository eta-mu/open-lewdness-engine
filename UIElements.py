import os
import pygame
from pygame.locals import *
import Globals
import DataStructures

SCROLLEVENT = pygame.USEREVENT + 1

pygame.font.init()

SCROLLBARWIDTH = 16
LINESPACING = 1
LINEINDENT = 6
SCROLLSPEED = 16


class OLEButton(object):
	"""
	The class for an in-game button.

	Args:
		rect:			The pygame rectangle which defines the physical space the button takes up on the game screen.
		message:	The display text on the button.
		bgcolor:	The background color of the button.
		fgcolor:		The foreground color of the button.
		font:			The intended font of the display text in "message"
		action:		An optional value for passing a non-specific function to the button, to be executed when the button is clicked.
		event:		An optional value for passing a pygame event, to be raised when the button is clicked.  Used largely for turning the page.
		normal:		An optional value for passing an image to be rendered as the button's typical-state texture.
		highlight:	An optional value for passing an image to be rendered as the button's highlighted-state texture.
		down:		An optional value for passing an image to be rendered as the button's just-clicked-state texture.

	Returns:
		nothing

	Raises:
		Executes the function passed in via "action"
		OR
		The event passsed in via "event", if "action" is not present
	"""
	def __init__(self, rect=None, message='', bgcolor=Globals.LIGHTGRAY, fgcolor=Globals.BLACK, font=None, action=None, event=None, normal=None, highlight=None, down=None):
		if rect is None:
			self._rect = pygame.Rect(0, 0, 30, 60)
		else:
			self._rect = pygame.Rect(rect)
		
		self._message = message
		self._bgcolor = bgcolor
		self._fgcolor = fgcolor
		
		if font is None:
			self._font = pygame.font.Font('freesansbold.ttf', 14)
		else:
			self._font = font
		
		# Tracks the state of the button.
		self.buttonDown = False # Is the button currently pushed down?
		self.mouseOverButton = False # Is the mouse currently hovering over the button?
		self.lastMouseDownOverButton = False # Was the last mouse down event over the mouse button? (Used to track clicks.)
		self._visible = True # Is the button visible?
		self.customSurfaces = False # Does the button start as a text button instead of having custom images for each surface?
		
		self._action = action
		self._event = event
		
		if normal is None:
			# Create the surfaces for a text button.
			self.surfaceNormal = pygame.Surface(self._rect.size)
			self.surfaceDown = pygame.Surface(self._rect.size)
			self.surfaceHighlight = pygame.Surface(self._rect.size)
			self._update() # draw the initial button images
		else:
			# create the surfaces for a custom image button
			self.setSurfaces(normal, down, highlight)
	
	def setSurfaces(self, normalSurface, downSurface=None, highlightSurface=None):
		"""Switch the button to a custom image type of button (rather than a text button). You can specify either a pygame.Surface object or a string of a filename to load for each of the three button appearance states."""
		if downSurface is None:
			downSurface = normalSurface
		if highlightSurface is None:
			highlightSurface = normalSurface
		
		if type(normalSurface) == str:
			self.origSurfaceNormal = pygame.image.load(normalSurface)
		if type(downSurface) == str:
			self.origSurfaceDown = pygame.image.load(downSurface)
		if type(highlightSurface) == str:
			self.origSurfaceHighlight = pygame.image.load(highlightSurface)
		
		if self.origSurfaceNormal.get_size() != self.origSurfaceDown.get_size() != self.origSurfaceHighlight.get_size():
			raise Exception('foo')
		
		self.surfaceNormal = self.origSurfaceNormal
		self.surfaceDown = self.origSurfaceDown
		self.surfaceHighlight = self.origSurfaceHighlight
		self.customSurfaces = True
		self._rect = pygame.Rect((self._rect.left, self._rect.top, self.surfaceNormal.get_width(), self.surfaceNormal.get_height()))
	
	def _update(self):
		"""Redraw the button's Surface object. Call this method when the button has changed appearance."""
		if self.customSurfaces:
			self.surfaceNormal = pygame.transform.smoothscale(self.origSurfaceNormal, self._rect.size)
			self.surfaceDown = pygame.transform.smoothscale(self.origSurfaceDown, self._rect.size)
			self.surfaceHighlight = pygame.transform.smoothscale(self.origSurfaceHighlight, self._rect.size)
			return
		
		w = self._rect.width # syntactic sugar
		h = self._rect.height # syntactic sugar
		
		# Fill background color for all buttons.
		self.surfaceNormal.fill(self._bgcolor)
		self.surfaceDown.fill(self._bgcolor)
		self.surfaceHighlight.fill(self._bgcolor)

		# Draw message text for all buttons.
		messageSurf = self._font.render(self._message, True, self._fgcolor, self._bgcolor)
		messageRect = messageSurf.get_rect()
		messageRect.center = int(w / 2), int(h / 2)
		self.surfaceNormal.blit(messageSurf, messageRect)
		self.surfaceDown.blit(messageSurf, messageRect)
		self.surfaceHighlight.blit(messageSurf, messageRect)

		# Draw border for normal button.
		pygame.draw.rect(self.surfaceNormal, Globals.BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
		pygame.draw.line(self.surfaceNormal, Globals.WHITE, (1, 1), (w - 2, 1)) # horizontal top
		pygame.draw.line(self.surfaceNormal, Globals.WHITE, (1, 1), (1, h - 2)) # vertical left
		pygame.draw.line(self.surfaceNormal, Globals.DARKGRAY, (1, h - 1), (w - 1, h - 1)) # horizontal bottom
		pygame.draw.line(self.surfaceNormal, Globals.DARKGRAY, (w - 1, 1), (w - 1, h - 1)) # vertical right
		pygame.draw.line(self.surfaceNormal, Globals.GRAY, (2, h - 2), (w - 2, h - 2)) # horizontal bottom
		pygame.draw.line(self.surfaceNormal, Globals.GRAY, (w - 2, 2), (w - 2, h - 2)) # vertical right

		# Draw border for down button.
		pygame.draw.rect(self.surfaceDown, Globals.BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
		pygame.draw.line(self.surfaceDown, Globals.WHITE, (1, 1), (w - 2, 1)) # horizontal top
		pygame.draw.line(self.surfaceDown, Globals.WHITE, (1, 1), (1, h - 2)) # vertical left
		pygame.draw.line(self.surfaceDown, Globals.DARKGRAY, (1, h - 2), (1, 1)) # horizontal bottom
		pygame.draw.line(self.surfaceDown, Globals.DARKGRAY, (1, 1), (w - 2, 1)) # vertical right
		pygame.draw.line(self.surfaceDown, Globals.GRAY, (2, h - 3), (2, 2)) # horizontal bottom
		pygame.draw.line(self.surfaceDown, Globals.GRAY, (2, 2), (w - 3, 2)) # vertical right

		# Draw border for highlight button.
		pygame.draw.rect(self.surfaceHighlight, Globals.BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
		pygame.draw.line(self.surfaceHighlight, Globals.WHITE, (1, 1), (w - 2, 1)) # horizontal top
		pygame.draw.line(self.surfaceHighlight, Globals.WHITE, (2, 2), (w - 2, 2)) # horizontal top
		pygame.draw.line(self.surfaceHighlight, Globals.WHITE, (1, 1), (1, h - 2)) # vertical left
		pygame.draw.line(self.surfaceHighlight, Globals.WHITE, (2, 2), (2, h - 2)) # vertical left
		pygame.draw.line(self.surfaceHighlight, Globals.DARKGRAY, (1, h - 1), (w - 1, h - 1)) # horizontal bottom
		pygame.draw.line(self.surfaceHighlight, Globals.DARKGRAY, (w - 1, 1), (w - 1, h - 1)) # vertical right
		pygame.draw.line(self.surfaceHighlight, Globals.GRAY, (2, h - 2), (w - 2, h - 2)) # horizontal bottom
		pygame.draw.line(self.surfaceHighlight, Globals.GRAY, (3, h - 3), (w - 2, h - 3)) # horizontal bottom
		pygame.draw.line(self.surfaceHighlight, Globals.GRAY, (w - 2, 2), (w - 2, h - 2)) # vertical right
		pygame.draw.line(self.surfaceHighlight, Globals.GRAY, (w - 3, 3), (w - 3, h - 2)) # vertical right
	
	def draw(self, surfaceObj):
		"""Blit the current button's appearance to the surface object."""
		if self._visible:
			if self.buttonDown:
				surfaceObj.blit(self.surfaceDown, self._rect)
			elif self.mouseOverButton:
				surfaceObj.blit(self.surfaceHighlight, self._rect)
			else:
				surfaceObj.blit(self.surfaceNormal, self._rect)
	
	
	def handleEvent(self, eventObj):
		if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self._visible:
			# The button only cares bout mouse-related events (or no events, if it is invisible).
			return []
		
		retVal = []
		
		hasExited = False
		if not self.mouseOverButton and self._rect.collidepoint(eventObj.pos):
			# If mouse has entered the button:
			self.mouseOverButton = True
			self.mouseEnter(eventObj)
			retVal.append('enter')
		elif self.mouseOverButton and not self._rect.collidepoint(eventObj.pos):
			# If mouse had exited the button:
			self.mouseOverButton = False
			hasExited = True # Call mouseExit() later, since we want mouseMove() to be handled before mouseExit().
		
		if self._rect.collidepoint(eventObj.pos):
			# If mouse event happened over the button:
			if eventObj.type == MOUSEMOTION:
				self.mouseMove(eventObj)
				retVal.append('move')
			elif eventObj.type == MOUSEBUTTONDOWN:
				self.buttonDown = True
				self.lastMouseDownOverButton = True
				self.mouseDown(eventObj)
				retVal.append('down')
		else:
			if eventObj.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
				# If an up/down happens off the button, then the next up won't cause mouseClick().
				self.lastMouseDownOverButton = False
		
		# Mouse up is handled whether or not it was over the button
		doMouseClick = False
		if eventObj.type == MOUSEBUTTONUP:
			if self.lastMouseDownOverButton:
				doMouseClick = True
			self.lastMouseDownOverButton = False
			
			if self.buttonDown:
				self.buttonDown = False
				self.mouseUp(eventObj)
				retVal.append('up')
			
			if doMouseClick:
				self.buttonDown = False
				self.mouseClick(eventObj)
				retVal.append('click')
		
		if hasExited:
			self.mouseExit(eventObj)
			retVal.append('exit')
		
		return retVal
	
	def mouseClick(self, event):
		if event.button == 1: # Left click.
			if self._action != None:
				self._action()
			elif self._event != None:
				pygame.event.post(self._event)
	
	def mouseEnter(self, event):
		pass # This class is meant to be overridden.
	
	def mouseExit(self, event):
		pass # This class is meant to be overridden.
	
	def mouseMove(self, event):
		pass # This class is meant to be overridden.
	
	def mouseDown(self, event):
		pass # This class is meant to be overridden.
	
	def mouseUp(self, event):
		pass # This class is meant to be overridden.
	
	def _propGetMessage(self):
		return self._message
	
	def _propSetMessage(self, messageText):
		self.customSurfaces = False
		self._message = messageText
		self._update()
	
	def _propGetRect(self):
		return self._rect
	
	def _propSetRect(self, newRect):
		# Note that changing the attributes of the Rect won't update the button.  You have to re-assign the rect member.
		self._update()
		self._rect = newRect
	
	def _propGetVisible(self):
		return self._visible
	
	def _propSetVisible(self, setting):
		self._visible = setting
	
	def _propGetFgColor(self):
		return self._fgcolor
	
	def _propSetFgColor(self, setting):
		self.customSurfaces = False
		self._fgcolor = setting
		self._update()
	
	def _propGetBgColor(self):
		return self._bgcolor
	
	def _propSetBgColor(self, setting):
		self.customSurfaces = False
		self._bgcolor = setting
		self._update()
	
	def _propGetFont(self):
		return self._font
	
	def _propSetFont(self, setting):
		self.customSurfaces = False
		self._font = setting
		self._update()
	
	message = property(_propGetMessage, _propSetMessage)
	rect = property(_propGetRect, _propSetRect)
	visible = property(_propGetVisible, _propSetVisible)
	fgcolor = property(_propGetVisible, _propSetVisible)
	bgcolor = property(_propGetBgColor, _propSetBgColor)
	font = property(_propGetFont, _propSetFont)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class OLEProgressBar(object):
	"""
	The class for a single-bar horizontal bar graph.

	Args:
		rect:			The pygame rectangle which defines the physical space the graph takes up on the game screen.
		message:	The display text captioning the graph.
		value:		The value for the graph, out of 100.  Displayed numerically on the bar.
		bgcolor:	The background color of the graph.
		fgcolor:		The foreground color of the graph.
		font:			The intended font of the display text in "message", and the number in "value".
		normal:		An optional value for passing an image to be rendered as the graphs's typical-state texture.
		highlight:	An optional value for passing an image to be rendered as the graphs's highlighted-state texture.
		dark:		An optional value for passing an image to be rendered as the graphs's deactivated-state texture.

	Returns:
		nothing

	Raises:
		nothing
	"""
	def __init__(self, rect=None, message='', value=0, bgcolor=Globals.LIGHTGRAY, fgcolor=Globals.BLACK, fontPath=None, fontSize=None, normal=None, highlight=None, dark=None):
		if rect is None:
			self._rect = pygame.Rect(0, 0, 30, 60)
		else:
			self._rect = pygame.Rect(rect)
		
		self._message = message
		self._value = value
		self._bgcolor = bgcolor
		self._fgcolor = fgcolor
		
		# Set font.
		if (fontPath is None) and (fontSize is None):
			self._font = pygame.font.Font('freesansbold.ttf', 12)
			self._fontBig = pygame.font.Font('freesansbold.ttf', 12 + 4)
		elif fontPath is None:
			self._font = pygame.font.Font('freesansbold.ttf', fontSize)
			self._fontBig = pygame.font.Font('freesansbold.ttf', fontSize + 4)
		elif fontSize is None:
			self._font = pygame.font.Font(fontPath, 12)
			self._fontBig = pygame.font.Font(fontPath, 12 + 4)
		else:
			self._font = pygame.font.Font(fontPath, fontSize)
			self._fontBig = pygame.font.Font(fontPath, fontSize + 4)
		
		# Tracks the state of the bar.
		self._visible = True # Is the bar visible?
		self.customSurfaces = False # Does the bar start as a color bar instead of having custom images for each surface?
		
		if normal is None:
			# Create the surfaces for a color bar.
			self.surfaceNormal = pygame.Surface(self._rect.size)
			self.surfaceDark = pygame.Surface(self._rect.size)
			self.surfaceHighlight = pygame.Surface(self._rect.size)
			self._update() # draw the initial bar images
		else:
			# create the surfaces for a custom image bar
			self.setSurfaces(normal, dark, highlight)
	
	def setSurfaces(self, normalSurface, darkSurface=None, highlightSurface=None):
		"""Switch the bar to a custom image type of bar (rather than a text bar). You can specify either a pygame.Surface object or a string of a filename to load for each of the three bar appearance states."""
		if darkSurface is None:
			darkSurface = normalSurface
		if highlightSurface is None:
			highlightSurface = normalSurface
		
		if type(normalSurface) == str:
			self.origSurfaceNormal = pygame.image.load(normalSurface)
		if type(darkSurface) == str:
			self.origsurfaceDark = pygame.image.load(darkSurface)
		if type(highlightSurface) == str:
			self.origSurfaceHighlight = pygame.image.load(highlightSurface)
		
		if self.origSurfaceNormal.get_size() != self.origsurfaceDark.get_size() != self.origSurfaceHighlight.get_size():
			raise Exception('foo')
		
		self.surfaceNormal = self.origSurfaceNormal
		self.surfaceDark = self.origsurfaceDark
		self.surfaceHighlight = self.origSurfaceHighlight
		self.customSurfaces = True
		self._rect = pygame.Rect((self._rect.left, self._rect.top, self.surfaceNormal.get_width(), self.surfaceNormal.get_height()))
	
	def _update(self):
		"""Redraw the bar's Surface object. Call this method when the bar has changed appearance."""
		if self.customSurfaces:
			self.surfaceNormal = pygame.transform.smoothscale(self.origSurfaceNormal, self._rect.size)
			self.surfaceDark = pygame.transform.smoothscale(self.origsurfaceDark, self._rect.size)
			self.surfaceHighlight = pygame.transform.smoothscale(self.origSurfaceHighlight, self._rect.size)
			return
		
		w = self._rect.width # syntactic sugar
		h = self._rect.height-1 # syntactic sugar
		barTopHeight = int(h/2) # Vertical beginning of the bar
		barRightEnd = int(w*self._value/100) # End of the bar on the right side, which slides around
		
		# Fill background color for all bar states.
		self.surfaceNormal.fill(self._bgcolor)
		self.surfaceDark.fill(self._bgcolor)
		self.surfaceHighlight.fill(self._bgcolor)
		
		# Draw message text for all bar states.
		messageSurf = self._font.render(self._message, True, self._fgcolor, self._bgcolor)
		messageRect = messageSurf.get_rect()
		messageRect.midleft = int(w / 20), int(h / 4)
		self.surfaceNormal.blit(messageSurf, messageRect)
		self.surfaceDark.blit(messageSurf, messageRect)
		self.surfaceHighlight.blit(messageSurf, messageRect)
		
		# Draw number text for all bar states
		numberSurf = self._fontBig.render(str(self._value), True, self._fgcolor, self._bgcolor)
		numberRect = numberSurf.get_rect()
		numberRect.midleft = int(w - 24), int(h / 4)
		self.surfaceNormal.blit(numberSurf, numberRect)
		self.surfaceDark.blit(numberSurf, numberRect)
		self.surfaceHighlight.blit(numberSurf, numberRect)
		
		# Draw border for a normal bar.
		pygame.draw.rect(self.surfaceNormal, Globals.RED, pygame.Rect((0, barTopHeight, barRightEnd, barTopHeight)), 0) # progress bar color
		pygame.draw.line(self.surfaceNormal, Globals.LIGHTRED, (0, barTopHeight), (barRightEnd, barTopHeight)) # horizontal bar top
		pygame.draw.line(self.surfaceNormal, Globals.LIGHTRED, (1, barTopHeight+1), (barRightEnd-1, barTopHeight+1)) # horizontal bar top
		pygame.draw.line(self.surfaceNormal, Globals.DARKRED, (0, barTopHeight), (0, h)) # vertical bar left
		pygame.draw.line(self.surfaceNormal, Globals.DARKRED, (1, barTopHeight+1), (1, h-1)) # vertical bar left
		pygame.draw.line(self.surfaceNormal, Globals.DARKRED, (0, h), (barRightEnd, h)) # horizontal bar bottom
		pygame.draw.line(self.surfaceNormal, Globals.DARKRED, (1, h-1), (barRightEnd-1, h-1)) # horizontal bar bottom
		pygame.draw.line(self.surfaceNormal, Globals.LIGHTRED, (barRightEnd, barTopHeight), (barRightEnd, h)) # vertical bar right
		pygame.draw.line(self.surfaceNormal, Globals.LIGHTRED, (barRightEnd-1, barTopHeight), (barRightEnd-1, h-1)) # vertical bar right
		
		# Draw border for a darkened bar.
		pygame.draw.rect(self.surfaceDark, Globals.DARKRED, pygame.Rect((0, barTopHeight, barRightEnd, barTopHeight)), 0) # progress bar color
		pygame.draw.line(self.surfaceDark, Globals.RED, (0, barTopHeight), (barRightEnd, barTopHeight)) # horizontal bar top
		pygame.draw.line(self.surfaceDark, Globals.RED, (0, barTopHeight), (0, h)) # vertical bar left
		pygame.draw.line(self.surfaceDark, Globals.DIMRED, (0, h), (barRightEnd, h)) # horizontal bar bottom
		pygame.draw.line(self.surfaceDark, Globals.DIMRED, (barRightEnd, barTopHeight), (barRightEnd, h)) # vertical bar right
		
		# Draw border for a highlighted bar.
		pygame.draw.rect(self.surfaceHighlight, Globals.LIGHTRED, pygame.Rect((0, barTopHeight, barRightEnd, barTopHeight)), 0) # progress bar color
		pygame.draw.line(self.surfaceHighlight, Globals.PALERED, (0, barTopHeight), (barRightEnd, barTopHeight)) # horizontal bar top
		pygame.draw.line(self.surfaceHighlight, Globals.PALERED, (0, barTopHeight), (0, h)) # vertical bar left
		pygame.draw.line(self.surfaceHighlight, Globals.RED, (0, h), (barRightEnd, h)) # horizontal bar bottom
		pygame.draw.line(self.surfaceHighlight, Globals.RED, (barRightEnd, barTopHeight), (barRightEnd, h)) # vertical bar right
	
	def draw(self, surfaceObj, state = "n"):
		"""Blit the current bar's appearance to the surface object."""
		if self._visible:
			if state == "d": # d for dark
				surfaceObj.blit(self.surfaceDark, self._rect)
			elif state == "h": # h for highlight
				surfaceObj.blit(self.surfaceHighlight, self._rect)
			else: # n for normal, or any other value
				surfaceObj.blit(self.surfaceNormal, self._rect)
	
	def _propGetMessage(self):
		return self._message
	
	def _propSetMessage(self, messageText):
		self.customSurfaces = False
		self._message = messageText
		self._update()
	
	def _propGetValue(self):
		return self._value
	
	def _propSetValue(self, valueNumber):
		self.customSurfaces = False
		self._value = valueNumber
		self._update()
	
	def _propGetRect(self):
		return self._rect
	
	def _propSetRect(self, newRect):
		# Note that changing the attributes of the Rect won't update the button.  You have to re-assign the rect member.
		self._update()
		self._rect = newRect
	
	def _propGetVisible(self):
		return self._visible
	
	def _propSetVisible(self, setting):
		self._visible = setting
	
	def _propGetFgColor(self):
		return self._fgcolor
	
	def _propSetFgColor(self, setting):
		self.customSurfaces = False
		self._fgcolor = setting
		self._update()
	
	def _propGetBgColor(self):
		return self._bgcolor
	
	def _propSetBgColor(self, setting):
		self.customSurfaces = False
		self._bgcolor = setting
		self._update()
	
	def _propGetFont(self):
		return self._font
	
	def _propSetFont(self, setting):
		self.customSurfaces = False
		self._font = setting
		self._update()
	
	message = property(_propGetMessage, _propSetMessage)
	rect = property(_propGetRect, _propSetRect)
	visible = property(_propGetVisible, _propSetVisible)
	fgcolor = property(_propGetVisible, _propSetVisible)
	bgcolor = property(_propGetBgColor, _propSetBgColor)
	font = property(_propGetFont, _propSetFont)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class UIWord(object):
	"""This entire class is depricated, and was never implemented.  It is preserved to show what characteristics a word should posess on-screen."""
	def __init__(self, word, font, size, underline, color):
		self.word = word
		self.fontSize = size
		self.format = format
		self.underline = underline
		self.color = color
		if font == None:
			self._font = pygame.font.Font('font' + '-' + format +'.ttf', size)
		else:
			self._font = pygame.font.Font(None, size)
			
	@property
	def word(self):
		return self.__word
	def fontSize(self):
		return self.__fontSize
	def format(self):
		return self.__format
	def underline(self):
		return self.__underline
	def color(self):
		return self.__color
	def font(self):
		return self.__font

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class OLEScrollBox(object):
	def __init__(self, rect, message, fontPath, fontSize, bgcolor=Globals.LIGHTGRAY, fgcolor=Globals.BLACK, normal=None, scroll=None):
		"""
		if rect is None:
			self._rect = pygame.Rect(0, 0, 30, 60)
		else:
		"""
		# The above is deprecated.  rect is now expected, no default rect.
		self._rect = pygame.Rect(rect)
		
		self._message = message
		self._bgcolor = bgcolor
		self._fgcolor = fgcolor
		
		# Tracks the state of the scroll box.
		self.buttonDown = False # Is the mouse button currently pushed down?
		self.mouseOverButton = False # Is the mouse currently hovering over the button?
		self.lastMouseDownOverButton = False # Was the last mouse down event over the box? (Used to track clicks.)
		self._visible = True # Is the box visible?
		self.customSurfaces = False # Does the box start without a custom background image?
		self._scrolling = False # Does the scroll box need to scroll?
		self._position = 0 # How far up or down is the text scrolled in pixels?
		self._excessTextHeight = 0 # By how many pixels do the lines of text exceed the box's height?
		
		# Generate a font object to use as a spacing and layout reference
		self.font_regular = pygame.font.Font(fontPath, fontSize)
		self.font_big_regular = pygame.font.Font(fontPath, fontSize + 4)
		
		self.font_height = self.font_regular.size('Tp')[1]  # Determine maximum possible height of one line of text.
		self.font_space_width = self.font_regular.size(' ')[0]  # Determine width of a space
		
		# Split message into lines.
		self._lines = self._splitLines(self._message)
		# Determine if the box must be scrollable.
		if len(self._lines) * (self.font_height + LINESPACING) > self._rect.height:
			self._scrolling = True
			self._excessTextHeight = (len(self._lines) * (self.font_height + LINESPACING)) - self._rect.height
		# If so, create a scroll bar.
		if self._scrolling:
			self._scrollBar = OLEScrollBar(self._rect, self)
		
		if normal is None:
			# Create the surfaces for a scroll box.
			self.surfaceNormal = pygame.Surface(self._rect.size)
			self.surfaceScroll = pygame.Surface(self._rect.size)
			self._update() # draw the initial bar images
		else:
			# create the surfaces for a custom image bar
			self.setSurfaces(normal, scroll)
	
	def _splitLines(self, message):
		"""Isolate the DataWords of the paragraph message into lines, so that they can be arranged within the margins of the scroll box."""
		lines = []
		for paragraph in message:
			current_line_length = 0
			current_line = []
			for word in paragraph:
				current_line_length += self.font_space_width
				current_line_length += word.font.size(word.word)[0]
				if current_line_length >= (self._rect.width - LINEINDENT - SCROLLBARWIDTH):
					# If the current line exceeds the margins
					lines.append(current_line)
					current_line_length = word.font.size(word.word)[0]
					current_line = [word]
				else:
					current_line.append(word)
			lines.append(current_line) # Last remaining words appended.
			lines.append([DataStructures.DataWord("", self.font_regular, None, None)])
		return lines
	
	def setSurfaces(self, normalSurface, scrollSurface=None):
		"""Switch the scroll box to a custom background (rather than single color). You can specify either a pygame.Surface object or a string of a filename to load for each of the three background appearance states."""
		if scrollSurface is None:
			scrollSurface = normalSurface
		
		if type(normalSurface) == str:
			self.origSurfaceNormal = pygame.image.load(normalSurface)
		if type(scrollSurface) == str:
			self.origSurfaceScroll = pygame.image.load(scrollSurface)
		
		if self.origSurfaceNormal.get_size() != self.origSurfaceScroll.get_size():
			raise Exception('foo')
		
		self.surfaceNormal = self.origSurfaceNormal
		self.surfaceScroll = self.origSurfaceScroll
		self.customSurfaces = True
		self._rect = pygame.Rect((self._rect.left, self._rect.top, self.surfaceNormal.get_width(), self.surfaceNormal.get_height()))
	
	def _update(self):
		"""Redraw the box's Surface object. Call this method when the box has changed appearance."""
		if self.customSurfaces:
			self.surfaceNormal = pygame.transform.smoothscale(self.origSurfaceNormal, self._rect.size)
			self.surfaceScroll = pygame.transform.smoothscale(self.origSurfaceScroll, self._rect.size)
			return
		
		w = self._rect.width # syntactic sugar
		h = self._rect.height # syntactic sugar
		
		# Fill background color for all box states.
		self.surfaceNormal.fill(self._bgcolor)
		self.surfaceScroll.fill(self._bgcolor)
		
		# Draw message text for all bar states.
		# Each word is blit as an surface individually.
		line_count = 0
		for line in self._lines:
			word_indent = 0
			for word in line:
				message_surface = word.font.render(word.word, True, word.color, self._bgcolor)
				message_rect = message_surface.get_rect()
				message_rect.bottomleft = LINEINDENT + word_indent, int(((self.font_height + LINESPACING) * (line_count + 1)) - self._position)
				
				word_indent += message_surface.get_size()[0] + self.font_space_width
				
				self.surfaceNormal.blit(message_surface, message_rect)
				self.surfaceScroll.blit(message_surface, message_rect)
			line_count += 1
		
		# Draw border for the normal scroll box.
		pygame.draw.line(self.surfaceNormal, Globals.BLACK, (0, 0), (w-1, 0)) # horizontal bar top
		pygame.draw.line(self.surfaceNormal, Globals.BLACK, (0, 0), (0, h-1)) # vertical bar left
		pygame.draw.line(self.surfaceNormal, Globals.BLACK, (0, h-1), (w-1, h-1)) # horizontal bar bottom
		pygame.draw.line(self.surfaceNormal, Globals.BLACK, (w-1, 0), (w-1, h-1)) # vertical bar right
		
		# Draw border for a scrolling bar.
		pygame.draw.line(self.surfaceScroll, Globals.BLACK, (0, 0), (w-1, 0)) # horizontal bar top
		pygame.draw.line(self.surfaceScroll, Globals.BLACK, (0, 0), (0, h-1)) # vertical bar left
		pygame.draw.line(self.surfaceScroll, Globals.BLACK, (0, h-1), (w-1, h-1)) # horizontal bar bottom
		pygame.draw.line(self.surfaceScroll, Globals.BLACK, (w-1, 0), (w-1, h-1)) # vertical bar right
		pygame.draw.line(self.surfaceScroll, Globals.BLACK, (w-SCROLLBARWIDTH, 0), (w-SCROLLBARWIDTH, h)) # vertical line interior right (scroll bar left)
	
	def draw(self, surfaceObj):
		"""Blit the current scroll box's appearance to the surface object."""
		if self._visible:
			if self._scrolling:
				surfaceObj.blit(self.surfaceScroll, self._rect)
			else:
				surfaceObj.blit(self.surfaceNormal, self._rect)
		
		if self._scrolling:
			self._scrollBar.draw(surfaceObj)
	
	def handleEvent(self, eventObj):
		if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, SCROLLEVENT) or not self._visible:
			# The box only cares bout mouse-related events (or no events, if it is invisible).
			return []
		
		retVal = []
		
		hasExited = False
		if not self.mouseOverButton and self._rect.collidepoint(eventObj.pos):
			# If mouse has entered the box:
			self.mouseOverButton = True
			self.mouseEnter(eventObj)
			retVal.append('enter')
		elif self.mouseOverButton and not self._rect.collidepoint(eventObj.pos):
			# If mouse had exited the box:
			self.mouseOverButton = False
			hasExited = True # Call mouseExit() later, since we want mouseMove() to be handled before mouseExit().
		
		if self._rect.collidepoint(eventObj.pos):
			# If mouse event happened over the box:
			if eventObj.type == MOUSEMOTION:
				self.mouseMove(eventObj)
				retVal.append('move')
			elif eventObj.type == MOUSEBUTTONDOWN:
				self.buttonDown = True
				self.lastMouseDownOverButton = True
				self.mouseDown(eventObj)
				retVal.append('down')
		else:
			if eventObj.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
				# If an up/down happens outside the box, then the next up won't cause wheelScroll().
				self.lastMouseDownOverButton = False
		
		# Mouse up is handled whether or not it was over the box.
		dowheelScroll = False
		if eventObj.type == MOUSEBUTTONUP:
			if self.lastMouseDownOverButton:
				dowheelScroll = True
			self.lastMouseDownOverButton = False
			
			if self.buttonDown:
				self.buttonDown = False
				self.mouseUp(eventObj)
				retVal.append('up')
			
			if dowheelScroll:
				self.buttonDown = False
				self.wheelScroll(eventObj)
				retVal.append('scroll')
		
		# Handle events from the scroll bar last.
		if eventObj.type == SCROLLEVENT:
			self.wheelScroll(eventObj)
			retVal.append('scroll')
		
		if hasExited:
			self.mouseExit(eventObj)
			retVal.append('exit')
		
		# Scroll bar events handled after all other events
		if self._scrolling:
			self._scrollBar.handleEvent(eventObj)
			
		return retVal
	
	def wheelScroll(self, event):
		if self._scrolling:
			if event.type == SCROLLEVENT:
				if event.button == 4: # Scroll up.
					self._position = int((event.pos[1] / self._scrollBar.maxPosition) * self._excessTextHeight)
					self._update()
				elif event.button == 5: # Scroll down.
					self._position = int((event.pos[1] / self._scrollBar.maxPosition) * self._excessTextHeight)
					self._update()
				else: # Scroll box doesn't care about anything else.
					pass
			else:
				if event.button == 4: # Scroll up.
					self.scrollUp(SCROLLSPEED)
				elif event.button == 5: # Scroll down.
					self.scrollDown(SCROLLSPEED)
				else: # Scroll box doesn't care about anything else.
					pass
	
	def scrollUp(self, rate):
		if self._position > 0:
			self._position -= rate
		if self._position < 0:
			self._position = 0
		self._scrollBar.position = int(self._scrollBar.maxPosition * (self._position / self._excessTextHeight))
		self._update()
	
	def scrollDown(self, rate):
		if self._position < self._excessTextHeight:
			self._position += rate
		if self._position > self._excessTextHeight:
			self._position = self._excessTextHeight
		self._scrollBar.position = int(self._scrollBar.maxPosition * (self._position / self._excessTextHeight))
		self._update()
	
	def mouseEnter(self, event):
		pass # This class is meant to be overridden.
	
	def mouseExit(self, event):
		pass # This class is meant to be overridden.
	
	def mouseMove(self, event):
		pass # This class is meant to be overridden.
	
	def mouseDown(self, event):
		pass # This class is meant to be overridden.
	
	def mouseUp(self, event):
		pass # This class is meant to be overridden.
	
	def _propGetMessage(self):
		return self._message
	
	def _propSetMessage(self, messageText):
		self.customSurfaces = False
		self._message = messageText
		self._update()
	
	def _propGetRect(self):
		return self._rect
	
	def _propSetRect(self, newRect):
		# Note that changing the attributes of the Rect won't update the button.  You have to re-assign the rect member.
		self._update()
		self._rect = newRect
	
	def _propGetVisible(self):
		return self._visible
	
	def _propSetVisible(self, setting):
		self._visible = setting
	
	def _propGetFgColor(self):
		return self._fgcolor
	
	def _propSetFgColor(self, setting):
		self.customSurfaces = False
		self._fgcolor = setting
		self._update()
	
	def _propGetBgColor(self):
		return self._bgcolor
	
	def _propSetBgColor(self, setting):
		self.customSurfaces = False
		self._bgcolor = setting
		self._update()
	
	def _propGetFont(self):
		return self._font
	
	def _propSetFont(self, setting):
		self.customSurfaces = False
		self._font = setting
		self._update()
	
	def _propGetScrolling(self):
		return self._scrolling
	
	def _propGetPosition(self):
		return self._position
	
	def _propGetFontHeight(self):
		return self.font_height
	
	def _propGetExcessTextHeight(self):
		return self._excessTextHeight
	
	message = property(_propGetMessage, _propSetMessage)
	rect = property(_propGetRect, _propSetRect)
	visible = property(_propGetVisible, _propSetVisible)
	fgcolor = property(_propGetVisible, _propSetVisible)
	bgcolor = property(_propGetBgColor, _propSetBgColor)
	font = property(_propGetFont, _propSetFont)
	scrolling = property(_propGetScrolling)
	position = property(_propGetPosition)
	fontHeight = property(_propGetFontHeight)
	excessTextHeight = property(_propGetExcessTextHeight)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class OLEScrollBar(object):
	def __init__(self, rect, scrollBox=None, bgcolor=Globals.LIGHTGRAY, fgcolor=Globals.BLACK, normal=None, down=None):
		self._position = 0 # How far up or down has the bar scrolled in pixels?
		# Get only relevant parent scroll box properties.
		self._SCROLLBOXHEIGHT = scrollBox.rect.height
		self._SCROLLBOXTOP = scrollBox.rect.top
		self._SCROLLBOXEXCESSTEXTHEIGHT = scrollBox.excessTextHeight
		self._SCROLLBOXLINEHEIGHT = scrollBox.fontHeight + LINESPACING
		
		self._SCROLLBARHEIGHT = 50#self._SCROLLBOXHEIGHT / (self._SCROLLBOXHEIGHT + self._SCROLLBOXEXCESSTEXTHEIGHT)
		
		self._rect = pygame.Rect(rect.right-SCROLLBARWIDTH, rect.top + self._position, SCROLLBARWIDTH, self._SCROLLBARHEIGHT)
		
		self._bgcolor = bgcolor
		self._fgcolor = fgcolor
		
		# Tracks the state of the bar.
		self.buttonDown = False # Is the bar currently pushed down?
		self.mouseOverButton = False # Is the mouse currently hovering over the button?
		self.lastMouseDownOverButton = False # Was the last mouse down event over the mouse button? (Used to track clicks.)
		self._visible = True # Is the bar visible?
		
		self._MAXPOSITION = self._SCROLLBOXHEIGHT - self._SCROLLBARHEIGHT
		
		# Create the surfaces for a scroll bar.
		self.surfaceNormal = pygame.Surface(self._rect.size)
		self.surfaceDown = pygame.Surface(self._rect.size)
		self.surfaceHighlight = pygame.Surface(self._rect.size)
		self._update() # draw the initial button images
	
	def _update(self):
		"""Redraw the bar's Surface object. Call this method when the bar has changed appearance."""
		w = self._rect.width # syntactic sugar
		h = self._rect.height # syntactic sugar
		
		# Re-position the scroll bar button.
		self._rect = pygame.Rect(self._rect.right-SCROLLBARWIDTH, self._SCROLLBOXTOP + self._position, SCROLLBARWIDTH, self._SCROLLBARHEIGHT)
		
		# Fill background color for all bars.
		self.surfaceNormal.fill(self._bgcolor)
		self.surfaceDown.fill(Globals.GRAY)
		self.surfaceHighlight.fill(Globals.WHITE)

		# Draw border for normal button.
		pygame.draw.line(self.surfaceNormal, Globals.DARKGRAY, (0, 0), (w - 1, 0)) # horizontal top
		pygame.draw.line(self.surfaceNormal, Globals.DARKGRAY, (0, 0), (0, h - 2)) # vertical left
		pygame.draw.line(self.surfaceNormal, Globals.DARKGRAY, (0, h - 1), (w - 1, h - 1)) # horizontal bottom
		pygame.draw.line(self.surfaceNormal, Globals.DARKGRAY, (w - 1, 1), (w - 1, h - 1)) # vertical right
		# Three middle lines
		pygame.draw.line(self.surfaceNormal, Globals.GRAY, (3, h/3), (w - 3, h/3)) # horizontal top
		pygame.draw.line(self.surfaceNormal, Globals.GRAY, (3, h/2), (w - 3, h/2)) # horizontal top
		pygame.draw.line(self.surfaceNormal, Globals.GRAY, (3, (2*h)/3), (w - 3, (2*h)/3)) # horizontal top

		# Draw border for down button.
		pygame.draw.line(self.surfaceDown, Globals.DARKGRAY, (0, 0), (w - 1, 0)) # horizontal top
		pygame.draw.line(self.surfaceDown, Globals.DARKGRAY, (0, 0), (0, h - 2)) # vertical left
		pygame.draw.line(self.surfaceDown, Globals.DARKGRAY, (0, h - 1), (w - 1, h - 1)) # horizontal bottom
		pygame.draw.line(self.surfaceDown, Globals.DARKGRAY, (w - 1, 1), (w - 1, h - 1)) # vertical right
		# Three middle lines
		pygame.draw.line(self.surfaceDown, Globals.GRAY, (3, h/3), (w - 3, h/3)) # horizontal top
		pygame.draw.line(self.surfaceDown, Globals.GRAY, (3, h/2), (w - 3, h/2)) # horizontal top
		pygame.draw.line(self.surfaceDown, Globals.GRAY, (3, (2*h)/3), (w - 3, (2*h)/3)) # horizontal top

		# Draw border for highlight button.
		pygame.draw.line(self.surfaceHighlight, Globals.DARKGRAY, (0, 0), (w - 1, 0)) # horizontal top
		pygame.draw.line(self.surfaceHighlight, Globals.DARKGRAY, (0, 0), (0, h - 2)) # vertical left
		pygame.draw.line(self.surfaceHighlight, Globals.DARKGRAY, (0, h - 1), (w - 1, h - 1)) # horizontal bottom
		pygame.draw.line(self.surfaceHighlight, Globals.DARKGRAY, (w - 1, 1), (w - 1, h - 1)) # vertical right
		# Three middle lines
		pygame.draw.line(self.surfaceHighlight, Globals.GRAY, (3, h/3), (w - 3, h/3)) # horizontal top
		pygame.draw.line(self.surfaceHighlight, Globals.GRAY, (3, h/2), (w - 3, h/2)) # horizontal top
		pygame.draw.line(self.surfaceHighlight, Globals.GRAY, (3, (2*h)/3), (w - 3, (2*h)/3)) # horizontal top
	
	def draw(self, surfaceObj):
		"""Blit the current button's appearance to the surface object."""
		if self._visible:
			if self.buttonDown:
				surfaceObj.blit(self.surfaceDown, self._rect)
			elif self.mouseOverButton:
				surfaceObj.blit(self.surfaceHighlight, self._rect)
			else:
				surfaceObj.blit(self.surfaceNormal, self._rect)
	
	def handleEvent(self, eventObj):
		if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self._visible:
			# The button only cares bout mouse-related events (or no events, if it is invisible).
			return []
		
		retVal = []
		
		hasExited = False
		if not self.mouseOverButton and self._rect.collidepoint(eventObj.pos):
			# If mouse has entered the button:
			self.mouseOverButton = True
			self.mouseEnter(eventObj)
			retVal.append('enter')
		elif self.mouseOverButton and not self._rect.collidepoint(eventObj.pos):
			# If mouse had exited the button:
			self.mouseOverButton = False
			hasExited = True # Call mouseExit() later, since we want mouseMove() to be handled before mouseExit().
		
		if self._rect.collidepoint(eventObj.pos):
			# If mouse event happened over the button:
			if eventObj.type == MOUSEMOTION:
				# If a down/move event happens on the button:
				if self.buttonDown == True:
					self.mouseDrag(eventObj)
					retVal.append('drag')
				# Otherwise just say it moves
				else:
					self.mouseMove(eventObj)
					retVal.append('move')
				
			elif eventObj.type == MOUSEBUTTONDOWN:
				self.buttonDown = True
				self.lastMouseDownOverButton = True
				self.mouseDown(eventObj)
				retVal.append('down')
		else:
			if eventObj.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
				# If an up/down happens off the button, then the next up won't cause mouseClick().
				self.lastMouseDownOverButton = False
			if eventObj.type == MOUSEMOTION:
				# If a down/move happens off of the button, keep the drag persisting
				if self.buttonDown == True:
					self.mouseDrag(eventObj)
					retVal.append('drag')
		
		# Mouse up is handled whether or not it was over the button
		doMouseClick = False
		if eventObj.type == MOUSEBUTTONUP:
			if eventObj.button == 1:
				if self.lastMouseDownOverButton:
					doMouseClick = True
				self.lastMouseDownOverButton = False
				
				if self.buttonDown:
					self.buttonDown = False
					self.mouseUp(eventObj)
					retVal.append('up')
				
				if doMouseClick:
					self.buttonDown = False
					self.mouseClick(eventObj)
					retVal.append('click')
		
		if hasExited:
			self.mouseExit(eventObj)
			retVal.append('exit')
		
		return retVal
	
	def mouseDrag(self, event):
		previousPosition = self._position
		if event.type == MOUSEMOTION:
			x, y = event.rel
			self._position += y
			if self._position > self._MAXPOSITION:
				self._position = self._MAXPOSITION
			elif self._position < 0:
				self._position = 0
			
			r = (event.pos[0], self._position)# syntactical sugar, r for relative pos
			
			if previousPosition > self._position:
				pygame.event.post(pygame.event.Event(SCROLLEVENT, {'pos':r,'button':4}))
				pygame.event.post(pygame.event.Event(SCROLLEVENT, {'pos':r,'button':4}))
			elif self._position > previousPosition:
				pygame.event.post(pygame.event.Event(SCROLLEVENT, {'pos':r,'button':5}))
				pygame.event.post(pygame.event.Event(SCROLLEVENT, {'pos':r,'button':5}))
		self._update()
	
	def mouseClick(self, event):
		pass # This class is meant to be overridden.
	
	def mouseEnter(self, event):
		pass # This class is meant to be overridden.
	
	def mouseExit(self, event):
		pass # This class is meant to be overridden.
	
	def mouseMove(self, event):
		pass # This class is meant to be overridden.
	
	def mouseDown(self, event):
		pass # This class is meant to be overridden.
	
	def mouseUp(self, event):
		pass # This class is meant to be overridden.
	
	"""
	@property
		def rect(self):
			return self._rect
		
		def visible(self):
			return self._visible
		
		def.fgColor(self):
			return self._fgcolor
		
		def.bgColor(self):
			return self._bgcolor
		
		def.position(self):
			return self._position
		
		def.maxPosition(self):
			return self._MAXPOSITION
	
	@rect.setter
		def rect(self, newRect):
			# Note that changing the attributes of the Rect won't update the button.  You have to re-assign the rect member.
			self._update()
			self._rect = newRect
	
	@visible.setter
		def visible(self, setting):
		self._visible = setting
	
	@fgColor.setter
		def fgColor(self, setting):
			self._fgcolor = setting
			self._update()
	
	@bgColor.setter
		def bgColor(self, setting):
			self._bgcolor = setting
			self._update()
	
	@position.setter
		def position(self, setting):
			self._position = setting
			self._update()
	
	"""
	
	def _propGetRect(self):
		return self._rect
	
	def _propSetRect(self, newRect):
		# Note that changing the attributes of the Rect won't update the button.  You have to re-assign the rect member.
		self._update()
		self._rect = newRect
	
	def _propGetVisible(self):
		return self._visible
	
	def _propSetVisible(self, setting):
		self._visible = setting
	
	def _propGetFgColor(self):
		return self._fgcolor
	
	def _propSetFgColor(self, setting):
		self._fgcolor = setting
		self._update()
	
	def _propGetBgColor(self):
		return self._bgcolor
	
	def _propSetBgColor(self, setting):
		self._bgcolor = setting
		self._update()
	
	def _propGetPosition(self):
		return self._position
	
	def _propSetPosition(self, setting):
		self._position = setting
		self._update()
	
	def _propGetMaxPosition(self):
		return self._MAXPOSITION
	
	rect = property(_propGetRect, _propSetRect)
	visible = property(_propGetVisible, _propSetVisible)
	fgcolor = property(_propGetVisible, _propSetVisible)
	bgcolor = property(_propGetBgColor, _propSetBgColor)
	position = property(_propGetPosition, _propSetPosition)
	maxPosition = property(_propGetMaxPosition)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -

class OLEBackground(object):
	# TODO: This class
	def __init__(self, rect=None, message='', bgcolor=Globals.LIGHTGRAY, fgcolor=Globals.BLACK, font=None, action=None, event=None, normal=None, highlight=None, down=None):
		if rect is None:
			self._rect = pygame.Rect(0, 0, 30, 60)
		else:
			self._rect = pygame.Rect(rect)
		
		self._message = message
		self._bgcolor = bgcolor
		self._fgcolor = fgcolor
		
		if font is None:
			self._font = pygame.font.Font('freesansbold.ttf', 14)
		else:
			self._font = font
		
		# Tracks the state of the background.
		self._visible = True # Is the background visible?
		self.customSurfaces = False # Does the background start as generic instead of having a custom image?
		
		self._action = action
		self._event = event
		
		if normal is None:
			# Create the surfaces for a text button.
			self.surfaceNormal = pygame.Surface(self._rect.size)
			self.surfaceDown = pygame.Surface(self._rect.size)
			self.surfaceHighlight = pygame.Surface(self._rect.size)
			self._update() # draw the initial button images
		else:
			# create the surfaces for a custom image button
			self.setSurfaces(normal, down, highlight)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -
	
class OLEInputBox(object):
	"""
	The class for a box to input text into.

	Args:
		rect:			The pygame rectangle which defines the physical space the input box takes up on the game screen.
		varString:
		bgcolor:	The background color of the input box.
		fgcolor:		The foreground color of the input box.
		font:			The intended font of the displayed text.
		action:		An optional value for passing a non-specific function to the input box, to be executed when the "Enter" key is pressed.
		eventDict:	An optional value for passing a pygame event, to be raised when the "Enter" key is pressed.  Used largely for turning the page.
		normal:		An optional value for passing an image to be rendered as the input box's typical-state texture.
		highlight:	An optional value for passing an image to be rendered as the input box's in-use-state texture.
		dark:		An optional value for passing an image to be rendered as the input box's deactivated-state texture.

	Returns:
		nothing

	Raises:
		Executes the function passed in via "action"
		OR
		A turn-page event which is created by using the data from the dictionary passed in via "eventDict", if "action" is not present
	"""
	
	def __init__(self, rect=None, varstring = None, bgcolor=Globals.LIGHTGRAY, fgcolor=Globals.BLACK, font=None, action=None, event=None, normal=None, highlight=None, dark=None):
		if rect is None:
			self._rect = pygame.Rect(0, 0, 30, 60)
		else:
			self._rect = pygame.Rect(rect)
		
		# If there is no exposed variable to input text into, then this input should not be created.
		if varstring is None:
			raise Exception('foo')
		else:
			self._varString = varstring
		
		self._bgcolor = bgcolor
		self._fgcolor = fgcolor
		self.color_active = Globals.LIGHTGRAY
		self.color_inactive = Globals.DARKGRAY
		self.color = self.color_inactive
		
		# Set up the font.
		if font is None:
			self._font = pygame.font.Font('freesansbold.ttf', 14)
		else:
			self._font = font
		#self.messageSurf = self._font.render(self._text, True, self._fgcolor, self._bgcolor)
		
		# Tracks the state of the input box.
		self.active = False # Is the box currently in use?
		self.mouseOverBox = False # Is the mouse currently hovering over the box?
		self.lastMouseDownOverBox = False # Was the last mouse down event over the box? (Used to track clicks.)
		self._visible = True # Is the box visible?
		self.customSurfaces = False # Does the box start as a text button instead of having custom images for each surface?
		self.inputString = '' # The current string typed into the input box.
		
		self._action = action
		self._event = event
		
		if normal is None:
			# Create the surfaces for an input box.
			self.surfaceNormal = pygame.Surface(self._rect.size)
			self.surfaceDark = pygame.Surface(self._rect.size)
			self.surfaceHighlight = pygame.Surface(self._rect.size)
			self._update() # draw the initial box images
		else:
			# Create the surfaces for a custom image input box
			self.setSurfaces(normal, dark, highlight)
	
	def setSurfaces(self, normalSurface, darkSurface=None, highlightSurface=None):
		"""Switch the bar to a custom image type of box. You can specify either a pygame.Surface object or a string of a filename to load for each of the three input appearance states."""
		if darkSurface is None:
			darkSurface = normalSurface
		if highlightSurface is None:
			highlightSurface = normalSurface
		
		if type(normalSurface) == str:
			self.origSurfaceNormal = pygame.image.load(normalSurface)
		if type(darkSurface) == str:
			self.origsurfaceDark = pygame.image.load(darkSurface)
		if type(highlightSurface) == str:
			self.origSurfaceHighlight = pygame.image.load(highlightSurface)
		
		if self.origSurfaceNormal.get_size() != self.origsurfaceDark.get_size() != self.origSurfaceHighlight.get_size():
			raise Exception('foo')
		
		self.surfaceNormal = self.origSurfaceNormal
		self.surfaceDark = self.origsurfaceDark
		self.surfaceHighlight = self.origSurfaceHighlight
		self.customSurfaces = True
		self._rect = pygame.Rect((self._rect.left, self._rect.top, self.surfaceNormal.get_width(), self.surfaceNormal.get_height()))
	
	def _update(self):
		"""Redraw the input box's Surface object. Call this method when the box has changed appearance."""
		if self.customSurfaces:
			self.surfaceNormal = pygame.transform.smoothscale(self.origSurfaceNormal, self._rect.size)
			self.surfaceDark = pygame.transform.smoothscale(self.origsurfaceDark, self._rect.size)
			self.surfaceHighlight = pygame.transform.smoothscale(self.origSurfaceHighlight, self._rect.size)
			return
		
		w = self._rect.width # syntactic sugar
		h = self._rect.height # syntactic sugar
		
		# Fill background color for all box states.
		self.surfaceNormal.fill(self.bgcolor)
		self.surfaceDark.fill(self.bgcolor)
		self.surfaceHighlight.fill(self.bgcolor)

		# Draw the currently-inputted text string for all box states.
		messageSurf = self._font.render(self.inputString, True, self._fgcolor, self._bgcolor)
		messageRect = messageSurf.get_rect()
		messageRect.center = int(w / 2), int(h / 2)
		self.surfaceNormal.blit(messageSurf, messageRect)
		self.surfaceDark.blit(messageSurf, messageRect)
		self.surfaceHighlight.blit(messageSurf, messageRect)

		# Draw border for normal box.
		pygame.draw.rect(self.surfaceNormal, Globals.BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
		pygame.draw.rect(self.surfaceNormal, Globals.WHITE, pygame.Rect((1, 1, w-3, h-3)), 2) # white inner border

		# Draw border for a highlighted box (input in use).
		pygame.draw.rect(self.surfaceHighlight, Globals.BLACK, pygame.Rect((0, 0, w, h)), 1) # black border around everything
		pygame.draw.rect(self.surfaceHighlight, Globals.GRAY, pygame.Rect((1, 1, w-3, h-3)), 2) # gray inner border
		pygame.draw.line(self.surfaceHighlight, Globals.GRAY, (2, h-2), (w-2, h-2)) # horizontal bottom
	
	def draw(self, surfaceObj):
		"""Blit the current button's appearance to the surface object."""
		if self._visible:
			if self.active or self.mouseOverBox:
				surfaceObj.blit(self.surfaceHighlight, self._rect)
			else:
				surfaceObj.blit(self.surfaceNormal, self._rect)
	
	
	def handleEvent(self, eventObj):
		retVal = []
		
		# This if tree handles the mouse clicking on the input box
		if eventObj.type == MOUSEBUTTONDOWN:
			# If the mouse clicked on the input box.
			if self.rect.collidepoint(eventObj.pos):
				# Toggle the active variable.
				self.active = not self.active
			else:
				self.active = False
		
		# This if tree handles typing input
		if eventObj.type == KEYDOWN:
			if self.active:
				if eventObj.key == K_RETURN:
					self.submitInputText()
					#print(self.inputString)
					self.inputString = ''
				elif eventObj.key == K_BACKSPACE:
					self.inputString = self.inputString[:-1]
				else:
					self.inputString += eventObj.unicode
				# Re-render the input box to account for the new text.
				self._update()
			
		
		"""
		hasExited = False
		if not self.mouseOverBox and self._rect.collidepoint(eventObj.pos):
			# If mouse is hovering over the box:
			self.mouseOverBox = True
			self.mouseEnter(eventObj)
			retVal.append('enter')
		elif self.mouseOverBox and not self._rect.collidepoint(eventObj.pos):
			# If mouse had exited the box:
			self.mouseOverBox = False
			hasExited = True # Call mouseExit() later, since we want mouseMove() to be handled before mouseExit().
		
		if self._rect.collidepoint(eventObj.pos):
			# If mouse event happened over the box:
			if eventObj.type == MOUSEMOTION:
				self.mouseMove(eventObj)
				retVal.append('move')
			elif eventObj.type == MOUSEBUTTONDOWN:
				self.buttonDown = True
				self.lastMouseDownOverBox = True
				self.mouseDown(eventObj)
				retVal.append('down')
		else:
			if eventObj.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
				# If an up/down happens off the box, then the next up won't cause mouseClick().
				self.lastMouseDownOverBox = False
		
		# Mouse up is handled whether or not it was over the box
		doMouseClick = False
		if eventObj.type == MOUSEBUTTONUP:
			if self.lastMouseDownOverBoc:
				doMouseClick = True
			self.lastMouseDownOverBox = False
			
			if self.active:
				self.active = False
				self.mouseUp(eventObj)
				retVal.append('up')
			
			if doMouseClick:
				self.active = False
				self.mouseClick(eventObj)
				retVal.append('click')
		
		if hasExited:
			self.mouseExit(eventObj)
			retVal.append('exit')
		"""
		
		return retVal
	
	def submitInputText(self):
		if self._action != None:
			self._action()
		elif self._event != None:
			self._event.dict[self._varString] = self.inputString
			pygame.event.post(self._event)
	
	def mouseEnter(self, event):
		pass # This class is meant to be overridden.
	
	def mouseExit(self, event):
		pass # This class is meant to be overridden.
	
	def mouseMove(self, event):
		pass # This class is meant to be overridden.
	
	def mouseDown(self, event):
		pass # This class is meant to be overridden.
	
	def mouseUp(self, event):
		pass # This class is meant to be overridden.
	
	def _propGetMessage(self):
		return self._message
	
	def _propSetMessage(self, messageText):
		self.customSurfaces = False
		self._message = messageText
		self._update()
	
	def _propGetRect(self):
		return self._rect
	
	def _propSetRect(self, newRect):
		# Note that changing the attributes of the Rect won't update the button.  You have to re-assign the rect member.
		self._update()
		self._rect = newRect
	
	def _propGetVisible(self):
		return self._visible
	
	def _propSetVisible(self, setting):
		self._visible = setting
	
	def _propGetFgColor(self):
		return self._fgcolor
	
	def _propSetFgColor(self, setting):
		self.customSurfaces = False
		self._fgcolor = setting
		self._update()
	
	def _propGetBgColor(self):
		return self._bgcolor
	
	def _propSetBgColor(self, setting):
		self.customSurfaces = False
		self._bgcolor = setting
		self._update()
	
	def _propGetFont(self):
		return self._font
	
	def _propSetFont(self, setting):
		self.customSurfaces = False
		self._font = setting
		self._update()
	
	message = property(_propGetMessage, _propSetMessage)
	rect = property(_propGetRect, _propSetRect)
	visible = property(_propGetVisible, _propSetVisible)
	fgcolor = property(_propGetVisible, _propSetVisible)
	bgcolor = property(_propGetBgColor, _propSetBgColor)
	font = property(_propGetFont, _propSetFont)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - -
	
class OLECard(object):
	"""
	The class for an action card.
	TODO: Expanding this class to include standardized card formatting and text wrapping.

	Args:
		rect:		The pygame rectangle which defines the physical space the card takes up on the game screen.
		card:		A CardData object containing the card to be displayed.
		bgcolor:	The background color of the card.
		fgcolor:	The foreground color of the card.
		font:		The intended font of the displayed text.
		action:		An optional value for passing a non-specific function to the card, to be executed when the "Enter" key is pressed.
		eventDict:	An optional value for passing a pygame event, to be raised when the card is played.  Unused.
		normal:		An optional value for passing an image to be rendered as the card's typical-state texture.
		dark:		An optional value for passing an image to be rendered as the card's deactivated-state texture.
		flipped:	An optional value for passing an image to be rendered as the card's reverse-side texture.

	Returns:
		nothing

	Raises:
		Executes the function passed in via "action"
		OR
		A turn-page event which is created by using the data from the dictionary passed in via "eventDict", if "action" is not present
	"""
	
	def __init__(self, rect=None, card=None, bgcolor=Globals.LIGHTGRAY, fgcolor=Globals.BLACK, font=None, action=None, event=None, normal=None, dark=None, flipped=None):
		if rect is None:
			self._rect = pygame.Rect(0, 0, 64, 89)
		else:
			self._rect = pygame.Rect(rect)
		
		# If there is no card info to use, fill out the card with a blank template.
		if card is None:
			raise Exception('Cannot render a card without any data!')
		else:
			self._card = card
		
		# Set up colors and backgrounds
		self._bgcolor = bgcolor
		self._fgcolor = fgcolor
		self.color_active = Globals.LIGHTGRAY
		self.color_inactive = Globals.DARKGRAY
		self.color = self.color_inactive
		
		# Set up the font.
		if font is None:
			self._font = pygame.font.Font('freesansbold.ttf', 14)
		else:
			self._font = font
		#self.messageSurf = self._font.render(self._text, True, self._fgcolor, self._bgcolor)

		# Shapes the card uses.
		self.small_card = pygame.Rect(self._rect.x, self._rect.y, self._rect.w, self._rect.h)
		self.large_card = pygame.Rect(self._rect.x + 50, self._rect.y - 178, 128, 178)
		self.goal_rect = pygame.Rect(0, 0, 0, 0)
		self.old_rect = pygame.Rect(self._rect.x, self._rect.y, self._rect.w, self._rect.h)
		#self.placeholder_space = pygame.Rect(self._rect.x, self._rect.y, self._rect.w, self._rect.h)
		
		# Tracks the state of the card.
		self.transiting = False # Is the card currently animated?
		self.flipped = False # Is the card currently face-down?
		self.selected = False # Is the card removed from the hand and displayed in a larger size?
		self.selecting = False # Is the card in the animation process of being selected or deselected?
		self.cardHeld = False # Is the mouse being held down over the card?
		self.mouseOverCard = False # Is the mouse currently hovering over the card?
		self.lastMouseDownOverCard = False # Was the last mouse down event over the card? (Used to track clicks.)
		self._visible = True # Is the card visible?
		self.customSurfaces = False # Does the card start as a text button instead of having custom images for each surface?
		
		# Technical variables
		self._action = action
		self._event = event
		self.animation_time = 0
		self.animation_frames = self.animation_time * Globals.FPS
		self.current_frame = self.animation_frames
		
		if normal is None:
			# Create the surfaces for a card.
			self.surfaceNormal = pygame.Surface(self._rect.size)
			self.surfaceDark = pygame.Surface(self._rect.size)
			self.surfaceFlipped = pygame.Surface(self._rect.size)
			self.origSurfaceNormal = pygame.Surface(self.large_card.size)
			self.origSurfaceDark = pygame.Surface(self.large_card.size)
			self.origSurfaceFlipped = pygame.Surface(self.large_card.size)
			self._update() # draw the initial card images
		else:
			# Create the surfaces for a custom image card
			self.setSurfaces(normal, dark, flipped)
	
	def setSurfaces(self, normalSurface, darkSurface=None, flippedSurface=None):
		"""Switch the card's front or back to a custom image. You can specify either a pygame.Surface object or a string of a filename to load for each of the three input appearance states."""
		if darkSurface is None:
			darkSurface = normalSurface
		if flippedSurface is None:
			flippedSurface = normalSurface
		
		if type(normalSurface) == str:
			self.origSurfaceNormal = pygame.image.load(normalSurface)
		if type(darkSurface) == str:
			self.origSurfaceDark = pygame.image.load(darkSurface)
		if type(flippedSurface) == str:
			self.origSurfaceFlipped = pygame.image.load(flippedSurface)
		
		if self.origSurfaceNormal.get_size() != self.origSurfaceDark.get_size() != self.origSurfaceFlipped.get_size():
			raise Exception('foo')
		
		self.surfaceNormal = self.origSurfaceNormal
		self.surfaceDark = self.origSurfaceDark
		self.surfaceFlipped = self.origSurfaceFlipped
		self.customSurfaces = True
		# TODO: The below line may conflict with move() and dynamic resizing.
		self._rect = pygame.Rect((self._rect.left, self._rect.top, self.surfaceNormal.get_width(), self.surfaceNormal.get_height()))
	
	def _update(self):
		"""Redraw the card's Surface object. Call this method when the card has changed appearance."""
		# Fill background color for all card states.
		self.origSurfaceNormal.fill(self._bgcolor)
		self.origSurfaceDark.fill(self._bgcolor)
		self.origSurfaceFlipped.fill(self._bgcolor)

		# Draw card title text for all card states.
		titleSurf = self._font.render(self._card._name, True, self._fgcolor, self._bgcolor)
		titleRect = titleSurf.get_rect()
		titleRect.center = int(self.large_card.w / 2), int(self.large_card.h / 8)
		self.origSurfaceNormal.blit(titleSurf, titleRect)
		self.origSurfaceDark.blit(titleSurf, titleRect)
		self.origSurfaceFlipped.blit(titleSurf, titleRect)

		# Draw card flavor text for all card states.
		# TODO: Make the flavor text wrap
		flavorTextSurf = self._font.render(self._card._flavor_text, True, self._fgcolor, self._bgcolor)
		flavorTextRect = flavorTextSurf.get_rect()
		flavorTextRect.center = int(self.large_card.w / 2), int(self.large_card.h / 2)
		self.origSurfaceNormal.blit(flavorTextSurf, flavorTextRect)
		self.origSurfaceDark.blit(flavorTextSurf, flavorTextRect)
		self.origSurfaceFlipped.blit(flavorTextSurf, flavorTextRect)

		# Any drawing on the card's surfaces must occur before this line.
		# Animate the card moving.
		if (self.transiting):
			# Adjust the card's features linearly with time, over the desired timeline.
			# TODO: These functions will need to change for parabolic movement to be possible.
			self._rect.x = self.old_rect.x + ((self.goal_rect.x - self.old_rect.x) * ((self.animation_frames - self.current_frame) / self.animation_frames))
			self._rect.y = self.old_rect.y + ((self.goal_rect.y - self.old_rect.y) * ((self.animation_frames - self.current_frame) / self.animation_frames))
			self._rect.width = self.old_rect.width + ((self.goal_rect.width - self.old_rect.width) * ((self.animation_frames - self.current_frame) / self.animation_frames))
			self._rect.height = self.old_rect.height + ((self.goal_rect.height - self.old_rect.height) * ((self.animation_frames - self.current_frame) / self.animation_frames))
			self.current_frame -= 1

			if self.current_frame <= 0:
				# Cease animation.
				self.transiting = False
				# Achieve the desired location and size.
				self._rect.x = self.goal_rect.x
				self._rect.y = self.goal_rect.y
				self._rect.w = self.goal_rect.w
				self._rect.h = self.goal_rect.h
				# Toggle selecting state, if relevant
				if self.selecting:
					self.selected = not self.selected
					self.selecting = False
		
		# Squash and stretch the original custom images or the fabricated images.
		self.surfaceNormal = pygame.transform.smoothscale(self.origSurfaceNormal, self._rect.size)
		self.surfaceDark = pygame.transform.smoothscale(self.origSurfaceDark, self._rect.size)
		self.surfaceFlipped = pygame.transform.smoothscale(self.origSurfaceFlipped, self._rect.size)
	
	def draw(self, surfaceObj):
		"""Blit the card's current appearance to the surface object."""
		if self.transiting:
			self._update()

		if self._visible:
			if self.flipped:
				surfaceObj.blit(self.surfaceFlipped, self._rect)
			else:
				surfaceObj.blit(self.surfaceNormal, self._rect)		
	
	def handleEvent(self, eventObj):
		if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN) or not self._visible:
			# The card only cares about mouse-related events (or no events, if it is invisible).
			return []
		
		retVal = []
		
		hasExited = False
		if not self.mouseOverCard and (self.small_card.collidepoint(eventObj.pos)):
			# If mouse has entered the small card:
			self.mouseOverCard = True
			self.mouseEnter(eventObj)
			retVal.append('enter')
		elif self.mouseOverCard and not (self.small_card.collidepoint(eventObj.pos) or self.large_card.collidepoint(eventObj.pos)):
			# If mouse had exited all card areas:
			self.mouseOverCard = False
			hasExited = True # Call mouseExit() later, since we want mouseMove() to be handled before mouseExit().
		
		if (self.small_card.collidepoint(eventObj.pos) or self.large_card.collidepoint(eventObj.pos)):
			# If mouse event happened over any card area:
			if eventObj.type == MOUSEMOTION:
				self.mouseMove(eventObj)
				retVal.append('move')
			elif eventObj.type == MOUSEBUTTONDOWN:
				self.cardHeld = True
				self.lastMouseDownOverCard = True
				self.mouseDown(eventObj)
				retVal.append('down')
		else:
			if eventObj.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
				# If an up/down happens off the card, then the next up won't cause mouseClick().
				self.lastMouseDownOverCard = False
		
		# Mouse up is handled whether or not it was over the card
		doMouseClick = False
		if eventObj.type == MOUSEBUTTONUP:
			if self.lastMouseDownOverCard:
				doMouseClick = True
			self.lastMouseDownOverCard = False
			
			if self.cardHeld:
				self.cardHeld = False
				self.mouseUp(eventObj)
				retVal.append('up')
			
			if doMouseClick:
				self.cardHeld = False
				self.mouseClick(eventObj)
				retVal.append('click')
		
		if hasExited:
			self.mouseExit(eventObj)
			retVal.append('exit')
		
		return retVal
	
	def mouseClick(self, event):
		if event.button == 1: # Left click.
			if self.selected:
				self.move(0.5, self.small_card)
				self.selecting = True
				print("Small Card: " + str(self.small_card.x) + ", " + str(self.small_card.y) + ", " + str(self.small_card.w) + ", " + str(self.small_card.h))
			else:
				self.move(0.5, self.large_card)
				self.selecting = True
				print("Large Card: " + str(self.large_card.x) + ", " + str(self.large_card.y) + ", " + str(self.large_card.w) + ", " + str(self.large_card.h))
			#if self._action != None:
			#	self._action()
			#elif self._event != None:
			#	pygame.event.post(self._event)
	
	def move(self, seconds, rectangle):
		# Begin the animation
		self.transiting = True
		# Reset the animation timing tracker variables with current data
		self.animation_time = seconds
		self.animation_frames = self.animation_time * Globals.FPS
		self.current_frame = self.animation_frames
		self.old_rect = pygame.Rect(self._rect.x, self._rect.y, self._rect.w, self._rect.h)

		if rectangle is None:
			raise Exception("Cannot move to nonexistant rectangle!")
		else:
			self.goal_rect.x = rectangle.x
			self.goal_rect.y = rectangle.y
			self.goal_rect.w = rectangle.w
			self.goal_rect.h = rectangle.h
	
	def mouseEnter(self, event):
		pass # This class is meant to be overridden.
	
	def mouseExit(self, event):
		pass # This class is meant to be overridden.
	
	def mouseMove(self, event):
		pass # This class is meant to be overridden.
	
	def mouseDown(self, event):
		pass # This class is meant to be overridden.
	
	def mouseUp(self, event):
		pass # This class is meant to be overridden.