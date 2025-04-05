# Drawbot

import AppKit
import os
from datetime import datetime
from mojo.roboFont import CurrentFont, CurrentGlyph, RGlyph
from drawBot import *

time = datetime.now().strftime('%Y-%m-%d-%H-%M')
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
        
        dict(name="margin", ui="Slider", args=dict(value=100, minValue=0, maxValue=500)),
    
        dict(name="artboardHeight", ui="RadioGroup", args=dict(titles=['Font Height', 'Glyph Height'], isVertical=True)),
        
        dict(name="backgroundColor", ui="ColorWell", args=dict(color=AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(1, 1, 1, 1))),
    
        dict(name="removeOverlap", ui="CheckBox"),

    
        dict(name="exportAs", ui="RadioGroup", args=dict(titles=['PDF', 'SVG', 'PNG'], isVertical=True))
        
        ], globals())

glyphsToProcess = []

# Current glyph
if glyphSelection == 0:
    glyphsToProcess = [CurrentGlyph()]

# Selected Glyphs    
elif glyphSelection == 1:
    glyphsToProcess = [font[glyphName] for glyphName in font.selection]
    
# All glyphs (with contours)
elif glyphSelection == 2:
    glyphsToProcess = [glyph for glyph in font]
    
print(glyphsToProcess)

# Initialize the last processed glyph variable
last_processed_glyph = None

# Process selected glyph/s
for glyph in glyphsToProcess:
    # Skip empty or None glyphs
    if glyph is None or not glyph.contours:
        continue

    print(f"Processing glyph: {glyph.name}")  # Debugging: Print the name of the glyph being processed

    glyphHeight = abs(glyph.bounds[1] - glyph.bounds[3])
    if artboardHeight == 0:
        height = (font.info.ascender + margin) + -(font.info.descender - (margin / 2))
    else:
        height = (glyphHeight + margin)
    
    pwidth = font.info.unitsPerEm + margin
    pheight = font.info.ascender - font.info.descender + margin
    
    newPage(pwidth, pheight)
    
    fill(backgroundColor)
    rect(0, 0, pwidth, pheight)

    # Translate so that the glyph is positioned correctly
    translate(margin / 2, -font.info.descender + (margin / 2))

    for layer in font.layers:  
        if glyphSelection == 0:
            glyph = layer[CurrentGlyph().name] if CurrentGlyph().name in layer else None
            glyphsToProcess = [glyph] if glyph else []
        elif glyphSelection == 1:
            glyphsToProcess = [layer[glyphName] for glyphName in font.selection if glyphName in layer]
        elif glyphSelection == 2:
            glyphsToProcess = [glyph for glyph in layer]

        for glyph in glyphsToProcess:
            if glyph is None or not glyph.contours:
                continue  # Skip empty glyphs

            # Extract the layer color
            layerColor = layer.color
            if layerColor:
                red, green, blue, alpha = layerColor
                strokeColor = AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(red, green, blue, alpha)
            else:
                strokeColor = AppKit.NSColor.colorWithSRGBRed_green_blue_alpha_(0, 0, 0, 1)  # Default to black

            # Set drawing attributes
            fill(None)  # No fill
            stroke(strokeColor)
            strokeWidth(1)

            # Copy the glyph and draw it
            c = glyph.copy()
            if removeOverlap:
                c.removeOverlap()
            drawGlyph(c)            # Draw contours without showing nodes
            for contour in c:
                for segment in contour:
                    # You can add conditions here to show nodes or not
                    pass

            # Save the last processed glyph
            last_processed_glyph = glyph

# Now, we handle the export outside the loop, using last_processed_glyph
if font is not None and font.path:
    font_path = os.path.dirname(font.path)  # Get Folder in which the font is
    output_folder = f"{font_path}/Showcaser-Output"  # Create output folder inside of that folder

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

# print(font_path)
# print(output_folder)
# print(time)

# Exporting
if exportAs == 0:
    if glyphSelection == 0 and last_processed_glyph:
         saveImage(f"{output_folder}/{time}-GlyphShowcaser-{fontName}-{last_processed_glyph.name}.pdf")  
    elif glyphSelection == 1 and last_processed_glyph:  
         saveImage(f"{output_folder}/{time}-GlyphShowcaser-{fontName}.pdf") 
    
if exportAs == 1:
    if glyphSelection == 0 and last_processed_glyph:
        saveImage(f"{output_folder}/{time}-GlyphShowcaser-{fontName}-{last_processed_glyph.name}.svg")
    elif glyphSelection == 1 and last_processed_glyph:
        saveImage(f"{output_folder}/{time}-GlyphShowcaser-{fontName}-.svg")
   
if exportAs == 2 and last_processed_glyph:
    saveImage(f"{output_folder}/{time}-GlyphShowcaser-{fontName}-{last_processed_glyph.name}.png") 