import ezui
from mojo.extensions import getExtensionDefault, setExtensionDefault, removeExtensionDefault

extensionDefaultKey = "Jacobs.amazing.showcaser.settings"

removeExtensionDefault(extensionDefaultKey)

class ShowcaserInterface(ezui.WindowController):

    def build(self):
        content = """
        = TwoColumnForm 
        !§ Showcase your Drawings!
        : Glyph Selection:        
        (X) Current Glyph @glyphSelection
        ( ) Selected glyphs
        ( ) All Glyphs      
        
        ---

        : Margins:
        ---X--- [_](±) @margin
        
        : Artboard Height:
        (X) Font Height @artboardHeight 
        ( ) Glyph Height
        
        ---
         
        :Background Color:
        * ColorWell @backgroundColor
        
        : Glyph Color:
        * ColorWell @glyphColor
        
        : Glyph Outline:
        [X] @glyphOutline
        
        : Outline Color:
        * ColorWell @outlineColor
        
        --- 
        
        : Show Nodes:
        [X] @showNodes
        
        : Node Shape:
        (X) Circle @nodeShape
        ( ) Rectangle
        ( ) Cross
        
        : Node Size:
        ---X--- [_](±) @nodeSize
        : Node Size Ratio:
        ---X--- [_](±) @nodeSizeRatio
        
        ---
        
        : Oncurve Stroke Color:
        * ColorWell @onCurveStroke
        
        : Oncurve Fill Color:
        * ColorWell @onCurveColor
        
        : Offcurve Stroke Color:
        * ColorWell @offCurveStroke
        
        : Offcurve Fill Color:
        * ColorWell @offCurveColor
        
        : Handle Stroke Color:
        * ColorWell @handleStroke
        
        ---
        
        : Remove Overlap:
        [X] @removeOverlap
        
        : Display Coordinates:
        [ ] @displayCoordinates
        
        : Coordinates Color:
        * ColorWell @coordinatesColor
        
        ---
        
        : Format:
        (X) PDF  @exportFormat
        ( ) SVG
        ( ) PNG
        =---=
                
        (Export) @export        
        """
  
        
        descriptionData = dict(
            content=dict(
                titleColumnWidth=150,
                itemColumnWidth=200
            ),
                                        
            margin=dict(
                minValue=0,
                maxValue=500,
                value=100
            ),
                        
            nodeSize=dict(
                minValue=1,
                maxValue=10,
                value=5,
                tickMarks=10,
                stopOnTickMarks=False
            ),
            
            nodeSizeRatio=dict(
                minValue=0,
                maxValue=1,
                value=1,
                tickMarks=10,
                stopOnTickMarks=False
            ),
        )
        
        self.w = ezui.EZWindow(
            title="Showcaser",
            content=content,
            descriptionData=descriptionData,
            controller=self
        )
        
        self.w.setItemValues(getExtensionDefault(extensionDefaultKey, dict()))

    def started(self):
        self.w.open()
    
    def glyphSelectionCallback(self, sender):
        print(sender.get())
        
    def marginCallback(self, sender):    
        print(sender.get())
        
    def backgroundColorCallback(self, sender):
        print(sender.get())
            
    def glyphColorCallback(self, sender):
        print(sender.get())
        
    def glyphOutlineCallback(self, sender):
        print(sender.get())
        
    def outlineColorCallback(self, sender):
        print(sender.get())
        
    def showNodesCallback(self, sender):
        print(sender.get())
        
    def nodeShapeCallback(self, sender):
        print(sender.get())
        
    def nodeSizeCallback(self, sender):
        print(sender.get())
        
    def nodeSizeRatioCallback(self, sender):
        print(sender.get())
        
    def onCurveStrokeCallback(self, sender):
        print(sender.get())
        
    def onCurveColorCallback(self, sender):
        print(sender.get())
        
    def offCurveStrokeCallback(self, sender):
        print(sender.get())
        
    def offCurveColorCallback(self, sender):
        print(sender.get()) 
           
    def handleStrokeCallback(self, sender):
        print(sender.get())
        
    def removeOverlapCallback(self, sender):
        print(sender.get())
        
    def displayCoordinatesCallback(self, sender):
        print(sender.get())
        
    def exportFormatCallback(self, sender):
        print(sender.get())
        
    def exportCallback(self, sender):
        values = self.w.getItemValues()
        setExtensionDefault(extensionDefaultKey, values)
        print(self.w.getItemValues())

ShowcaserInterface()