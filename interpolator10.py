## Super Crude Interpolation from two masters. 
# ---
# http://www.scribbletone.com
# --




from mojo.roboFont import *
from vanilla import *
from mojo.glyphPreview import GlyphPreview
from mojo.events import addObserver
from mojo.roboFont import OpenWindow

from robofab.interface.all.dialogs import SelectFont

from mojo.events import BaseEventTool, installTool
from AppKit import *
import os

import time



# Interpolator
# By: Travis Kochel of TK Type
# http://www.tktype.com


all_f = AllFonts()

#self.font_1 is selected font window
font_1 = all_f[0]
font_2 = all_f[1]


preview_glyph = 'n'

#masters
shape_1 = font_1[preview_glyph]
shape_2 = font_2[preview_glyph]

#removes previous interpTest glyphs
#for f in AllFonts():
#    if f.has_key('interpTest'):
#        f.removeGlyph('interpTest')
#        f.update()

#where preview shape will be placed
font_1.newGlyph('interpTest')
new_shape = font_1['interpTest']

new_shape.update()
font_1.update()



#factors for interpolation 
x_factor = 0
y_factor = 0



class Preview:
  
    def __init__(self):
        
        
        self.font_1 = font_1
        self.font_2 = font_2
        self.x_factor = x_factor
        self.y_factor = y_factor
        self.shape_1 = shape_1
        self.shape_2 = shape_2
        self.new_shape = new_shape
        self.preview_glyph = preview_glyph

        self.new_shape.interpolate((x_factor, y_factor), shape_2, shape_1)
        
        ## create a window
        self.w = Window((1100, 375), "Interpolate")

        #window design elements
        #self.w.zeroLine = VerticalLine((610, 8, 5, 58))
        #self.w.oneLine = VerticalLine((727, 8, 5, 58))
        
        self.w.box = Box((10, 10, 180, -10))

        ## add a GlyphPreview to the window
        self.w.preview = GlyphPreview((200, 50, 300, 350))
        self.w.preview2 = GlyphPreview((500, 50, 300, 350))
        self.w.preview3 = GlyphPreview((800, 50, 300, 350))

        self.new_shape.update()
        self.font_1.update() 
        ## set the currentGlyph
        self.setGlyph(CurrentGlyph())

        ## add an observer when the glyph changed in the glyph view
        #addObserver(self, "_currentGlyphChanged", "currentGlyphChanged")


        ## sliders
        
        
        
        self.x_size = 0.00
        self.w.textX = EditText((212, 21, 40, 19), callback=self.textAdjust, sizeStyle= 'small')
        self.w.textX.set(0.00)
        
        self.w.textXlabel = TextBox((200, 22, 20, 19), "x", sizeStyle= 'small')
        
        self.w.x = Slider((260, 24, 820, 22), value=0.00,
                                        maxValue=3,
                                        minValue=-2,
                                        callback=self.adjust,tickMarkCount=6)
        
        
        self.y_size = 0.00
        self.w.textY = EditText((212, 51, 40, 19), callback=self.textAdjust, sizeStyle= 'small', placeholder = '0.00')
        self.w.textY.set(0.00)
        
        self.w.textYlabel = TextBox((200, 52, 20, 19), "y", sizeStyle= 'small')
        
        self.w.y = Slider((260, 54, 820, 22), value=0.00, maxValue=3,minValue=-2, callback=self.adjust,tickMarkCount=6)
        
        self.w.m1Tick= TextBox((569, 80, 40, 70), "M1", sizeStyle= 'small', alignment="center")
        self.w.m2Tick= TextBox((732, 80, 40, 70), "M2", sizeStyle= 'small', alignment="center")
                      
        #current masters
        font_list = []
        for f in all_f:
            font_list.append(str(f))
        
        self.w.master1Text = TextBox((20, 20, 160, 20), 'Master 1', sizeStyle= 'small')
        self.w.master1 = PopUpButton((20, 35, 160, 20), font_list, callback=self.chooseMaster1, sizeStyle= 'small')
        
        self.w.master2Text = TextBox((20, 65, 160, 20), 'Master 2', sizeStyle= 'small')
        self.w.master2 = PopUpButton((20, 80, 160, 20), font_list, callback=self.chooseMaster2, sizeStyle= 'small') 
        self.w.master2.set(1)
                
        
        #change glyph preview
        glyph_list = []
        for g in self.font_1:
            glyph_list.append(str(g.name))
        
        self.w.baseGlyphText = TextBox((20, 130, 160, 20), 'Preview Glyph', sizeStyle= 'small')
        self.w.baseGlyph = ComboBox((20, 148, 160, 20), glyph_list, callback=self.changeBaseGlyph, sizeStyle= 'small' )
        self.w.baseGlyph.set('n');
                
        
        self.w.line = HorizontalLine((20, 115, 160, 5))
        self.w.line2 = HorizontalLine((20, 185, 160, 5))
        self.w.line3 = HorizontalLine((20, 189, 160, 5))
        
        
        # button to apply settings to whole font
        self.w.button = Button((20, 325, 160, 40), "Interpolate it!", callback=self.interpolateFull, sizeStyle= 'small')

        
        
        ## open the window
        self.w.open()
        
        
    def setGlyph(self, glyph):
        ## setting the glyph in the glyph Preview
        self.w.preview.setGlyph(self.shape_1)
        self.w.preview2.setGlyph(self.new_shape)
        self.w.preview3.setGlyph(self.shape_2)
        
    def adjust(self, sender):
        ## get slider values
        
        self.x_factor = float(self.w.x.get())
        self.w.textX.set("%0.2f" % self.x_factor)
        
        self.y_factor = float(self.w.y.get())
        self.w.textY.set("%0.2f" % self.y_factor)
        
        self.interPrev('adjust')
        
    def textAdjust(self, sender):
        ## get slider values
        
        try:
            float(sender.get())
            
        except:
            print 'Float values only'
        else:
            
            self.x_factor = float(self.w.textX.get())
            self.w.x.set(self.x_factor)
        
            self.y_factor = float(self.w.textY.get())
            self.w.y.set(self.y_factor)
        
            self.interPrev('adjust')
        
        
                
    def interPrev (self, sender):
        
                
        self.new_shape.interpolate((self.x_factor, self.y_factor), self.shape_2, self.shape_1)
        
        self.new_shape.update()
        self.font_1.update() 
        self.font_2.update() 
        
    def interpolateFull (self, sender):
        print 'Interpolating with factors of x:' + str(self.x_factor) + ' y:' + str(self.y_factor)
        
        
        #removes interpTest glyphs
        for f in all_f:
            if f.has_key('interpTest'):
                f.removeGlyph('interpTest')
                f.update()
        
        dst = NewFont()

        dst.interpolate((self.x_factor, self.y_factor), self.font_2, self.font_1)

        dst.info.familyName = "NewWeight"

        for glyph in dst:
            glyph.round()
            glyph.update()
            
        dst.update()
        
        print 'Interpolated, your curves have been!'


    def chooseMaster1 (self, sender):
        
        self.font_1 = all_f[sender.get()]
        self.font_1.update()
        
        self.font_1.newGlyph('interpTest')
        
        self.shape_1 = self.font_1[self.preview_glyph]
        
        self.setGlyph(CurrentGlyph())
        self.interPrev('adjust')
        
                         
                         
    def chooseMaster2 (self, sender):
        self.font_2 = all_f[sender.get()]
        self.font_2.update()
                
        self.shape_2 = self.font_2[self.preview_glyph]

        self.setGlyph(CurrentGlyph())
        self.interPrev('adjust')
        
    def changeBaseGlyph (self, sender):
    
        self.preview_glyph = sender.get()
        
        self.shape_1 = self.font_1[self.preview_glyph]
        self.shape_2 = self.font_2[self.preview_glyph]

        self.setGlyph(CurrentGlyph())
        self.interPrev('adjust')
        
        
        
        
        
    
    def testDef (self, sender):
        print 'test'
        
OpenWindow(Preview)
        


print 'Ready for some interpolation action'