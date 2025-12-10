# menuTitle: Glyph Showcaser

'''
Show your Drawings!
Tool to showcase your Glyphs and export it as PDF, SVG or PNG; change colours, Node Shapes and more.

Jacob Tegel 2024–2025
'''

from vanilla import *
from AppKit import NSColor, NSButton, NSView
from mojo.UI import Message
import drawBot
from drawBot.ui.drawView import DrawView
import traceback
import os
from datetime import datetime

time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

font = CurrentFont()

if font is None:
	Message('Please open a font in RoboFont.')

else: 
	name = ( f'{font.info.familyName}-{font.info.styleName}')
	fontName = name.replace(' ', '-')

class GlyphShowcaser:
	
	def __init__(self):
		self.winWidth = 1000
		self.winHeight = 1250
		self.sidebarWidth = 300
		self.sidebarHeight = 1715

		self.nodeStackSize = 0

		self.w = Window((self.winWidth, self.winHeight), 'Glyph Showcaser', (100, 100))
		self.w.controls = Group((-self.sidebarWidth, 10, self.sidebarWidth, self.sidebarHeight))

		x1 = 10
		x2 = 150
		
		y = 10
		
		w1 = 145
		w2 = -10
		
		h = 20

		dy = h + 15

		t = 5

		# Glyph selection
		self.w.controls.glyphSelectionLabel = TextBox((x1, y, w1, h), 'Glyph Selection')
		self.w.controls.glyphSelection = VerticalRadioGroup((x2, y-2.5, w2, h * 3), ['Current Glyph', 'Selected Glyphs', 'All Glyphs'], callback = self.redraw)
		self.w.controls.glyphSelection.set(0)
		y += dy + h * 2

		# margin
		self.w.controls.marginLabel = TextBox((x1, y, w1, h), 'Margin')
		self.w.controls.marginSlider = Slider((x2, y, w2-40, h + t), minValue = 0, maxValue = 500, value = 100, callback = self.marginSliderChanged)
		self.w.controls.marginValue = EditText((w2-35, y, w2, h + t), str(round(float(self.w.controls.marginSlider.get()))), callback = self.marginValueChanged, continuous = False)
		y += dy + t

		# height
		self.w.controls.artboardHeightLabel = TextBox((x1, y, w1, h), 'Artboard Height')
		self.w.controls.artboardHeight = VerticalRadioGroup((x2, y-2.5, w2, h * 2), ['Font Height', 'Glyph Height'], callback = self.redraw)
		self.w.controls.artboardHeight.set(0)
		y += dy + h

		# backgroundColor
		self.w.controls.backgroundColorLabel = TextBox((x1, y, w1, h), 'Background Color')
		self.w.controls.backgroundColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.clearColor())
		y += dy + 10

		# glyphColor
		self.w.controls.glyphColorLabel = TextBox((x1, y, w1, h), 'Glyph Color')
		self.w.controls.glyphColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.clearColor())
		y += dy + 10

		# glyphOutline
		self.w.controls.glyphOutlineLabel = TextBox((x1, y, w1, h), 'Glyph Outline')
		self.w.controls.glyphOutlineCheck = CheckBox((x2, y, w2, h), '', callback = self.redraw, value = True)
		y += dy

		# outlineColor
		self.w.controls.outlineColorLabel = TextBox((x1, y, w1, h), 'Outline Color')
		self.w.controls.outlineColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.blackColor())
		y += dy + 10

		# outlineThickness
		self.w.controls.outlineThicknessLabel = TextBox((x1, y, w1, h), 'Outline Thickness')
		self.w.controls.outlineThicknessSlider = Slider((x2, y, w2-40, h + t), minValue = 1, maxValue = 5, value = 1, callback = self.outlineThicknessSliderChanged)
		self.w.controls.outlineThicknessValue = EditText((w2-35, y, w2, h + t), str(round(float(self.w.controls.outlineThicknessSlider.get()), 1)), callback = self.outlineThicknessValueChanged, continuous = False)
		y += dy + t

		# showNodes
		self.w.controls.showNodesLabel = TextBox((x1, y, w1, h), 'Show Nodes')
		self.w.controls.showNodesCheck = CheckBox((x2, y, w2, h), '', callback = self.redraw, value = True)
		y += dy

		# cornerNodeShape
		self.w.controls.cornerNodeShapeLabel = TextBox((x1, y, w1, h), 'Corner PointShape')
		self.w.controls.cornerNodeShape = VerticalRadioGroup((x2, y-2.5, w2, h * 4), ['Circle', 'Rectangle', 'Triangle', 'Cross'], callback = self.redraw)
		self.w.controls.cornerNodeShape.set(1)
		y += dy + 3 * h

		# smoothCornerNodeShape
		self.w.controls.smoothCornerNodeShapeLabel = TextBox((x1, y, w1, h), 'Smooth Point Corner')
		self.w.controls.smoothCornerNodeShape = VerticalRadioGroup((x2, y-2.5, w2, h * 4), ['Circle', 'Rectangle', 'Triangle', 'Cross'], callback = self.redraw)
		self.w.controls.smoothCornerNodeShape.set(2)
		y += dy + 3 * h

		# onCurveNodeShape
		self.w.controls.onCurveNodeShapeLabel = TextBox((x1, y, w1, h), 'Curve Point Shape')
		self.w.controls.onCurveNodeShape = VerticalRadioGroup((x2, y-2.5, w2, h * 4), ['Circle', 'Rectangle', 'Triangle', 'Cross'], callback = self.redraw)
		self.w.controls.onCurveNodeShape.set(0)
		y += dy + 3 * h

		# offCurveNodeShape
		self.w.controls.offCurveNodeShapeLabel = TextBox((x1, y, w1, h), 'Offcurve Point Shape')
		self.w.controls.offCurveNodeShape = VerticalRadioGroup((x2, y-2.5, w2, h * 4), ['Circle', 'Rectangle', 'Triangle', 'Cross'], callback = self.redraw)
		self.w.controls.offCurveNodeShape.set(0)
		y += dy + 3 * h

		# nodeSize
		self.w.controls.nodeSizeLabel = TextBox((x1, y, w1, h), 'Node Size')
		self.w.controls.nodeSizeSlider = Slider((x2, y, w2-40, h + t), minValue = 1, maxValue = 10, value = 5, callback = self.nodeSizeSliderChanged)
		self.w.controls.nodeSizeValue = EditText((w2-35, y, w2, h + t), str(round(float(self.w.controls.nodeSizeSlider.get()), 1)), callback = self.nodeSizeValueChanged, continuous = False)
		y += dy + t

		# nodeSizeRatio
		self.w.controls.nodeSizeRatioLabel = TextBox((x1, y, w1, h), 'Node Size Ratio')
		self.w.controls.nodeSizeRatioSlider = Slider((x2, y, w2-40, h + t), minValue = 0, maxValue = 2, value = 1, callback = self.nodeSizeRatioSliderChanged)
		self.w.controls.nodeSizeRatioValue = EditText((w2-35, y, w2, h + t), str(round(float(self.w.controls.nodeSizeRatioSlider.get()), 1)), callback = self.nodeSizeRatioValueChanged, continuous = False)
		y += dy + t

		# makeNodesOutlineCol
		self.w.controls.makeNodesOutlineColLabel = TextBox((x1, y, w1, h), 'Node Color = Outline Color')
		self.w.controls.makeNodesOutlineColCheck = CheckBox((x2, y, w2, h), '', callback = self.makeNodesOutlineColCheckCallback, value = False)
		y += dy

		
		# cornerPoint
		self.w.controls.cornerPointLabel = TextBox((x1, y, w1, h), 'Corner Point')
		self.w.controls.cornerPointColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.blackColor())
		y += dy + 10
		# cornerStroke
		self.w.controls.cornerStrokeLabel = TextBox((x1, y, w1, h), 'Corner Point Outline')
		self.w.controls.cornerStrokeColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.blackColor())
		y += dy + 10
		
		# smoothCornerPoint
		self.w.controls.smoothCornerPointLabel = TextBox((x1, y, w1, h), 'Smooth Corner Point')
		self.w.controls.smoothCornerPointColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.blackColor())
		y += dy + 10
		# smoothCornerStroke
		self.w.controls.smoothCornerStrokeLabel = TextBox((x1, y, w1, h), 'Smooth Corner Outline')
		self.w.controls.smoothCornerStrokeColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.blackColor())
		y += dy + 10
		
		# onCurvePoint
		self.w.controls.onCurvePointLabel = TextBox((x1, y, w1, h), 'Curve Point')
		self.w.controls.onCurvePointColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.blackColor())
		y += dy + 10
		# onCurveStroke
		self.w.controls.onCurveStrokeLabel = TextBox((x1, y, w1, h), 'Curve Outline')
		self.w.controls.onCurveStrokeColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.blackColor())
		y += dy + 10

		# offCurvePoint
		self.w.controls.offCurvePointLabel = TextBox((x1, y, w1, h), 'Offcurve Point')
		self.w.controls.offCurvePointColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.blackColor())
		y += dy + 10
		# offCurveStroke
		self.w.controls.offCurveStrokeLabel = TextBox((x1, y, w1, h), 'Offcurve Stroke')
		self.w.controls.offCurveStrokeColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.blackColor())
		y += dy + 10
		

		# handlebar color
		self.w.controls.handleBarLabel = TextBox((x1, y, w1, h), 'Handle Bar')
		self.w.controls.handleBarColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.blackColor())
		y += dy + 10

		# removeOverlap
		self.w.controls.removeOverlapLabel = TextBox((x1, y, w1, h), 'Remove Overlap')
		self.w.controls.removeOverlapCheck = CheckBox((x2, y, w2, h), '', callback = self.redraw, value = True)
		y += dy

		# decomposeComponents
		self.w.controls.decomposeComponentsLabel = TextBox((x1, y, w1, h), 'Decompose Comps')
		self.w.controls.decomposeComponentsCheck = CheckBox((x2, y, w2, h), '', callback = self.redraw, value = True)
		y += dy
		
		# displayCoordinates
		self.w.controls.displayCoordinatesLabel = TextBox((x1, y, w1, h), 'Display Coordinates')
		self.w.controls.displayCoordinatesCheck = CheckBox((x2, y, w2, h), '', callback = self.displayCoordinatesCheckCallback, value = False)
		y += dy

		# coordinates color
		self.w.controls.coordinatesColorLabel = TextBox((x1, y, w1, h), 'Coordinates Color')
		self.w.controls.coordinatesColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color=NSColor.grayColor())
		y += dy + 10

		# displayMetrics
		self.w.controls.displayMetricsLabel = TextBox((x1, y, w1, h), 'Display Metrics')
		self.w.controls.displayMetricsCheck = CheckBox((x2, y, w2, h), '', callback = self.displayCoordinatesCheckCallback, value = False)
		y += dy

		# Metrics color
		self.w.controls.metricsColorLabel = TextBox((x1, y, w1, h), 'Metrics Color')
		self.w.controls.metricsColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color = NSColor.grayColor())
		y += dy + 10

		# displayBluezones
		self.w.controls.displayBluezonesLabel = TextBox((x1, y, w1, h), 'Display Bluezones')
		self.w.controls.displayBluezonesCheck = CheckBox((x2, y, w2, h), '', callback = self.displayBluezonesCheckCallback, value = False)
		y += dy

		# Bluezones color
		self.w.controls.bluezonesColorLabel = TextBox((x1, y, w1, h), 'Bluezones Color')
		self.w.controls.bluezonesColor = ColorWell((x2, y, w2, h + 10), callback = self.redraw, color = NSColor.colorWithRed_green_blue_alpha_(.5, 1, 1, .3))
		y += dy + 10


		# export as
		self.w.controls.exportText = TextBox((x1, y, w1, h), 'Export as:')
		self.w.controls.exportPdf = CheckBox((x2, y, w2, h), 'PDF')
		y += dy -10
		self.w.controls.exportSvg = CheckBox((x2, y, w2, h), 'SVG')
		y += dy -10
		self.w.controls.exportPng = CheckBox((x2, y, w2, h), 'PNG')
		y += dy

		# close
		self.w.closeButton = Button(((-self.sidebarWidth - 10), - h - h / 2, self.sidebarWidth / 2 - 5, h), 'Close', callback=self.close)
		# export
		self.w.exportButton = Button((-self.sidebarWidth / 2 - 5, - h - h / 2, self.sidebarWidth / 2 - 5, h), 'Export', callback=self.exportButtonCallback)

		self.w.setDefaultButton(self.w.exportButton)

		# view = self.w.controls.getNSView()
		self.w.scrollView = ScrollView((-(self.sidebarWidth) - 10, 10, self.sidebarWidth, - (10 + 10 + h)), self.w.controls.getNSView(), autohidesScrollers=True, drawsBackground = False)
		self.w.preview = DrawView((10, 10, -self.sidebarWidth - 20, -10))
		
		self.w.open()
		self.redraw(None)

	def marginSliderChanged(self, sender):
		v = round(float(self.w.controls.marginSlider.get()))
		self.w.controls.marginValue.set(str(v))
		self.redraw(sender)

	def marginValueChanged(self, sender):
		v = round(float(self.w.controls.marginValue.get()))
		self.w.controls.marginSlider.set(v)
		self.redraw(sender)

	def outlineThicknessSliderChanged(self, sender):
		v = round(float(self.w.controls.outlineThicknessSlider.get()), 1)
		self.w.controls.outlineThicknessValue.set(str(v))
		self.redraw(sender)

	def outlineThicknessValueChanged(self, sender):
		v = round(float(self.w.controls.outlineThicknessValue.get()), 1)
		self.w.controls.outlineThicknessSlider.set(v)
		self.redraw(sender)

	def nodeSizeSliderChanged(self, sender):
		v = round(float(self.w.controls.nodeSizeSlider.get()), 1)
		self.w.controls.nodeSizeValue.set(str(v))
		self.redraw(sender)

	def nodeSizeValueChanged(self, sender):
		v = round(float(self.w.controls.nodeSizeValue.get()), 1)
		self.w.controls.nodeSizeSlider.set(v)
		self.redraw(sender)

	def nodeSizeRatioSliderChanged(self, sender):
		v = round(float(self.w.controls.nodeSizeRatioSlider.get()), 1)
		self.w.controls.nodeSizeRatioValue.set(str(v))
		self.redraw(sender)

	def nodeSizeRatioValueChanged(self, sender):
		v = round(float(self.w.controls.nodeSizeRatioValue.get()), 1)
		self.w.controls.nodeSizeRatioSlider.set(v)
		self.redraw(sender)

	def makeNodesOutlineColCheckCallback(self, sender):
		
		self.redraw(sender)

	def displayCoordinatesCheckCallback(self, sender):

		self.redraw(sender)

	def displayBluezonesCheckCallback(self, sender):

		self.redraw(sender)

	def exportAs(self):

		exportPdf = self.w.controls.exportPdf.get()
		exportSvg = self.w.controls.exportSvg.get()
		exportPng = self.w.controls.exportPng.get()

		return exportPdf, exportSvg, exportPng

	def exportButtonCallback(self, sender):
		self.redraw(sender)
		self.export(sender)	

	def glyphsToProcess(self):
		
		glyphSelection = self.w.controls.glyphSelection.get()

		# Setup
		glyphsToProcess = []

		# Current glyph
		if glyphSelection == 0:
			glyphsToProcess = [CurrentGlyph()]

		# Selected glyphs    
		elif glyphSelection == 1:
			glyphsToProcess = [font[glyphName] for glyphName in font.selectedGlyphNames]

		# All glyphs
		elif glyphSelection == 2:
			glyphsToProcess = [glyph for glyph in font]

		return glyphsToProcess

	def drawNodes(self, x, y, s, shape, pointColor, strokeColor):

		makeNodesOutlineColor = self.w.controls.makeNodesOutlineColCheck.get()
		outlineColor = self.w.controls.outlineColor.get()
	
		outlineThickness = self.w.controls.outlineThicknessSlider.get()
		drawBot.strokeWidth(outlineThickness)

		drawBot.fill(pointColor)
		drawBot.stroke(strokeColor)

		if makeNodesOutlineColor:
			drawBot.fill(outlineColor)
			drawBot.stroke(outlineColor)

		if shape == 0:
								
			drawBot.oval(x - s, y - s, s * 2, s * 2)
		
		elif shape == 1:
							
			drawBot.rect(x - s, y - s, s * 2, s * 2)
							
		elif shape == 2:
			s *= 1.1
			drawBot.polygon((x - s, y - s), (x + s, y - s), (x, y + s))

		elif shape == 3:

			drawBot.stroke(pointColor)
			drawBot.line((x - s, y - s), (x + s, y + s))
			drawBot.line((x - s, y + s), (x + s, y - s))


	def redraw(self, sender):

		#Variables
		glyphSelection = self.w.controls.glyphSelection.get()
		
		margin = self.w.controls.marginSlider.get()
		artboardHeight = self.w.controls.artboardHeight.get()
		
		backgroundColor = self.w.controls.backgroundColor.get()
		glyphColor = self.w.controls.glyphColor.get()
		glyphOutline = self.w.controls.glyphOutlineCheck.get()
		
		outlineColor = self.w.controls.outlineColor.get()
		outlineThickness = self.w.controls.outlineThicknessSlider.get()
		
		showNodes = self.w.controls.showNodesCheck.get()
		makeNodesOutlineColor = self.w.controls.makeNodesOutlineColCheck.get()
		
		cornerNodeShape = self.w.controls.cornerNodeShape.get()
		smoothCornerNodeShape = self.w.controls.smoothCornerNodeShape.get()

		onCurveNodeShape = self.w.controls.onCurveNodeShape.get()
		
		offCurveNodeShape = self.w.controls.offCurveNodeShape.get()
		
		nodeSize = self.w.controls.nodeSizeSlider.get()
		nodeSizeRatio = self.w.controls.nodeSizeRatioSlider.get()
		
		cornerPointColor = self.w.controls.cornerPointColor.get()
		cornerStrokeColor = self.w.controls.cornerStrokeColor.get()

		smoothCornerPointColor = self.w.controls.smoothCornerPointColor.get()
		smoothCornerStrokeColor = self.w.controls.smoothCornerStrokeColor.get()

		onCurvePointColor = self.w.controls.onCurvePointColor.get()
		onCurveStrokeColor = self.w.controls.onCurveStrokeColor.get()
		
		offCurveStrokeColor = self.w.controls.offCurveStrokeColor.get()
		offCurvePointColor = self.w.controls.offCurvePointColor.get()
		handleBarColor = self.w.controls.handleBarColor.get()
		
		decomposeComponents = self.w.controls.decomposeComponentsCheck.get()
		removeOverlap = self.w.controls.removeOverlapCheck.get()
		
		displayCoordinates = self.w.controls.displayCoordinatesCheck.get()
		coordinatesColor = self.w.controls.coordinatesColor.get()
		displayMetrics = self.w.controls.displayMetricsCheck.get()
		metricsColor = self.w.controls.metricsColor.get()
		displayBluezones = self.w.controls.displayBluezonesCheck.get()
		bluezonesColor = self.w.controls.bluezonesColor.get()

		glyphsToProcess = self.glyphsToProcess()
		
		s = nodeSize
		r = nodeSizeRatio * s

		i = 6

		# Drawing
		drawBot.newDrawing()

		for glyph in glyphsToProcess:
			
			# Skip empty or None glyphs
			if glyph is None or not glyph.contours:
				continue		

			glyphHeight = abs(glyph.bounds[1]-glyph.bounds[3])

			if artboardHeight == 0:
				height = (font.info.ascender + margin) + -(font.info.descender - (margin / 2))
			else:
				height = (glyphHeight + margin)

			drawBot.newPage(glyph.width + margin, height)

			# Create Orphan
			c = glyph.copy()     
	
			drawBot.fill(backgroundColor)
			drawBot.rect(0, 0, glyph.width + margin, height + margin)
			
			if artboardHeight == 0:
				drawBot.translate(margin/2, -font.info.descender + (margin / 2))
			
			else:
				drawBot.translate(margin/2, -glyph.bounds[1] + margin / 2)
			
			if displayMetrics:
				drawBot.stroke(metricsColor)
				drawBot.fill(metricsColor)
				drawBot.fontSize(i)	
			
				drawBot.line((0 -  margin / 2, font.info.descender), (drawBot.width(), font.info.descender))
				drawBot.line((0 -  margin / 2, 0), (drawBot.width(), 0))
				drawBot.line((0 -  margin / 2, font.info.xHeight), (drawBot.width(), font.info.xHeight))
				drawBot.line((0 -  margin / 2, font.info.capHeight), (drawBot.width(), font.info.capHeight))
				drawBot.line((0 -  margin / 2, font.info.ascender), (drawBot.width(), font.info.ascender))
				
				drawBot.line((0, - 10), (0, 10))
				drawBot.line((glyph.width, -10), (glyph.width, 10))

				drawBot.stroke(None)

				o = 10

				drawBot.text(f'Descender',(0 + o -  margin / 2, font.info.descender - o), align='left',)
				drawBot.text(f'Baseline',(0 + o -  margin / 2, 0 - o), align='left',)
				drawBot.text(f'x-Height',(0 + o -  margin / 2, font.info.xHeight - o), align='left',)
				drawBot.text(f'Cap-Height',(0 + o -  margin / 2, font.info.capHeight - o), align='left',)
				drawBot.text(f'Ascender',(0 + o -  margin / 2, font.info.ascender - o), align='left',)

			if displayBluezones:
				drawBot.fill(bluezonesColor)
				drawBot.stroke(None)

				try:

					for e, blueValue in enumerate(font.info.postscriptBlueValues):
						nextBlueValue = font.info.postscriptBlueValues[(e + 1) % len(font.info.postscriptBlueValues)]
						if e % 2 != 0:
							continue
						drawBot.rect(0 - margin, blueValue, drawBot.width() + margin, abs(nextBlueValue - blueValue))

					for e, blueValue in enumerate(font.info.postscriptOtherBlues):
						nextBlueValue = font.info.postscriptOtherBlues[(e + 1) % len(font.info.postscriptOtherBlues)]
						if e % 2 != 0:
							continue
						drawBot.rect(0 - margin, blueValue, drawBot.width() + margin, abs(nextBlueValue - blueValue))
				
				except Exception as e:
					Message('Error', informativeText=str(e))

			
			if decomposeComponents:
				c.decompose()
		   
			if removeOverlap:
			   c.removeOverlap()

			drawBot.fill(glyphColor)
			
			if glyphOutline:
				drawBot.stroke(outlineColor)
				drawBot.strokeWidth(outlineThickness)

			if makeNodesOutlineColor == 1:
				onCurveStrokeColor = outlineColor
				onCurvePointColor = outlineColor
				offCurveStrokeColor = outlineColor
				offCurvePointColor = outlineColor
				handleBarColor = outlineColor

			pen = c.getPen()
			   
			drawBot.drawGlyph(c)

			if showNodes:

				for contour in c:

					for bPoint in contour.bPoints:
						
						if showNodes:
							
							with drawBot.savedState():
								x, y = bPoint.anchor
								drawBot.translate(x, y)
								drawBot.stroke(handleBarColor)
								drawBot.strokeWidth(outlineThickness)
								drawBot.line ((0,0), bPoint.bcpIn)
								drawBot.line ((0,0), bPoint.bcpOut)
				
					for e,segment in enumerate(contour):
						nextSegment = contour[(e + 1) % len(contour)]

						if segment.type != nextSegment.type:
							for point in segment:
								if point.type != 'offcurve':

									x = point.x
									y = point.y
									
									# Smooth Corner
									if point.smooth:
										self.drawNodes(x, y, s, smoothCornerNodeShape, smoothCornerPointColor, smoothCornerStrokeColor)
									# Corner Point
									else:
										self.drawNodes(x, y, s, cornerNodeShape, cornerPointColor, cornerStrokeColor)

						elif segment.type == 'curve' and nextSegment.type == 'curve':
							for point in segment:
								if point.type != 'offcurve':

									x = point.x
									y = point.y

									# Curve Point
									if point.smooth:
										self.drawNodes(x, y, s, onCurveNodeShape, onCurvePointColor, onCurveStrokeColor)
									# Corner Point
									else:
										self.drawNodes(x, y, s, cornerNodeShape, cornerPointColor, cornerStrokeColor)
						
						else:
							# Corner Point
							for point in segment:
								if point.type != 'offcurve':
									x = point.x 
									y = point.y 
									self.drawNodes(x, y, s, cornerNodeShape, cornerPointColor, cornerStrokeColor)

						for point in segment:

							x = point.x
							y = point.y

							# Offcurve Point
							if point.type == 'offcurve':
								drawBot.stroke(offCurveStrokeColor)
								drawBot.strokeWidth(outlineThickness)
								drawBot.fill(offCurvePointColor)

								self.drawNodes(x, y, r, offCurveNodeShape, offCurvePointColor, offCurveStrokeColor)
			
			if displayCoordinates:
				drawBot.stroke(None)
				drawBot.fill(coordinatesColor)
				drawBot.fontSize(i)	

				for contour in c:
					for segment in contour:
						for point in segment:
							
							if point.type != 'offcurve':
								drawBot.text(f'{point.x}, {point.y}',(point.x,point.y - s - 10),align='center',)
							
							else:
								drawBot.text(f'{point.x}, {point.y}',(point.x,point.y - s - 10),align='center',)

			pdf = drawBot.pdfImage()

			self.w.preview.setPDFDocument(pdf)

			drawBot.endDrawing()

	def export(self, sender):

		glyphSelection = self.w.controls.glyphSelection.get()
		glyphsToProcess = self.glyphsToProcess()

		exportPdf, exportSvg, exportPng = self.exportAs()
		
		if font.path:
			url = os.path.dirname(font.path)
			export = f'{url}/GlyphShowcaser'

			if not os.path.exists(export):
				os.makedirs(export)

		if exportPdf == 1:

			if glyphSelection == 0:
				for glyph in glyphsToProcess:
					drawBot.saveImage(f'{export}/{time}-GlyphShowcaser-{fontName}-{glyph.name}.pdf')  
			
			elif glyphSelection == 1:  
				drawBot.saveImage(f'{export}/{time}-GlyphShowcaser-{fontName}.pdf') 
				
		if exportSvg == 1:

			if glyphSelection == 0:
				for glyph in glyphsToProcess:
					drawBot.saveImage(f'{export}/{time}-GlyphShowcaser-{fontName}-{glyph.name}.svg')
			
			elif glyphSelection == 1:
				drawBot.saveImage(f'{export}/{time}-GlyphShowcaser-{fontName}-.svg')
			   
		if exportPng == 1:
			for glyph in glyphsToProcess:
				drawBot.saveImage(f'{export}/{time}-GlyphShowcaser-{fontName}-{glyph.name}.png', imageResolution=300)

	def close(self, sender):
		self.w.close()

	def destroy(self):
		self.w.close()

GlyphShowcaser()