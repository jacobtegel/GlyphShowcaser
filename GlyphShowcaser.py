# Drawbot

import AppKit
import os
import ezui

from datetime import datetime
from mojo.roboFont import CurrentFont, CurrentGlyph, RGlyph
from drawBot import *


time = datetime.now().strftime('%Y-%m-%d-%H-%M:')

margin = 100

t = FormattedString()
t.fontSize(72)

font = CurrentFont()

height = (font.info.ascender + margin) + -(font.info.descender - (margin / 2))

name = f"{font.info.familyName}-{font.info.styleName}"

fontName = name.replace(" ","-")


########## BEGIN EZUI ##########

########## END EZUI ##########


########## BEGIN VARIABLES ##########

Variable([

        dict(name="glyphSelection", ui="RadioGroup", args=dict(titles=['Current Glyph', 'All Glyphs'], isVertical=True)),
        
        dict(name="margin", ui="Slider", args=dict(value=100, minValue=0, maxValue=500)),
    
        dict(name="backgroundColor", ui="ColorWell", args=dict(color=AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(1, 1, 1, 0))), 

        dict(name="glyphColor", ui="ColorWell", args=dict(color=AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(1, 1, 1, 0))),
        
        dict(name="glyphOutline", ui="CheckBox", args=dict(value=True)),
        
        dict(name="outlineColor", ui="ColorWell"),
        
        dict(name="showNodes", ui="CheckBox", args=dict(value=True)),
        
        dict(name="nodeShape", ui="RadioGroup", args=dict(titles=['Circle', 'Rectangle', 'Cross'], isVertical=True), value = 0),
        
        dict(name="nodeSize", ui="Slider", args=dict(value=5, minValue=1, maxValue=10)),
        
        dict(name="onCurveStroke", ui="ColorWell"),
        dict(name="onCurveColor", ui="ColorWell"),
        
        dict(name="offCurveStroke", ui="ColorWell"),
        dict(name="offCurveColor", ui="ColorWell"),
        
        dict(name="bcpLineStroke", ui="ColorWell"),
                
        dict(name="removeOverlap", ui="CheckBox"),
        
        dict(name="displayCoordinates", ui="CheckBox"),
        
        dict(name="exportAs", ui="RadioGroup", args=dict(titles=['PDF', 'SVG', 'PNG'], isVertical=True))
        
        ], globals())

s = nodeSize

# print(nodeShape)

########## END VARIABLES ##########


##########
# Determine which glyphs to process based on GlyphSelection
glyphsToProcess = []

# Current glyph
if glyphSelection == 0:
    glyphsToProcess = [CurrentGlyph()]
    
# All glyphs (with contours)
elif glyphSelection == 1:
    glyphsToProcess = [glyph for glyph in font if glyph.contours]

# Process selected glyph/s
for glyph in glyphsToProcess:
    # Skip empty or None glyphs
    if glyph is None or not glyph.contours:
        continue
##########

    g = glyph.getLayer('foreground')
    
    # create orhpan child of g
    c = g.copy()     

    newPage(glyph.width + margin, height + margin)
    
    fill(backgroundColor)
    rect(0, 0, glyph.width + margin, height + margin)
    
    translate(margin/2, -font.info.descender + (margin / 2))
    
    fill(glyphColor)
    
    if glyphOutline:
        stroke(outlineColor)
        strokeWidth(1)
   
    if removeOverlap:
        c.removeOverlap()

    pen = c.getPen()
       
    drawGlyph(c)
           
    for contour in c:

        for bPoint in contour.bPoints:
            
            if showNodes:
                
                with savedState():
                    x, y = bPoint.anchor
                    translate(x, y)
                    stroke(bcpLineStroke)
                    strokeWidth(1)
                    line ((0,0), bPoint.bcpIn)
                    line ((0,0), bPoint.bcpOut)
    
        for segment in contour:
           
            for point in segment:
                
                stroke(None)
                fill(1,.5,.5)
                
                # s = 10
                
                if showNodes:
                
                    if point.type == "offcurve":
                        stroke(offCurveStroke)
                        fill(offCurveColor)
                    else:
                        stroke(onCurveStroke)
                        strokeWidth(1)
                        fill(onCurveColor)
  
                    if nodeShape == 0:
                        oval(point.x-s, point.y-s, s*2, s*2)
                    
                    elif nodeShape == 1:
                        rect(point.x-s, point.y-s, s*2, s*2)
                        
                    elif nodeShape == 2:
                        
                        line((point.x-s, point.y-s), (point.x+s, point.y+s))
                        line((point.x-s, point.y+s), (point.x+s, point.y-s))
                
                # shape[nodeShape](point.x-s, point.y-s, s*2, s*2)
                
                if displayCoordinates:
                    stroke(None)
                    fill(0)
                    text(f"{point.x}, {point.y}",(point.x,point.y-s-10),align="center",)


# print(fontName)

if font is not None and font.path:
    font_path = os.path.dirname(font.path) #Get Folder in which the font is
    output_folder = f"{font_path}/Showcaser-Output" # create output folder inside of that folder

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

# print(font_path)
# print(output_folder)
# print(time)

if exportAs == 0:

    if glyphSelection == 0:
         saveImage(f"{output_folder}/{time}-GlyphShowcaser-{fontName}-{glyph.name}.pdf")  
    
    elif glyphSelection == 1:  
         saveImage(f"{output_folder}/{time}-GlyphShowcaser-{fontName}.pdf") 
        
if exportAs == 1:

    if glyphSelection == 0:
        saveImage(f"{output_folder}/{time}-GlyphShowcaser-{fontName}-{glyph.name}.svg")
    
    elif glyphSelection == 1:
        saveImage(f"{output_folder}/{time}-GlyphShowcaser-{fontName}-.svg")
       
if exportAs == 2:
    saveImage(f"{output_folder}/{time}-GlyphShowcaser-{fontName}-{glyph.name}.png")      