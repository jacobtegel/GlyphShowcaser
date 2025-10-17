# Drawbot

'''

Overlay Layers!

LayerOverlayer is a stripped down and modified version of GlyphShowcaser with the intent of overlaying all of your layers over each other. Whether that might be different versions, alternate drawings or something else, stack it and save it.

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
t = FormattedString()
t.fontSize(72)
font = CurrentFont()
fontHeight = (font.info.ascender + margin) + -(font.info.descender - (margin / 2))
name = f"{font.info.familyName}-{font.info.styleName}"
fontName = name.replace(" ","-")

# Variables for UI (unchanged, removed for brevity)

Variable([

        dict(name="glyphSelection", ui="RadioGroup", args=dict(titles=['Current Glyph', 'Selected Glyphs', 'All Glyphs'], isVertical=True)),
        
        dict(name="margin", ui="Slider", args=dict(value=150, minValue=0, maxValue=500)),
    
        dict(name="artboardHeight", ui="RadioGroup", args=dict(titles=['Font Height', 'Glyph Height'], isVertical=True)),
        
        dict(name="backgroundColor", ui="ColorWell", args=dict(color=AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(1, 1, 1, 0))),
        
        dict(name="oncurveNodeShape", ui="RadioGroup", args=dict(titles=['Circle', 'Rectangle', 'Cross'], isVertical=True), value = 0),
        
        dict(name="offcurveNodeShape", ui="RadioGroup", args=dict(titles=['Circle', 'Rectangle', 'Cross'], isVertical=True), value = 0),
        
        dict(name="outlineThickness", ui="Slider", args=dict(value=1, minValue=1, maxValue=10)),
        
        dict(name="nodeSize", ui="Slider", args=dict(value=5, minValue=1, maxValue=10)),
        
        dict(name="nodeRatio", ui="Slider", args=dict(value=1, minValue=0, maxValue=1)),

        dict(name="useLayerColors", ui="CheckBox", args=dict(value=True)),
    
        dict(name="removeOverlap", ui="CheckBox", args=dict(value=True)),
    
        dict(name="exportAs", ui="RadioGroup", args=dict(titles=['PDF', 'SVG', 'PNG'], isVertical=True))
        
        ], globals())

s = nodeSize
r = nodeRatio * nodeSize

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

    glyphHeight = abs(glyph.bounds[1] - glyph.bounds[3])
    if artboardHeight == 0:
        height = (font.info.ascender + margin) + -(font.info.descender - (margin / 2))
    else:
        height = (glyphHeight + margin)
    
    pwidth = glyph.width + margin
    pheight = height
    
    newPage(pwidth, pheight)
    
    fill(backgroundColor)
    rect(0, 0, pwidth, pheight)

    # Translate so that the glyph is positioned correctly
    translate(margin / 2, -font.info.descender + (margin / 2))

    glyphName = glyph.name  # save name from initial glyphsToProcess loop

    for layer in font.layers:
        
        if glyphName not in layer:
            continue  # skip if layer doesn't have this glyph

        layerGlyph = layer[glyphName]

        c = RGlyph()
        pen = c.getPointPen()
        
        decomposePen = DecomposePointPen(layerGlyph.layer, pen)
        layerGlyph.drawPoints(decomposePen)            
        
        if c is None or not c.contours:
            continue  # Skip empty glyphs
        
        if removeOverlap:
            c.removeOverlap()
        
        # Extract the layer color
        layerColor = layer.color
        
        if useLayerColors:
            if layerColor:
                red, green, blue, alpha = layerColor
                strokeColor = AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(red, green, blue, alpha)
            else:
                strokeColor = AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(0, 0, 0, 1)  # Default to black
        else:
            strokeColor = AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(0, 0, 0, 1)  # Default to black

        # Set drawing attributes
        fill(None)  # No fill
        stroke(strokeColor)
        strokeWidth(outlineThickness)
                       
        drawGlyph(c)            # Draw contours without showing nodes
       
        for contour in c:
            
            for bPoint in contour.bPoints:
                        
                with savedState():
                    x, y = bPoint.anchor
                    translate(x, y)
                    stroke(strokeColor)
                    strokeWidth(1)
                    line ((0,0), bPoint.bcpIn)
                    line ((0,0), bPoint.bcpOut)
            
                for segment in contour:
       
                    for point in segment:
                    
                        if point.type == "offcurve":
                            stroke(strokeColor)
                            strokeWidth(1)
                            fill(strokeColor)

                            
                            if offcurveNodeShape == 0:
                                oval(point.x-r, point.y-r, r*2, r*2)
                    
                            elif offcurveNodeShape == 1:
                                rect(point.x-r, point.y-r, r*2, r*2)
                        
                            elif offcurveNodeShape == 2:
                        
                                line((point.x-r, point.y-r), (point.x+r, point.y+r))
                                line((point.x-r, point.y+r), (point.x+r, point.y-r))
                    
                        else:
                            stroke(strokeColor)
                            strokeWidth(1)
                            fill(strokeColor)

  
                            if oncurveNodeShape == 0:
                                oval(point.x-s, point.y-s, s*2, s*2)
                    
                            elif oncurveNodeShape == 1:
                                rect(point.x-s, point.y-s, s*2, s*2)
                        
                            elif oncurveNodeShape == 2:
                        
                                line((point.x-s, point.y-s), (point.x+s, point.y+s))
                                line((point.x-s, point.y+s), (point.x+s, point.y-s))
                            

if font is not None and font.path:
    font_path = os.path.dirname(font.path) #Get Folder in which the font is
    output_folder = f"{font_path}/LayerOverlayer-Output" # create output folder inside of that folder

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

if exportAs == 0:

    if glyphSelection == 0:
         saveImage(f"{output_folder}/{time}-LayerOverlayer-{fontName}-{glyph.name}.pdf")

    else:
         saveImage(f"{output_folder}/{time}-LayerOverlayer-{fontName}.pdf")
    
if exportAs == 1:

    if glyphSelection == 0:
        saveImage(f"{output_folder}/{time}-LayerOverlayer-{fontName}-{glyph.name}.svg", multipage = True)

    else:
        saveImage(f"{output_folder}/{time}-LayerOverlayer-{fontName}.svg", multipage = True)
   
if exportAs == 2:
    
    if glyphSelection == 0:
        saveImage(f"{output_folder}/{time}-LayerOverlayer-{fontName}-{glyph.name}.png", multipage = True)
    
    else:
        saveImage(f"{output_folder}/{time}-LayerOverlayer-{fontName}.png", multipage = True)
