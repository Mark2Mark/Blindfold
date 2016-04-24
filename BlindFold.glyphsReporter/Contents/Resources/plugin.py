# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

from GlyphsApp.plugins import *
from vanilla import *
import math

class BlindFold(ReporterPlugin):

	def settings(self):

		###################################
		## Rotation Slider for Context Menu:
		self.name = 'Blindfold'

		# Create Vanilla window and group with controls
		viewWidth = 160
		viewHeight = 65 # 65
		self.sliderMenuView = Window((viewWidth, viewHeight))
		self.sliderMenuView.group = Group((0, 0, viewWidth, viewHeight)) # (0, 0, viewWidth, viewHeight)
		self.sliderMenuView.group.line = HorizontalLine((10, 10, -10, 1))
		# self.sliderMenuView.group.text = TextBox((10, 20, -10, -10), self.name)
		# self.sliderMenuView.group.PUButton = PopUpButton((10, 40, -10, 20), ["x-Height", "Cap-Height"], sizeStyle="small", callback=self.PopUpButtonCallback)
		self.sliderMenuView.group.PUButton = RadioGroup((10, 20, -10, 40), ["Blindfold: x-Height", "Blindfold: Cap-Height"], sizeStyle="small", callback=self.PopUpButtonCallback)
		self.sliderMenuView.group.PUButton.set(0)

		## Define the menu
		self.generalContextMenus = [
		    {"view": self.sliderMenuView.group.getNSView()}
		]
		###################################

		# self.menuName = Glyphs.localize({'en': u'* Blindfold 🙈', 'de': u'* Blindfold 🙈'})
		self.menuName = Glyphs.localize({'en': u'* Blindfold'})


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#		UNDER CONSTRUCTION
# 		# mainMenu = NSMenuItem.alloc().init()
# 		# mainMenu.setTitle_("Main Item")

# 		subMenu = NSMenu.alloc().init()
# 		subMenu.addItemWithTitle_action_keyEquivalent_("Sub Menu here", self.RefreshView, "")
# 		print "\n__SubMenu:\n%s\n" % subMenu

# 		### IRGENDWAS VON DEN SACHEN HIER: (?)

# 		# self.addMenuItemsForEvent_toMenu_(subMenu, self.generalContextMenus)
# 		# print "\n__generalContextMenus:\n%s\n" % self.generalContextMenus

# 		# mainMenu.setSubmenu_(subMenu)
# 		# self.addMenuItemsForEvent_toMenu_(mainMenu, self.generalContextMenus)

# 		# self.generalContextMenus.setSubmenu(subMenu)
# 		# self.generalContextMenus.append(subMenu)


# 	### DIESE addMenuItemsForEvent_toMenu_??
# 	# def addMenuItemsForEvent_toMenu_(self, event, contextMenu):
# 	# 	'''
# 	# 	The event can tell you where the user had clicked.
# 	# 	'''
# 	# 	try:
			
# 	# 		if self.generalContextMenus:
# 	# 			setUpMenuHelper(contextMenu, self.generalContextMenus, self)
			
# 	# 		if hasattr(self, 'conditionalContextMenus'):
# 	# 			contextMenus = self.conditionalContextMenus()
# 	# 			if contextMenus:
# 	# 				setUpMenuHelper(contextMenu, contextMenus, self)

# 	# 	except:
# 	# 		self.logError(traceback.format_exc())

# 	### ODER DIESE addMenuItemsForEvent_toMenu_??
# 	def addMenuItemsForEvent_toMenu_(self, theEvent, theMenu):
# 		try:
			
# 			if hasattr(self, 'conditionalContextMenus'):
# 				contextMenus = self.conditionalContextMenus()
			
# 				if contextMenus:
# 					# Todo: Make sure that the index is 0 for all items
# 					setUpMenuHelper(theMenu, contextMenus, self)
					
# 					newSeparator = NSMenuItem.separatorItem()
# 					theMenu.insertItem_atIndex_(newSeparator, 1)
					
# 		except:
# 			self.logError(traceback.format_exc())
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


	def background(self, layer):  # def foreground(self, layer):
		self.drawRect(layer, self.getScale() )

	def inactiveLayers(self, layer):
		self.drawRect(layer, self.getScale() )
		# inactiveLayers() overwrites Glyphs built-in drawing,
		# hence redo drawing here:
		self.redrawLayer(layer)

	def preview(self, layer):
		# preview() overwrites Glyphs built-in drawing,
		# hence redo drawing here:		
		self.redrawLayer(layer)

	def redrawLayer(self, layer):
		NSColor.blackColor().set()
		if layer.paths:
			layer.bezierPath.fill()
		if layer.components:
			for component in layer.components:
				component.bezierPath.fill()			

	def drawRect(self, layer, scale):
		view = self.controller.graphicView()
		Visible = view.visibleRect()
		activePosition = view.activePosition()

		UcLcCompensator = -600 / scale # avoid weird gap when a line starts with an UC and LC follow
		relativePosition = NSMakePoint(math.floor((Visible.origin.x - activePosition.x) / scale), math.floor((NSMinY(Visible) - activePosition.y + Visible.size.height) / scale))

		moreBlack = 70  # Optional: Additional Buffer to top and bottom

		try:
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 0, 0, 0, 1 ).set()
			
			'''	Rect 1: Descender '''
			y = layer.glyphMetrics()[3] - moreBlack  # descender
			height = (y * -1) + 1 # +1 closes the tiny gap
			NSBezierPath.fillRect_( ( (relativePosition[0] + UcLcCompensator, y), ( ( math.floor((Visible.size.width - UcLcCompensator + activePosition.x) / scale) , height ) ) ) )
			
			''' Rect 2: Ascender '''	
			# if self.sliderMenuView.group.PUButton.getTitle() == "Cap-Height":
			if self.sliderMenuView.group.PUButton.get() == 1:
			 	y = layer.glyphMetrics()[2] # capHeight
			# if self.sliderMenuView.group.PUButton.getTitle() == "x-Height":
			if self.sliderMenuView.group.PUButton.get() == 0:
			 	y = layer.glyphMetrics()[4] # xHeight
						
			height = layer.glyphMetrics()[1] + moreBlack - y + moreBlack # ascender - y			
			NSBezierPath.fillRect_( ( (relativePosition[0] + UcLcCompensator, y), ( ( math.floor((Visible.size.width - UcLcCompensator + activePosition.x) / scale) , height ) ) ) )
		except: pass


	def RefreshView(self):
		try:
			Glyphs = NSApplication.sharedApplication()
			currentTabView = Glyphs.font.currentTab
			if currentTabView:
				currentTabView.graphicView().setNeedsDisplay_(True)
		except:
			pass

	def PopUpButtonCallback(self, sender):
		self.RefreshView()
