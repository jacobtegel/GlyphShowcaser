from mojo.extensions import getExtensionDefault, setExtensionDefault, removeExtensionDefault
from vanilla import *

extensionDefaultKey = "Jacobs.amazing.showcaser.settings"

# Remove previous settings
removeExtensionDefault(extensionDefaultKey)


class ShowcaserInterface:

    def __init__(self):
        # Window setup
        self.w = Window((475, 880), "GlyphShowcaser",)

        y = 10
        col1y = 15
        col2y = 175

        self.w.glyphSelectionTitle = TextBox((col1y, y, -10, 20), "Glyph Selection:")
        self.w.glyphSelection = RadioGroup((col2y, y, -15, 60),
                                      ["Current Glyph", "Selected Glyphs", "All Glyphs"],
                                      isVertical=True)
        self.w.glyphSelection.set(0)
        y += 70

        # Horizontal Line
        self.w.line1 = HorizontalLine((col1y, y, -15, 1))
        y += 15
        
        # Node Size
        self.w.marginTitle = TextBox((col1y, y, -10, 20), "Node Size:")
        self.w.marginSlider = Slider((col2y, y, 200, 20), minValue=0, maxValue=500, value=100, callback=self.nodeSizeCallback)
        self.w.marginStepper = Stepper((col2y + 210, y, 20, 20), minValue=0, maxValue=500, value=100, callback=self.nodeSizeCallback)
        self.w.marginValue = EditText((col2y + 240, y, 50, 20), text="100")
        y += 30

        # Artboard Height
        self.w.artboardHeightTitle = TextBox((col1y, y, -10, 20), "Artboard Height:")
        self.w.artboardHeight = RadioGroup((col2y, y, -15, 40),
                                           ["Font Height", "Glyph Height"],
                                           isVertical=True)
        self.w.artboardHeight.set(0)
        y += 50

        # Horizontal Line
        self.w.line2 = HorizontalLine((col1y, y, -15, 1))
        y += 15

        # Background and Glyph Colors
        self.w.backgroundColorTitle = TextBox((col1y, y, -10, 20), "Background Color:")
        self.w.backgroundColor = ColorWell((col2y, y, 100, 20))
        y += 30

        self.w.glyphColorTitle = TextBox((col1y, y, -10, 20), "Glyph Color:")
        self.w.glyphColor = ColorWell((col2y, y, 100, 20))
        y += 30

        # Glyph Outline
        self.w.glyphOutlineTitle = TextBox((col1y, y, -10, 20), "Glyph Outline:")
        self.w.glyphOutline = CheckBox((col2y, y, -15, 20), "")
        y += 30

        self.w.outlineColorTitle = TextBox((col1y, y, -10, 20), "Outline Color:")
        self.w.outlineColor = ColorWell((col2y, y, 100, 20))
        y += 30

        # Horizontal Line
        self.w.line3 = HorizontalLine((col1y, y, -15, 1))
        y += 15

        # Show Nodes
        self.w.showNodesTitle = TextBox((col1y, y, -10, 20), "Show Nodes:")
        self.w.showNodes = CheckBox((col2y, y, -15, 20), "")
        y += 30

        self.w.nodeShapeTitle = TextBox((col1y, y, -10, 20), "Node Shape:")
        self.w.nodeShape = RadioGroup((col2y, y, -15, 60),
                                      ["Circle", "Rectangle", "Cross"],
                                      isVertical=True)
        self.w.nodeShape.set(0)
        y += 70

        # Node Size
        self.w.nodeSizeTitle = TextBox((col1y, y, -10, 20), "Node Size:")
        self.w.nodeSizeSlider = Slider((col2y, y, 200, 20), minValue=1, maxValue=10, value=5, callback=self.nodeSizeCallback)
        self.w.nodeSizeStepper = Stepper((col2y + 210, y, 20, 20), minValue=1, maxValue=10, value=5, callback=self.nodeSizeCallback)
        self.w.nodeSizeValue = EditText((col2y + 240, y, 50, 20), text="5")
        y += 30

        self.w.nodeSizeRatioTitle = TextBox((col1y, y, -10, 20), "Node Size Ratio:")
        self.w.nodeSizeRatioSlider = Slider((col2y, y, 200, 20), minValue=0, maxValue=1, value=1, callback=self.nodeSizeRatioCallback)
        self.w.nodeSizeRatioStepper = Stepper((col2y + 210, y, 20, 20), minValue=0, maxValue=1, value=1, callback=self.nodeSizeRatioCallback)
        self.w.nodeSizeRatioValue = EditText((col2y + 240, y, 50, 20), text="1")
        y += 30

        # Horizontal Line
        self.w.line4 = HorizontalLine((col1y, y, -15, 1))
        y += 15

        # Color Wells for Oncurve, Offcurve, and Handle Colors
        self.w.onCurveStrokeTitle = TextBox((col1y, y, -10, 20), "Oncurve Stroke Color:")
        self.w.onCurveStroke = ColorWell((col2y, y, 100, 20))
        y += 30

        self.w.onCurveFillTitle = TextBox((col1y, y, -10, 20), "Oncurve Fill Color:")
        self.w.onCurveFill = ColorWell((col2y, y, 100, 20))
        y += 30

        self.w.offCurveStrokeTitle = TextBox((col1y, y, -10, 20), "Offcurve Stroke Color:")
        self.w.offCurveStroke = ColorWell((col2y, y, 100, 20))
        y += 30

        self.w.offCurveFillTitle = TextBox((col1y, y, -10, 20), "Offcurve Fill Color:")
        self.w.offCurveFill = ColorWell((col2y, y, 100, 20))
        y += 30

        self.w.handleStrokeTitle = TextBox((col1y, y, -10, 20), "Handle Stroke Color:")
        self.w.handleStroke = ColorWell((col2y, y, 100, 20))
        y += 30

        # Horizontal Line
        self.w.line5 = HorizontalLine((col1y, y, -15, 1))
        y += 15

        # Remove Overlap and Show Coordinates
        self.w.removeOverlapTitle = TextBox((col1y, y, -10, 20), "Remove Overlap:")
        self.w.removeOverlap = CheckBox((col2y, y, -15, 20), "")
        y += 30

        self.w.showCoordinatesTitle = TextBox((col1y, y, -10, 20), "Show Coordinates:")
        self.w.showCoordinates = CheckBox((col2y, y, -15, 20), "")
        y += 30

        self.w.coordinatesColorTitle = TextBox((col1y, y, -10, 20), "Coordinates Color:")
        self.w.coordinatesColor = ColorWell((col2y, y, 100, 20))
        y += 30

        # Horizontal Line
        self.w.line6 = HorizontalLine((col1y, y, -15, 1))
        y += 15

        # Format and Export Button
        self.w.formatTitle = TextBox((col1y, y, -10, 20), "Format:")
        self.w.format = RadioGroup((col2y, y, -15, 60),
                                   ["PDF", "SVG", "PNG"],
                                   isVertical=True)
        self.w.format.set(0)
        y += 70

        # Export Button
        self.w.exportButton = Button((col1y, y, -15, 30), "Export", callback=self.exportCallback)

        # Load initial settings
        self.loadSettings()

        # Open window
        self.w.open()

    def loadSettings(self):
        settings = getExtensionDefault(extensionDefaultKey, {})
        # Restore settings here if needed

    def marginCallback(self, sender):
        print("Margin:", sender.get())

    def nodeSizeCallback(self, sender):
        print("Node Size:", sender.get())

    def nodeSizeRatioCallback(self, sender):
        print("Node Size Ratio:", sender.get())

    def exportCallback(self, sender):
        values = {
            "glyphSelection": self.w.glyphSelection.get(),
            "margin": self.w.marginSlider.get(),
            "backgroundColor": self.w.backgroundColor.get(),
            "glyphColor": self.w.glyphColor.get(),
            # Add more values as needed
        }
        setExtensionDefault(extensionDefaultKey, values)
        print("Exported values:", values)


# Instantiate the interface
ShowcaserInterface()