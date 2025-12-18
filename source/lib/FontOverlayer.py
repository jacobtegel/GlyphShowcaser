# menuTitle: Font Overlayer

'''
Overlay Fonts!
FontOverlayer is a modified version of GlyphShowcaser created to overlay open font files with each other. 
Multiple styles of one Family or variously different fonts. Stack it and export it as PDF, SVG or PNG; change colours, Node Shapes and more.

Jacob Tegel 2024-2025
'''
import drawBot
import os

from vanilla import *
from AppKit import *
from mojo.UI import Message
from mojo.pens import DecomposePointPen
from drawBot.ui.drawView import DrawView

from datetime import datetime

time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

fonts = AllFonts()

if not fonts:
	Message('Error', informativeText = 'No fonts open.')

else:
	try:
		name = f"{fonts[0].info.familyName}-{fonts[0].info.styleName}-{fonts[-1].info.familyName}-{fonts[-1].info.styleName}"
		fontName = name.replace(" ","-")
		fontPath = f'{os.path.dirname(fonts[0].path)}'

	except Exception as e:
		Message('Error', informativeText = sr(e))


class FontOverlayer:

	def __init__(self):

		self.winWidth = 1000
		self.winHeight = 1250
		self.sidebarWidth = 325
		self.sidebarHeight = 1170

		self.nodeStackSize = 0

		self.w = Window((self.winWidth, self.winHeight), 'Font Overlayer', (100, 100))
		self.w.controls = Group((-self.sidebarWidth, 10, self.sidebarWidth, self.sidebarHeight))

		x1 = 10
		x2 = 160
		
		y = 10
		
		w1 = 160
		w2 = -10
		
		h = 20

		dy = h + 15

		t = 5

		# glyph selection
		self.w.controls.glyphSelectionLabel = TextBox((x1, y, w1, h), 'Glyph Selection')
		self.w.controls.glyphSelection = VerticalRadioGroup((x2, y-2.5, w2, h * 3), ['Current Glyph', 'Selected Glyphs', 'All Glyphs'], callback = self.redraw)
		self.w.controls.glyphSelection.set(0)
		y += dy + h * 2

		# artboard Height
		self.w.controls.artboardHeightLabel = TextBox((x1, y, w1, h), 'Artboard Height')
		self.w.controls.artboardHeight = VerticalRadioGroup((x2, y-2.5, w2, h * 2), ['Font Height', 'Glyph Height'], callback = self.redraw)
		self.w.controls.artboardHeight.set(0)
		y += dy + h

		# glyph Alignment
		self.w.controls.glyphAlignLabel = TextBox((x1, y, w1, h), 'Glyph Alignment')
		self.w.controls.glyphAlign = VerticalRadioGroup((x2, y-2.5, w2, h * 3), ['left', 'center', 'right'], callback = self.redraw)
		self.w.controls.glyphAlign.set(1)
		y += dy + h * 2

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

		# tint fonts
		self.w.controls.tintFontsLabel = TextBox((x1, y, w1, h), 'Tint Fonts')
		self.w.controls.tintFontsCheck = CheckBox((x2, y, w2, h), '', callback = self.redraw, value = True)
		y += dy

		# tint intensity
		self.w.controls.tintIntensityLabel = TextBox((x1, y, w1, h), 'Tint Intensity')
		self.w.controls.tintIntensitySlider = Slider((x2, y, w2-40, h + t), minValue = 0, maxValue = 1, value = .5, callback = self.tintIntensitySliderChanged)
		self.w.controls.tintIntensityValue = EditText((w2-35, y, w2, h + t), str(round(float(self.w.controls.tintIntensitySlider.get()), 1)), callback = self.tintIntensityValueChanged, continuous = False)
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
		#self.w.closeButton = Button(((-self.sidebarWidth - 10), - h - h / 2, self.sidebarWidth / 2 - 5, h), 'Close', callback=self.close)
		
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

	def tintIntensitySliderChanged(self, sender):
		v = round(float(self.w.controls.tintIntensitySlider.get()), 2)
		self.w.controls.tintIntensityValue.set(str(v))
		self.redraw(sender)

	def tintIntensityValueChanged(self, sender):
		v = round(float(self.w.controls.tintIntensityValue.get()), 2)
		self.w.controls.tintIntensitySlider.set(v)
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
			glyphsToProcess = [CurrentGlyph().name]

		# Selected glyphs    
		elif glyphSelection == 1:
			glyphsToProcess = [fonts[0].selectedGlyphNames]

		# All glyphs
		elif glyphSelection == 2:
			glyphsToProcess = [glyph.name for glyph in fonts[0] if glyph.contours]

		return glyphsToProcess

	def drawNodes(self, x, y, s, shape, pointColor, strokeColor, idx):
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

		glyphAlign = self.w.controls.glyphAlign.get()
		
		backgroundColor = self.w.controls.backgroundColor.get()
		glyphColor = self.w.controls.glyphColor.get()
		glyphOutline = self.w.controls.glyphOutlineCheck.get()
		
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
		
		tintFonts = self.w.controls.tintFontsCheck.get()
		tintIntensity = self.w.controls.tintIntensitySlider.get()

		glyphsToProcess = self.glyphsToProcess()
		
		s = nodeSize
		r = nodeSizeRatio * s

		fontHeight = (fonts[0].info.ascender + margin) + -(fonts[0].info.descender - (margin / 2))

		# Drawing
		drawBot.newDrawing()

		for glyph in glyphsToProcess:
	
			glyphs = []
			for font in reversed(fonts):
				try: 
					if glyph in font and font[glyph] is not None:
						glyphs.append(font[glyph])
				except Exception as e:
					Message('Error', informativeText = str(e))
			
			if not glyphs:
				continue

			font = fonts[0]
			refGlyph = glyphs[0]
			
			bounds = refGlyph.bounds
			
			if bounds:
				xMin, yMin, xMax, yMax = bounds
			else:
				xMin, yMin, xMax, yMax = 0, 0, refGlyph.width, 0
			
			glyphWidth = refGlyph.width
			glyphHeight = abs(yMax - yMin)
			
			if artboardHeight == 0:
				height = (font.info.ascender + margin) + -(font.info.descender - (margin / 2))
			else:
				height = (glyphHeight + margin)
			
			pwidth = glyphWidth + margin
			pheight = height

			# Alignment offset
			if glyphAlign == 0:  # left
				xOffset = margin / 2 - xMin
			elif glyphAlign == 1:  # center
				xOffset = (pwidth - (xMax - xMin)) / 2 - xMin
			elif glyphAlign == 2:  # right
				xOffset = pwidth - (xMax - xMin) - xMin - margin / 2
			else:
				xOffset = margin / 2 - xMin

			drawBot.newPage(pwidth, pheight)
			drawBot.fill(backgroundColor)
			drawBot.rect(0, 0, pwidth, pheight)
			
			glyphBaseR, glyphBaseG, glyphBaseB, glyphBaseA = glyphColor.redComponent(), glyphColor.greenComponent(), glyphColor.blueComponent(), glyphColor.alphaComponent()
			strokeBaseR, strokeBaseG, strokeBaseB, strokeBaseA = outlineColor.redComponent(), outlineColor.greenComponent(), outlineColor.blueComponent(), outlineColor.alphaComponent()
			backgroundBaseR, backgroundBaseG, backgroundBaseB, backgroundBaseA = backgroundColor.redComponent(), backgroundColor.greenComponent(), backgroundColor.blueComponent(), backgroundColor.alphaComponent()
			
			numFonts = len(fonts)

			for idx, glyph in enumerate(glyphs):
				
				c = glyph.copy()
				
				if glyph.components:
					c.clear()
					glyph.drawPoints(DecomposePointPen(glyph.font, c.getPointPen()))

				if removeOverlap:
					c.removeOverlap()

				pen = c.getPointPen()

				if c is None:
					continue
				
				# Calculate bounds and alignment for this glyph
				bounds = c.bounds
				if bounds:
					xMin, yMin, xMax, yMax = bounds
				else:
					xMin, yMin, xMax, yMax = 0, 0, c.width, 0

				# Alignment offset for this glyph
				if glyphAlign == 0:  # left
					xOffset = margin / 2 - xMin
				elif glyphAlign == 1:  # center
					xOffset = (pwidth - (xMax - xMin)) / 2 - xMin
				elif glyphAlign == 2:  # right
					xOffset = pwidth - (xMax - xMin) - xMin - margin / 2
				else:
					xOffset = margin / 2 - xMin

				# Save and restore state for each glyph
				with drawBot.savedState():
					
					if artboardHeight == 0:
						drawBot.translate(xOffset, -font.info.descender + (margin / 2))
					
					else:
						drawBot.translate(xOffset, -yMin + (margin / 2))
				
					# lightest to 0.0 (base color)
					factor = (numFonts - 1 - idx) / max(1, (numFonts - 1)) * tintIntensity  
					
					# fade to black if glyphBase is white
					if glyphBaseR > 0.95 and glyphBaseG > 0.95 and glyphBaseB > 0.95 and backgroundBaseA != 0:
						glyphTargetR, glyphTargetG, glyphTargetB, glyphTargetA = backgroundBaseR, backgroundBaseG, backgroundBaseB, backgroundBaseA
					
					elif backgroundBaseA != 0:
						glyphTargetR, glyphTargetG, glyphTargetB, glyphTargetA = backgroundBaseR, backgroundBaseG, backgroundBaseB, backgroundBaseA

					else:
						glyphTargetR, glyphTargetG, glyphTargetB, glyphTargetA = 1.0, 1.0, 1.0, 1.0

					# fade to black if glyphBase is white
					if strokeBaseR > 0.95 and strokeBaseG > 0.95 and strokeBaseB > 0.95 and backgroundBaseA != 0:
						strokeTargetR, strokeTargetG, strokeTargetB, strokeTargetA = backgroundBaseR, backgroundBaseG, backgroundBaseB, backgroundBaseA
					
					elif backgroundBaseA != 0:
						strokeTargetR, strokeTargetG, strokeTargetB, strokeTargetA = backgroundBaseR, backgroundBaseG, backgroundBaseB, backgroundBaseA
					
					else:
						strokeTargetR, strokeTargetG, strokeTargetB, strokeTargetA = 1.0, 1.0, 1.0, 1.0

					# do not fade transparency if transparency is 0
					if glyphBaseA == 0:
						glyphTargetA = 0
					if strokeBaseA == 0:
						strokeTargetA = 0

					if tintFonts:
						glyphColor = NSColor.colorWithSRGBRed_green_blue_alpha_(
							glyphBaseR + (glyphTargetR - glyphBaseR) * factor,
							glyphBaseG + (glyphTargetG - glyphBaseG) * factor,
							glyphBaseB + (glyphTargetB - glyphBaseB) * factor,
							# glyphBaseA
							# glyphBaseA * (glyphTargetA - factor)
							glyphBaseA + (glyphTargetA - glyphBaseA) * factor
						)

						outlineColor = NSColor.colorWithSRGBRed_green_blue_alpha_(
							strokeBaseR + (strokeTargetR - strokeBaseR) * factor,
							strokeBaseG + (strokeTargetG - strokeBaseG) * factor,
							strokeBaseB + (strokeTargetB - strokeBaseB) * factor,
							# strokeBaseA
							# strokeBaseA * (strokeTargetA - factor)
							strokeBaseA + (strokeTargetA - strokeBaseA) * factor
						)

					else:
						glyphColor = glyphColor
						outlineColor = outlineColor
					
					drawBot.fill(glyphColor)
					
					if glyphOutline:
						outlineColor = outlineColor
					else:
						outlineColor = None
					
					drawBot.stroke(outlineColor)
					drawBot.strokeWidth(outlineThickness)				
					
					drawBot.drawGlyph(c)
					
					if showNodes:

						for contour in c:

							for bPoint in contour.bPoints:
								
								with drawBot.savedState():
									x, y = bPoint.anchor
									drawBot.translate(x, y)
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
												self.drawNodes(x, y, s, smoothCornerNodeShape, glyphColor, outlineColor, idx)
											# Corner Point
											else:
												self.drawNodes(x, y, s, cornerNodeShape, glyphColor, outlineColor, idx)

								elif segment.type == 'curve' and nextSegment.type == 'curve':
									for point in segment:
										if point.type != 'offcurve':

											x = point.x
											y = point.y

											# Curve Point
											if point.smooth:
												self.drawNodes(x, y, s, onCurveNodeShape, glyphColor, outlineColor, idx)
											# Corner Point
											else:
												self.drawNodes(x, y, s, cornerNodeShape, glyphColor, outlineColor, idx)
								
								else:
									# Corner Point
									for point in segment:
										if point.type != 'offcurve':
											x = point.x 
											y = point.y 
											self.drawNodes(x, y, s, cornerNodeShape, glyphColor, outlineColor, idx)

								for point in segment:

									x = point.x
									y = point.y

									# Offcurve Point
									if point.type == 'offcurve':

										self.drawNodes(x, y, r, offCurveNodeShape, glyphColor, outlineColor, idx)

		pdf = drawBot.pdfImage()

		self.w.preview.setPDFDocument(pdf)

		drawBot.endDrawing()

	def export(self, sender):

		url = self.w.pathControl.get()

		glyphSelection = self.w.controls.glyphSelection.get()
		glyphsToProcess = self.glyphsToProcess()

		exportPdf, exportSvg, exportPng = self.exportAs()
		
		export = f"{url}/FontOverlayer"
		
		if not exportPdf and not exportSvg and not exportPng:
			pass

		else:
			try:

				if not os.path.exists(export):
					os.makedirs(export)

				if exportPdf == 1:

					if glyphSelection == 0:
						for glyph in glyphsToProcess:
							drawBot.saveImage(f'{export}/{time}-FontOverlayer-{fontName}-{glyph}.pdf')  
					
					elif glyphSelection == 1:  
						drawBot.saveImage(f'{export}/{time}-FontOverlayer-{fontName}.pdf') 
						
				if exportSvg == 1:

					if glyphSelection == 0:
						for glyph in glyphsToProcess:
							drawBot.saveImage(f'{export}/{time}-FontOverlayer-{fontName}-{glyph}.svg')
					
					elif glyphSelection == 1:
						drawBot.saveImage(f'{export}/{time}-FontOverlayer-{fontName}-.svg')
					   
				if exportPng == 1:
					for glyph in glyphsToProcess:
						drawBot.saveImage(f'{export}/{time}-FontOverlayer-{fontName}-{glyph}.png', imageResolution=300)
				
			except Exception as e:
				Message(f'Export Failed', informativeText = str(e))

	def close(self, sender):
		self.w.close()

	def destroy(self):
		self.w.close()

FontOverlayer()