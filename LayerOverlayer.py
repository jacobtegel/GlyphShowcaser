# menuTitle: Layer Overlayer

'''
Overlay Layers!
LayerOverlayer is a stripped down and modified version of GlyphShowcaser with the intent of overlaying all of your layers over each other. 
Whether that might be different versions, alternate drawings or something else, stack it and export it as PDF, SVG or PNG.

Jacob Tegel 2024-2025
'''

import drawBot
import os

from vanilla import *
from AppKit import NSColor, NSButton, NSView
from mojo.UI import Message
from mojo.pens import DecomposePointPen
from drawBot.ui.drawView import DrawView

from datetime import datetime

time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

font = CurrentFont()

if font is None:
	Message('Please open a font in RoboFont.')

else:
	try: 
		name = ( f'{font.info.familyName}-{font.info.styleName}')
		fontName = name.replace(' ', '-')
		fontPath = f'{os.path.dirname(font.path)}' 
	
	except Exception as e:
		Message('Error', informativeText = sr(e))

class LayerOverlayer:
	
	def __init__(self):
		self.winWidth = 1000
		self.winHeight = 1250
		self.sidebarWidth = 325
		self.sidebarHeight = 1135

		self.nodeStackSize = 0

		self.w = Window((self.winWidth, self.winHeight), 'Layer Overlayer', (100, 100))
		self.w.controls = Group((-self.sidebarWidth, 10, self.sidebarWidth, self.sidebarHeight))

		x1 = 10
		x2 = 160
		
		y = 10
		
		w1 = 160
		w2 = -10
		
		h = 20

		dy = h + 15

		t = 5

		# Glyph selection
		self.w.controls.glyphSelectionLabel = TextBox((x1, y, w1, h), 'Glyph Selection')
		self.w.controls.glyphSelection = VerticalRadioGroup((x2, y-2.5, w2, h * 3), ['Current Glyph', 'Selected Glyphs', 'All Glyphs'], callback = self.redraw)
		self.w.controls.glyphSelection.set(0)
		y += dy + h * 2

		# Artboard height
		self.w.controls.artboardHeightLabel = TextBox((x1, y, w1, h), 'Artboard Height')
		self.w.controls.artboardHeight = VerticalRadioGroup((x2, y-2.5, w2, h * 2), ['Font Height', 'Glyph Height'], callback = self.redraw)
		self.w.controls.artboardHeight.set(0)
		y += dy + h

		# margin
		self.w.controls.marginLabel = TextBox((x1, y, w1, h), 'Margin')
		self.w.controls.marginSlider = Slider((x2, y, w2-40, h + t), minValue = 0, maxValue = 500, value = 100, callback = self.marginSliderChanged)
		self.w.controls.marginValue = EditText((w2-35, y, w2, h + t), str(round(float(self.w.controls.marginSlider.get()))), callback = self.marginValueChanged, continuous = False)
		y += dy + t

		# showNodes
		self.w.controls.showNodesLabel = TextBox((x1, y, w1, h), 'Show Nodes')
		self.w.controls.showNodesCheck = CheckBox((x2, y, w2, h), '', callback = self.redraw, value = True)
		y += dy

		# cornerNodeShape
		self.w.controls.cornerNodeShapeLabel = TextBox((x1, y, w1, h), 'Corner Point Shape')
		self.w.controls.cornerNodeShape = VerticalRadioGroup((x2, y-2.5, w2, h * 4), ['Circle', 'Rectangle', 'Triangle', 'Cross'], callback = self.redraw)
		self.w.controls.cornerNodeShape.set(1)
		y += dy + 3 * h

		# smoothCornerNodeShape
		self.w.controls.smoothCornerNodeShapeLabel = TextBox((x1, y, w1, h), 'Smooth Corner Point')
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

		# bg Color
		self.w.controls.backgroundColorLabel = TextBox((x1, y, w1, h), 'Background Color')
		self.w.controls.backgroundColor = ColorWell((x2, y, w2, h + 15), callback = self.redraw, color = NSColor.colorWithRed_green_blue_alpha_(0, 0, 0, 0))
		y += dy + 15

		# fill color
		self.w.controls.glyphColorLabel = TextBox((x1, y, w1, h), 'Glyph Color')
		self.w.controls.glyphColor = ColorWell((x2, y, w2, h + 15), callback = self.redraw, color = NSColor.colorWithRed_green_blue_alpha_(1, 1, 1, 0))
		y += dy + 15

		# glyph Outline
		self.w.controls.glyphOutlineLabel = TextBox((x1, y, w1, h), 'Glyph Outline')
		self.w.controls.glyphOutlineCheck = CheckBox((x2, y, w2, h), '', callback = self.redraw, value = True)
		y += dy

		# use layer Color
		self.w.controls.useLayerColorLabel = TextBox((x1, y, w1, h), 'Use Layer Color')
		self.w.controls.useLayerColorCheck = CheckBox((x2, y, w2, h), '', callback = self.redraw, value = True)
		y += dy

		# fill Glyphs
		self.w.controls.fillGlyphsLabel = TextBox((x1, y, w1, h), 'Fill Glyphs')
		self.w.controls.fillGlyphsCheck = CheckBox((x2, y, w2, h), '', callback = self.redraw, value = False)
		y += dy

		# outlineColor
		self.w.controls.outlineColorLabel = TextBox((x1, y, w1, h), 'Outline Color')
		self.w.controls.outlineColor = ColorWell((x2, y, w2, h + 15), callback = self.redraw, color = NSColor.colorWithRed_green_blue_alpha_(0, 0, 0, 1))
		y += dy + 15

		# outline thickness
		self.w.controls.outlineThicknessLabel = TextBox((x1, y, w1, h), 'Outline Thickness')
		self.w.controls.outlineThicknessSlider = Slider((x2, y, w2-40, h + t), minValue = 1, maxValue = 5, value = 1, callback = self.outlineThicknessSliderChanged)
		self.w.controls.outlineThicknessValue = EditText((w2-35, y, w2, h + t), str(round(float(self.w.controls.outlineThicknessSlider.get()), 1)), callback = self.outlineThicknessValueChanged, continuous = False)
		y += dy + t

		# removeOverlap
		self.w.controls.removeOverlapLabel = TextBox((x1, y, w1, h), 'Remove Overlap')
		self.w.controls.removeOverlapCheck = CheckBox((x2, y, w2, h), '', callback = self.redraw, value = True)
		y += dy

		# opacity
		self.w.controls.opacityLabel = TextBox((x1, y, w1, h), 'Opacity')
		self.w.controls.opacitySlider = Slider((x2, y, w2-40, h + t), minValue = 0, maxValue = 1, value = 1, callback = self.opacitySliderChanged)
		self.w.controls.opacityValue = EditText((w2-35, y, w2, h + t), str(round(float(self.w.controls.opacitySlider.get()), 1)), callback = self.opacityValueChanged, continuous = False)
		y += dy + t

		# export as
		self.w.controls.exportText = TextBox((x1, y, w1, h), 'Export as:')
		self.w.controls.exportPdf = CheckBox((x2, y, w2, h), 'PDF')
		y += dy -10
		self.w.controls.exportSvg = CheckBox((x2, y, w2, h), 'SVG')
		y += dy -10
		self.w.controls.exportPng = CheckBox((x2, y, w2, h), 'PNG')
		y += dy

		# close
		# self.w.closeButton = Button(((-self.sidebarWidth - 10), - h - h / 2, self.sidebarWidth / 2 - 5, h), 'Close', callback=self.close)
		
		# path Control
		self.w.pathControl = PathControl(((-self.sidebarWidth - 10), - h - h / 2, self.sidebarWidth / 2 - 5, h), fontPath, pathStyle="popUp", callback=self.pathControlCallback)
		
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

	def opacitySliderChanged(self, sender):
		v = round(float(self.w.controls.opacitySlider.get()), 2)
		self.w.controls.opacityValue.set(str(v))
		self.redraw(sender)

	def opacityValueChanged(self, sender):
		v = round(float(self.w.controls.opacityValue.get()), 2)
		self.w.controls.opacitySlider.set(v)
		self.redraw(sender)

	def exportAs(self):

		exportPdf = self.w.controls.exportPdf.get()
		exportSvg = self.w.controls.exportSvg.get()
		exportPng = self.w.controls.exportPng.get()

		return exportPdf, exportSvg, exportPng

	def pathControlCallback(self, sender):
		
		self.redraw(sender)

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

		# Selected Glyphs    
		elif glyphSelection == 1:
			# print(font.selection)
			glyphsToProcess = [font[glyphName] for glyphName in font.selection]
			
		# All glyphs
		elif glyphSelection == 2:
			glyphsToProcess = [glyph for glyph in font]

		return glyphsToProcess

	def drawNodes(self, x, y, s, shape, pointColor, strokeColor):
		outlineThickness = self.w.controls.outlineThicknessSlider.get()
		drawBot.strokeWidth(outlineThickness)

		drawBot.fill(pointColor)
		drawBot.stroke(strokeColor)

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
		
		useLayerColor = self.w.controls.useLayerColorCheck.get()
		fillGlyphs = self.w.controls.fillGlyphsCheck.get()

		outlineColor = self.w.controls.outlineColor.get()
		outlineThickness = self.w.controls.outlineThicknessSlider.get()
		
		showNodes = self.w.controls.showNodesCheck.get()
		
		cornerNodeShape = self.w.controls.cornerNodeShape.get()
		smoothCornerNodeShape = self.w.controls.smoothCornerNodeShape.get()

		onCurveNodeShape = self.w.controls.onCurveNodeShape.get()
		
		offCurveNodeShape = self.w.controls.offCurveNodeShape.get()
		
		nodeSize = self.w.controls.nodeSizeSlider.get()
		nodeSizeRatio = self.w.controls.nodeSizeRatioSlider.get()
				
		removeOverlap = self.w.controls.removeOverlapCheck.get()
		
		# tintFonts = self.w.controls.tintFontsCheck.get()
		opacity = self.w.controls.opacitySlider.get()

		glyphsToProcess = self.glyphsToProcess()

		s = nodeSize
		r = nodeSizeRatio * nodeSize

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
			
			drawBot.fill(backgroundColor)
			drawBot.rect(0, 0, glyph.width + margin, height)

			if artboardHeight == 0:
				drawBot.translate(margin/2, -font.info.descender + (margin / 2))
			else:
				drawBot.translate(margin/2, -glyph.bounds[1] + margin / 2)

			glyphName = glyph.name  

			for layer in font.layers:
				
				if glyphName not in layer:
					continue  

				layerGlyph = layer[glyphName]

				c = layer[glyph.name].copy()
				
				if glyph.components:
					c.clear()
					layer[glyph].drawPoints(DecomposePointPen(layer[glyph].font, c.getPointPen()))

				if removeOverlap:
					c.removeOverlap()
				
				# Extract layer color
				layerColor = layer.color
				
				if useLayerColor and layerColor:
					red, green, blue, _ = layerColor
					outlineColor = NSColor.colorWithSRGBRed_green_blue_alpha_(red, green, blue, opacity)
				
				else:
					red, green, blue = outlineColor.redComponent(), outlineColor.greenComponent(), outlineColor.blueComponent()
					outlineColor = NSColor.colorWithSRGBRed_green_blue_alpha_(red, green, blue, opacity)
				
				drawBot.stroke(outlineColor)
				
				if fillGlyphs:
					
					if useLayerColor and layerColor:
						red, green, blue, _ = layerColor
						fillColor = NSColor.colorWithSRGBRed_green_blue_alpha_(red, green, blue, opacity)
					
					else:
						red, green, blue = glyphColor.redComponent(), glyphColor.greenComponent(), glyphColor.blueComponent()
						fillColor = NSColor.colorWithSRGBRed_green_blue_alpha_(red, green, blue, opacity)
						
					drawBot.fill(fillColor)
				
				else:
				    drawBot.fill(None)
				
				drawBot.strokeWidth(outlineThickness)
				
				pen = c.getPointPen()			   
				drawBot.drawGlyph(c)
			   
				if showNodes:

					for contour in c:

						for bPoint in contour.bPoints:
							
							with drawBot.savedState():
								x, y = bPoint.anchor
								drawBot.translate(x, y)
								drawBot.line ((0,0), bPoint.bcpIn)
								drawBot.line ((0,0), bPoint.bcpOut)
					
						for e, segment in enumerate(contour):
							
							nextSegment = contour[(e + 1) % len(contour)]

							if segment.type != nextSegment.type:
								for point in segment:
									if point.type != 'offcurve':

										x = point.x
										y = point.y
										
										# Smooth Corner
										if point.smooth:
											self.drawNodes(x, y, s, smoothCornerNodeShape, glyphColor, outlineColor)
										# Corner Point
										else:
											self.drawNodes(x, y, s, cornerNodeShape, glyphColor, outlineColor)

							elif segment.type == 'curve' and nextSegment.type == 'curve':
								for point in segment:
									if point.type != 'offcurve':

										x = point.x
										y = point.y

										# Curve Point
										if point.smooth:
											self.drawNodes(x, y, s, onCurveNodeShape, glyphColor, outlineColor)
										# Corner Point
										else:
											self.drawNodes(x, y, s, cornerNodeShape, glyphColor, outlineColor)
							
							else:
								# Corner Point
								for point in segment:
									if point.type != 'offcurve':
										x = point.x 
										y = point.y 
										self.drawNodes(x, y, s, cornerNodeShape, glyphColor, outlineColor)

							for point in segment:

								x = point.x
								y = point.y

								# Offcurve Point
								if point.type == 'offcurve':

									self.drawNodes(x, y, r, offCurveNodeShape, glyphColor, outlineColor)
		
		pdf = drawBot.pdfImage()

		self.w.preview.setPDFDocument(pdf)

		drawBot.endDrawing()

	def export(self, sender):

		glyphSelection = self.w.controls.glyphSelection.get()
		glyphsToProcess = self.glyphsToProcess()

		exportPdf, exportSvg, exportPng = self.exportAs()
		
		export = f"{fontPath}/LayerOverlayer"
			
		if not os.path.exists(export):
			os.makedirs(export)

		if exportPdf == 1:

			if glyphSelection == 0:
				for glyph in glyphsToProcess:
					drawBot.saveImage(f'{export}/{time}-LayerOverlayer-{fontName}-{glyph.name}.pdf')  
			
			elif glyphSelection == 1:  
				drawBot.saveImage(f'{export}/{time}-LayerOverlayer-{fontName}.pdf') 
				
		if exportSvg == 1:

			if glyphSelection == 0:
				for glyph in glyphsToProcess:
					drawBot.saveImage(f'{export}/{time}-LayerOverlayer-{fontName}-{glyph.name}.svg')
			
			elif glyphSelection == 1:
				drawBot.saveImage(f'{export}/{time}-LayerOverlayer-{fontName}-.svg')
			   
		if exportPng == 1:
			for glyph in glyphsToProcess:
				drawBot.saveImage(f'{export}/{time}-LayerOverlayer-{fontName}-{glyph.name}.png', imageResolution=300)

	def close(self, sender):
		self.w.close()

	def destroy(self):
		self.w.close()

LayerOverlayer()