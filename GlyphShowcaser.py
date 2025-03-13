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

fontHeight = (font.info.ascender + margin) + -(font.info.descender - (margin / 2))

name = f"{font.info.familyName}-{font.info.styleName}"

fontName = name.replace(" ","-")


########## BEGIN EZUI ##########

########## END EZUI ##########


########## BEGIN VARIABLES ##########

Variable([

        dict(name="glyphSelection", ui="RadioGroup", args=dict(titles=['Current Glyph', 'Selected Glyphs', 'All Glyphs'], isVertical=True)),
        
        dict(name="margin", ui="Slider", args=dict(value=100, minValue=0, maxValue=500)),
    
        dict(name="artboardHeight", ui="RadioGroup", args=dict(titles=['Font Height', 'Glyph Height'], isVertical=True)),
    
        dict(name="backgroundColor", ui="ColorWell", args=dict(color=AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(1, 1, 1, 0))), 

        dict(name="glyphColor", ui="ColorWell", args=dict(color=AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(1, 1, 1, 0))),
        
        dict(name="glyphOutline", ui="CheckBox", args=dict(value=True)),
        
        dict(name="outlineColor", ui="ColorWell"),
        
        dict(name="showNodes", ui="CheckBox", args=dict(value=True)),
        
        dict(name="oncurveNodeShape", ui="RadioGroup", args=dict(titles=['Circle', 'Rectangle', 'Cross'], isVertical=True), value = 0),
        
        dict(name="offcurveNodeShape", ui="RadioGroup", args=dict(titles=['Circle', 'Rectangle', 'Cross'], isVertical=True), value = 0),
        
        dict(name="nodeSize", ui="Slider", args=dict(value=5, minValue=1, maxValue=10)),
        
        dict(name="nodeRatio", ui="Slider", args=dict(value=1, minValue=0, maxValue=1)),
        
        dict(name="onCurveStroke", ui="ColorWell"),
        dict(name="onCurveColor", ui="ColorWell"),
        
        dict(name="offCurveStroke", ui="ColorWell"),
        dict(name="offCurveColor", ui="ColorWell"),
        
        dict(name="handleStroke", ui="ColorWell"),
                
        dict(name="removeOverlap", ui="CheckBox"),
        
        dict(name="displayCoordinates", ui="CheckBox"),
        
        dict(name="coordinatesColor", ui="ColorWell"),
        
        dict(name="exportAs", ui="RadioGroup", args=dict(titles=['PDF', 'SVG', 'PNG'], isVertical=True))
        
        ], globals())

s = nodeSize
r = nodeRatio * nodeSize

# print(nodeShape)

########## END VARIABLES ##########


##########
# Determine which glyphs to process based on GlyphSelection
glyphsToProcess = []

# Current glyph
if glyphSelection == 0:
    glyphsToProcess = [CurrentGlyph()]

# Selected Glyphs    
elif glyphSelection == 1:
    # print(font.selection)
    glyphsToProcess = [font[glyphName] for glyphName in font.selection]
    
# All glyphs (with contours)
elif glyphSelection == 2:
    glyphsToProcess = [glyph for glyph in font]
    
print(glyphsToProcess)

# Process selected glyph/s
for glyph in glyphsToProcess:
    # Skip empty or None glyphs
    if glyph is None or not glyph.contours:
        continue
##########

    # print(glyph.bounds)
    glyphHeight = abs(glyph.bounds[1]-glyph.bounds[3])
    # print(glyphHeight)
    
    if artboardHeight == 0:
        height = (font.info.ascender + margin) + -(font.info.descender - (margin / 2))
    else:
        height = (glyphHeight + margin)
        
    newPage(glyph.width + margin, height)
    
    g = glyph.getLayer('foreground')
    
    # create orhpan child of g
    c = g.copy()     

    
    
    fill(backgroundColor)
    rect(0, 0, glyph.width + margin, height + margin)
    
    if artboardHeight == 0:
        translate(margin/2, -font.info.descender + (margin / 2))
    else:
        translate(margin/2, -glyph.bounds[1] + margin / 2)
    
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
                    stroke(handleStroke)
                    strokeWidth(1)
                    line ((0,0), bPoint.bcpIn)
                    line ((0,0), bPoint.bcpOut)
    
        for segment in contour:
           
            for point in segment:
                
                # stroke(None)
                # fill(1,.5,.5)
                
                # s = 10
                
                if showNodes:
                
                    if point.type == "offcurve":
                        stroke(offCurveStroke)
                        fill(offCurveColor)
                        
                        if offcurveNodeShape == 0:
                        
                            oval(point.x-r, point.y-r, r*2, r*2)
                    
                        elif offcurveNodeShape == 1:
                        
                            rect(point.x-r, point.y-r, r*2, r*2)
                        
                        elif offcurveNodeShape == 2:
                        
                            line((point.x-r, point.y-r), (point.x+r, point.y+r))
                            line((point.x-r, point.y+r), (point.x+r, point.y-r))
                            
                    else:
                        stroke(onCurveStroke)
                        strokeWidth(1)
                        fill(onCurveColor)
  
                        if oncurveNodeShape == 0:
                        
                            oval(point.x-s, point.y-s, s*2, s*2)
                    
                        elif oncurveNodeShape == 1:
                        
                            rect(point.x-s, point.y-s, s*2, s*2)
                        
                        elif oncurveNodeShape == 2:
                        
                            line((point.x-s, point.y-s), (point.x+s, point.y+s))
                            line((point.x-s, point.y+s), (point.x+s, point.y-s))
                            
                                            
                # shape[nodeShape](point.x-s, point.y-s, s*2, s*2)
                
                if displayCoordinates:
                    stroke(None)
                    fill(coordinatesColor)
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