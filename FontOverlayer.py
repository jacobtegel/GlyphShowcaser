# Drawbot

'''
Overlay Fonts!

FontOverlayer is another modified version of GlyphShowcaser, using the LayerOverlayer logic, but overlaying currently open font files with each other. Multiple styles of one Family or variously different fonts. Stack it and save it.

Jacob Tegel 2024-2025
'''

import AppKit
import os
from datetime import datetime
from mojo.roboFont import CurrentFont, CurrentGlyph, RGlyph
from mojo.pens import DecomposePointPen
from drawBot import *

time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
margin = 100

fonts = AllFonts()

if not fonts:
	raise ValueError("No fonts open.")

for f in fonts:
	print(f.info.familyName, f.info.styleName)

fontHeight = (fonts[0].info.ascender + margin) + -(fonts[0].info.descender - (margin / 2))
name = f"{fonts[0].info.familyName}-{fonts[0].info.styleName}"
fontName = name.replace(" ","-")

Variable([

		dict(name="glyphSelection", ui="RadioGroup", args=dict(titles=['Current Glyph', 'Selected Glyphs', 'All Glyphs'], isVertical=True)),
		
		dict(name="glyphAlign", ui="RadioGroup", args=dict(titles=['left', 'center', 'right'], isVertical=True)),
		
		dict(name="margin", ui="Slider", args=dict(value=10, minValue=0, maxValue=500)),
	
		dict(name="artboardHeight", ui="RadioGroup", args=dict(titles=['Font Height', 'Glyph Height'], isVertical=True)),

		dict(name="showNodes", ui="CheckBox", args=dict(value=True)),
	 
		dict(name="oncurveNodeShape", ui="RadioGroup", args=dict(titles=['Circle', 'Rectangle', 'Cross'], isVertical=True), value = 0),
		
		dict(name="offcurveNodeShape", ui="RadioGroup", args=dict(titles=['Circle', 'Rectangle', 'Cross'], isVertical=True), value = 0),
		
		dict(name="nodeSize", ui="Slider", args=dict(value=5, minValue=1, maxValue=10)),
		
		dict(name="nodeRatio", ui="Slider", args=dict(value=1, minValue=0, maxValue=1)),
		
		dict(name="backgroundColor", ui="ColorWell", args=dict(color=AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(1, 1, 1, 0))),
		
		dict(name="strokeColor", ui="ColorWell", args=dict(color=AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(0, 0, 0, 1))),
		
		dict(name="outlineThickness", ui="Slider", args=dict(value=1, minValue=1, maxValue=10)),
				
		dict(name="removeOverlap", ui="CheckBox", args=dict(value=True)),
				
		dict(name="tintFonts", ui="CheckBox", args=dict(value=True)),
		
		dict(name="tintIntensity", ui="Slider", args=dict(value=.8, minValue=0, maxValue=1)),
	
		dict(name="exportAs", ui="RadioGroup", args=dict(titles=['PDF', 'SVG', 'PNG'], isVertical=True))
		
		], globals())

s = nodeSize
r = nodeRatio * nodeSize

glyphNamesToProcess = []

if glyphSelection == 0:
	glyphNamesToProcess = [CurrentGlyph().name]

elif glyphSelection == 1:
	glyphNamesToProcess = list(fonts[0].selectedGlyphNames)

elif glyphSelection == 2:
	glyphNamesToProcess = [g.name for g in fonts[0] if g.contours]

