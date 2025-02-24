import ezui

interfaceWidth = 350

class ShowcaserInterface(ezui.WindowController):

    def build(self):
        content = """
        !!! Showcase your Drawings!
        ---
        
        * VerticalStack
        > * TwoColumnForm @formOne
        >> : Glyph Selection:        
        >> ( ) Current Glyph @glyphSelection
        # >> ( ) Selected glyphs
        >> ( ) All Glyphs
        >> --- 
        >> : Margins:
        >> ---X--- [_](±) @margin
        >> ---
        >> : Background Color:
        >> * ColorWell @backgroundColor
        >> : Glyph Color:
        >> * ColorWell @glyphColor
        >> ---
        >> : Glyph Outline:
        >> [X] @glyphOutline
        >> : Outline Color:
        >> * ColorWell @outlineColor
        
        ---
        
        * VerticalStack 
        > * TwoColumnForm @formTwo
        >> : Show Nodes:
        >> [X] @showNodes
        >> : Node Shape:
        >> (X) Circle @nodeShape"
        >> ( ) Rectangle
        >> ( ) Cross
        >> : Node Size:
        >> ---X--- [_](±) @nodeSize
        
        ---
        
        * VerticalStack 
        > * TwoColumnForm @formThree
        >> : Oncurve Stroke Color:
        >> * ColorWell @onCurveStroke
        >> : Oncurve Fill Color:
        >> * ColorWell @onCurveColor
        >> : Offcurve Stroke Color:
        >> * ColorWell @offCurveStroke
        >> : Offcurve Fill Color:
        >> * ColorWell @offCurveColor
        >> : Handle Stroke Color:
        >> * ColorWell @bcpLineStroke
        
        ---
        
        * VerticalStack 
        > * TwoColumnForm @formFour
        >> : Remove Overlap:
        >> [X] @removeOverlap
        >> : Display Coordinates:
        >> [ ] @displayCoordinates
        
        ---
        
        * VerticalStack 
        > * TwoColumnForm @formFive
        >> : Export as:
        >> * HorizontalStack
        >>> (PDF) @exportPdf
        >>> (SVG) @exportSvg
        >>> (PNG) @exportPng        
        """
        
        descriptionData = dict(
                            
            formOne = dict(
                titleColumnWidth = interfaceWidth/2,
                itemColumnWidth = interfaceWidth/2
            ),
            
            formTwo = dict(
                titleColumnWidth = interfaceWidth/2,
                itemColumnWidth = interfaceWidth/2   
            ),
            
            formThree = dict(
                titleColumnWidth = interfaceWidth/2,
                itemColumnWidth = interfaceWidth/2   
            ),
            
            formFour = dict(
                titleColumnWidth = interfaceWidth/2,
                itemColumnWidth = interfaceWidth/2   
            ),
            
            formFive = dict(
                titleColumnWidth = interfaceWidth/2,
                itemColumnWidth = interfaceWidth/2   
            ),

            accordion=dict(
                closed=False,
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
                stopOnTickMarks=True
            ),
        )
        
        self.w = ezui.EZWindow(
            title="Showcaser",
            content=content,
            descriptionData=descriptionData,
            controller=self
        )

    def started(self):
        self.w.open()

ShowcaserInterface()
