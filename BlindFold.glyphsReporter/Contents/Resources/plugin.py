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

from GlyphsApp import *
from GlyphsApp.plugins import *
import math

glyphsVersion = float(wrapperVersion)

class BlindFold(ReporterPlugin):

	def settings(self):
		self.name = 'Blindfold'
		self.thisMenuTitle = {"name": u"%s:" % self.name, "action": None }
		self.toggleNames = ["x-Height", "Cap-Height"]
		self.toggleShadeNames = ["White", "Black"]
		self.generalContextMenus = [
			self.thisMenuTitle,
			{"name": u"%s" % self.toggleNames[0], "action": self.toggleHeight},
			#{"name": u"%s" % self.toggleShadeNames[0], "action": self.toggleShade },
		]

		# self.menuName = Glyphs.localize({'en': u'* Blindfold 🙈', 'de': u'* Blindfold 🙈'})
		self.menuName = Glyphs.localize({'en': u'Blindfold'})
		self.showXHeight = True
		self.paintBlack = True

	def toggleHeight(self):
		switch = bool(self.showXHeight)
		self.generalContextMenus = [
			self.thisMenuTitle,
			{"name": u"%s" % self.toggleNames[switch], "action": self.toggleHeight},
			#{"name": u"%s" % self.toggleShadeNames[int(self.paintBlack)], "action": self.toggleShade},
		]
		self.showXHeight = not self.showXHeight
		self.RefreshView()

	def toggleShade(self):
		switch = bool(self.paintBlack)
		self.generalContextMenus = [
			self.thisMenuTitle,
			{"name": u"%s" % self.toggleNames[int(self.showXHeight)], "action": self.toggleHeight},
			#{"name": u"%s" % self.toggleShadeNames[switch], "action": self.toggleShade },
		]
		self.paintBlack = not self.paintBlack
		self.RefreshView()

	@objc.python_method
	def foreground(self, layer): # def background(self, layer):
		self.drawRect(layer, self.getScale())

	@objc.python_method
	def inactiveLayerBackground(self, layer):
		self.drawRect(layer, self.getScale())

	# Keep original drawing for inactive layers:
	def needsExtraMainOutlineDrawingForInactiveLayer_(self, Layer):
		return True


	@objc.python_method
	def topY(self, layer): # coulf be used to automate the height
		if glyphsVersion >= 3:
			return layer.associatedFontMaster().topHeightForLayer_(layer)
		else:
			if layer.parent.subCategory == "Lowercase":
				return layer.associatedFontMaster().xHeight
			else:
				return layer.associatedFontMaster().capHeight

	@objc.python_method
	def ascender(self, layer):
		if glyphsVersion >= 3:
			return layer.associatedFontMaster().ascenderForLayer_(layer)
		else:
			return layer.associatedFontMaster().ascender

	@objc.python_method
	def capHeight(self, layer):
		if glyphsVersion >= 3:
			return layer.associatedFontMaster().metricForKey_layer_(GSMetricsKeyCapHeight, layer)
		else:
			return layer.associatedFontMaster().capHeight

	@objc.python_method
	def xHeight(self, layer):
		if glyphsVersion >= 3:
			return layer.associatedFontMaster().xHeightForLayer_(layer)
		else:
			return layer.associatedFontMaster().xHeight

	@objc.python_method
	def descender(self, layer):
		if glyphsVersion >= 3:
			return layer.associatedFontMaster().descenderForLayer_(layer)
		else:
			return layer.associatedFontMaster().descender
	@objc.python_method
	def drawRect(self, layer, scale):
		view = self.controller.graphicView()
		Visible = view.visibleRect()
		activePosition = view.activePosition()

		UcLcCompensator = -600 / scale # avoid weird gap when a line starts with an UC and LC follow
		relativePosition = NSMakePoint(math.floor((Visible.origin.x - activePosition.x) / scale), math.floor((NSMinY(Visible) - activePosition.y + Visible.size.height) / scale))

		moreBlack = 70  # Optional: Additional Buffer to top and bottom

		try:
			if self.paintBlack is True:
				NSColor.blackColor().set()
			else:
				NSColor.whiteColor().set()

			'''	Rect 1: Descender '''
			y = self.descender(layer) - moreBlack  # descender
			height = (y * -1) + 1 # +1 closes the tiny gap
			NSBezierPath.fillRect_(((relativePosition[0] + UcLcCompensator, y), ((math.floor((Visible.size.width - UcLcCompensator + activePosition.x) / scale), height))))

			''' Rect 2: Ascender '''
			# if self.sliderMenuView.group.PUButton.getTitle() == "Cap-Height":
			# if self.sliderMenuView.group.PUButton.get() == 1:
			if self.showXHeight:
				y = self.xHeight(layer) # xHeight
			# if self.sliderMenuView.group.PUButton.getTitle() == "x-Height":
			else:
				y = self.capHeight(layer) # capHeight

			height = self.ascender(layer) + moreBlack - y + moreBlack # ascender - y
			NSBezierPath.fillRect_(((relativePosition[0] + UcLcCompensator, y), ((math.floor((Visible.size.width - UcLcCompensator + activePosition.x) / scale), height))))
		except: pass

	def RefreshView(self):
		try:
			Glyphs = NSApplication.sharedApplication()
			currentTabView = Glyphs.font.currentTab
			if currentTabView:
				currentTabView.graphicView().setNeedsDisplay_(True)
		except:
			pass