for glyphName in glyphNamesToProcess:
	
	glyphs = []
	for font in fonts:
		if glyphName in font and font[glyphName].contours:
			glyphs.append(font[glyphName])
	if not glyphs:
		continue

	font = fonts[0]
	refGlyph = glyphs[0]
	
	print(refGlyph)

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

	newPage(pwidth, pheight)
	fill(backgroundColor)
	rect(0, 0, pwidth, pheight)
	
	baseR, baseG, baseB, baseA = strokeColor.redComponent(), strokeColor.greenComponent(), strokeColor.blueComponent(), strokeColor.alphaComponent()
	numFonts = len(fonts)

	for idx, glyph in enumerate(glyphs):
		
		c = RGlyph()
		pen = c.getPointPen()
		decomposePen = DecomposePointPen(glyph.layer, pen)
		glyph.drawPoints(decomposePen)
		if c is None or not c.contours:
			continue
		if removeOverlap:
			c.removeOverlap()
		
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

		with savedState():
			if artboardHeight == 0:
				translate(xOffset, -font.info.descender + (margin / 2))
			else:
				translate(xOffset, -yMin + (margin / 2))
		
			factor = (numFonts - 1 - idx) / max(1, (numFonts - 1)) * tintIntensity  # 0.8 (lightest) to 0.0 (base color)
			
			if tintFonts:
				tintedColor = AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(
					baseR + (1.0 - baseR) * factor,
					baseG + (1.0 - baseG) * factor,
					baseB + (1.0 - baseB) * factor,
					baseA + (1.0 - baseA) * factor
				)
			else:
				tintedColor = strokeColor
			
			fill(None)
			stroke(tintedColor)
			strokeWidth(outlineThickness)
			drawGlyph(c)
			for contour in c:
				for bPoint in contour.bPoints:
					with savedState():
						x, y = bPoint.anchor
						translate(x, y)
						
						if showNodes:
							stroke(tintedColor)
							strokeWidth(1)

							line((0,0), bPoint.bcpIn)
							line((0,0), bPoint.bcpOut)
							
						else:
							continue
							
				for segment in contour:
					for point in segment:
					
						if showNodes:
					
							if point.type == "offcurve":
								stroke(tintedColor)
								strokeWidth(1)
								fill(tintedColor)
								
								if offcurveNodeShape == 0:
								
									oval(point.x-r, point.y-r, r*2, r*2)
							
								elif offcurveNodeShape == 1:
								
									rect(point.x-r, point.y-r, r*2, r*2)
								
								elif offcurveNodeShape == 2:
								
									line((point.x-r, point.y-r), (point.x+r, point.y+r))
									line((point.x-r, point.y+r), (point.x+r, point.y-r))
									
							else:
								stroke(tintedColor)
								strokeWidth(1)
								fill(tintedColor)
		  
								if oncurveNodeShape == 0:
								
									oval(point.x-s, point.y-s, s*2, s*2)
							
								elif oncurveNodeShape == 1:
								
									rect(point.x-s, point.y-s, s*2, s*2)
								
								elif oncurveNodeShape == 2:
								
									line((point.x-s, point.y-s), (point.x+s, point.y+s))
									line((point.x-s, point.y+s), (point.x+s, point.y-s))
								

if fonts[0] is not None and fonts[0].path:
	font_path = os.path.dirname(fonts[0].path)
	output_folder = f"{font_path}/FontOverlayer-Output"
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)

if exportAs == 0:

	if glyphSelection == 0:
		 saveImage(f"{output_folder}/{time}-FontOverlayer-{fontName}-{glyph.name}.pdf")

	else:
		 saveImage(f"{output_folder}/{time}-FontOverlayer-{fontName}.pdf")
	
if exportAs == 1:

	if glyphSelection == 0:
		saveImage(f"{output_folder}/{time}-FontOverlayer-{fontName}-{glyph.name}.svg", multipage = True)

	else:
		saveImage(f"{output_folder}/{time}-FontOverlayer-{fontName}.svg", multipage = True)
   
if exportAs == 2:
	
	if glyphSelection == 0:
		saveImage(f"{output_folder}/{time}-FontOverlayer-{fontName}-{glyph.name}.png", multipage = True)
	
	else:
		saveImage(f"{output_folder}/{time}-FontOverlayer-{fontName}.png", multipage = True)
