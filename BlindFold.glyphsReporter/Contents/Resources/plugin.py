# encoding: utf-8
from __future__ import division, print_function, unicode_literals

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
from math import floor

glyphsVersion = float(wrapperVersion)

class BlindFold(ReporterPlugin):

	@objc.python_method
	def settings(self):
		self.thisMenuTitle = {
			"name": Glyphs.localize({
				'en': 'Show Blindfold at:',
				'de': 'Blenden anzeigen auf:',
				'fr': 'Afficher bandeaux à:',
				'es': 'Mostrar vendas a la:',
				}),
			"action": None,
			}
		self.toggleNames = (
			Glyphs.localize({
				'en': 'Cap Height',
				'de': 'Versalhöhe',
				'fr': 'Hauteur des capitales',
				'es': 'Altura de mayúsculas',
				}),
			Glyphs.localize({
				'en': 'x-Height',
				'de': 'Mittellänge',
				'fr': 'Hauteur d’x',
				'es': 'Altura de x',
				}),
			)
		self.toggleShadeNames = (
			Glyphs.localize({
				'en': 'White',
				'de': 'Weiß',
				'fr': 'Blanc',
				'es': 'Blanco',
				}),
			Glyphs.localize({
				'en': 'Black',
				'de': 'Schwarz',
				'fr': 'Noir',
				'es': 'Negro',
				}),
			)
		self.generalContextMenus = [
			self.thisMenuTitle,
			{"name": self.toggleNames[0], "action": self.toggleHeight},
			#{"name": u"%s" % self.toggleShadeNames[0], "action": self.toggleShade },
		]

		# self.menuName = Glyphs.localize({'en': u'* Blindfold 🙈', 'de': u'* Blindfold 🙈'})
		self.menuName = Glyphs.localize({
			'en': 'Blindfold',
			'de': 'Blenden',
			'fr': 'bandeaux',
			'es': 'vendas',
			})
		self.showXHeight = True
		self.paintBlack = True

	def toggleHeight(self):
		switch = bool(self.showXHeight)
		self.generalContextMenus = [
			self.thisMenuTitle,
			{"name": self.toggleNames[switch], "action": self.toggleHeight},
			#{"name": u"%s" % self.toggleShadeNames[int(self.paintBlack)], "action": self.toggleShade},
		]
		self.showXHeight = not self.showXHeight
		self.RefreshView()

	@objc.python_method
	def toggleShade(self):
		switch = bool(self.paintBlack)
		self.generalContextMenus = [
			self.thisMenuTitle,
			{"name": self.toggleNames[int(self.showXHeight)], "action": self.toggleHeight},
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
		try:
			# GLYPHS 3
			return layer.master.topHeightForLayer_(layer)
		except:
			# GLYPHS 2
			if layer.parent.subCategory == "Lowercase":
				return layer.master.xHeight
			else:
				return layer.master.capHeight

	@objc.python_method
	def ascender(self, layer):
		try:
			# GLYPHS 3
			return layer.master.ascenderForLayer_(layer)
		except:
			# GLYPHS 2
			return layer.master.ascender

	@objc.python_method
	def capHeight(self, layer):
		try:
			# GLYPHS 3
			return layer.master.metricForKey_layer_(GSMetricsKeyCapHeight, layer)
		except:
			# GLYPHS 2
			return layer.master.capHeight

	@objc.python_method
	def xHeight(self, layer):
		try:
			# GLYPHS 3
			return layer.master.xHeightForLayer_(layer)
		except:
			# GLYPHS 2
			return layer.master.xHeight

	@objc.python_method
	def descender(self, layer):
		try:
			# GLYPHS 3
			return layer.master.descenderForLayer_(layer)
		except:
			# GLYPHS 2
			return layer.master.descender
			
	@objc.python_method
	def drawRect(self, layer, scale):
		view = self.controller.graphicView()
		Visible = view.visibleRect()
		activePosition = view.activePosition()

		UcLcCompensator = -600 / scale # avoid weird gap when a line starts with an UC and LC follow
		relativePosition = NSMakePoint(
			floor((Visible.origin.x - activePosition.x) / scale), 
			floor((NSMinY(Visible) - activePosition.y + Visible.size.height) / scale)
			)

		moreBlack = 70  # Optional: Additional Buffer to top and bottom

		try:
			if self.paintBlack is True:
				NSColor.textColor().set()
			else:
				NSColor.textBackgroundColor().set()

			'''	Rect 1: Descender '''
			y = self.descender(layer) - moreBlack  # descender
			height = (y * -1) + 1 # +1 closes the tiny gap
			NSBezierPath.fillRect_(((relativePosition[0] + UcLcCompensator, y), ((floor((Visible.size.width - UcLcCompensator + activePosition.x) / scale), height))))

			''' Rect 2: Ascender '''
			# if self.sliderMenuView.group.PUButton.getTitle() == "Cap-Height":
			# if self.sliderMenuView.group.PUButton.get() == 1:
			if self.showXHeight:
				y = self.xHeight(layer) # xHeight
			# if self.sliderMenuView.group.PUButton.getTitle() == "x-Height":
			else:
				y = self.capHeight(layer) # capHeight

			height = self.ascender(layer) + more
			- y + moreBlack # ascender - y
			NSBezierPath.fillRect_(((relativePosition[0] + UcLcCompensator, y), ((floor((Visible.size.width - UcLcCompensator + activePosition.x) / scale), height))))
		except:
			pass

	@objc.python_method
	def RefreshView(self):
		try:
			Glyphs = NSApplication.sharedApplication()
			currentTabView = Glyphs.font.currentTab
			if currentTabView:
				currentTabView.graphicView().setNeedsDisplay_(True)
		except:
			pass

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

