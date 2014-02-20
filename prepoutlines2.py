## Prep for Interpolation
# --- 
# Has some bugs, and doesn't completely fix everything. But gets you partly there.
# ---
# http://www.scribbletone.com
# --

from mojo.roboFont import *
from vanilla import *
from mojo.glyphPreview import GlyphPreview
from mojo.events import addObserver
from mojo.roboFont import OpenWindow

from mojo.events import BaseEventTool, installTool
from AppKit import *
import os

import time
# Interpolator
# By: Travis Kochel of TK Type
# http://www.tktype.com


class prepOutlines(object):

    def __init__(self):
        
        #initial variables
        self.all_f = AllFonts()
        self.master_1 = self.all_f[0]
        self.master_2 = self.all_f[1]
        
        self.master_fonts =[]
        self.master_fonts.append(self.master_1)
        self.master_fonts.append(self.master_2)
        
        
        
        
        self.w = Window((300, 340), "Whip Those Nodes into Shape")
        
        self.w.titleBox = TextBox((20, 20, -20, 17), "Prepare Outlines for Interpolation")
        
        
        #masters
        font_list = []
        for f in self.all_f:
            font_list.append(str(f))
        
        self.w.master1Text = TextBox((20, 50, 160, 20), 'Master 1', sizeStyle= 'small')
        self.w.master1 = PopUpButton((20, 65, 160, 20), font_list, callback=self.chooseMaster1, sizeStyle= 'small')
        
        self.w.master2Text = TextBox((20, 95, 160, 20), 'Master 2', sizeStyle= 'small')
        self.w.master2 = PopUpButton((20, 110, 160, 20), font_list, callback=self.chooseMaster2, sizeStyle= 'small') 
        self.w.master2.set(1)

        
        #options
        self.w.cleanSlate = CheckBox((20, 150, -20, 20), "Reset Glyph Mark colors", value=True, sizeStyle="small")
        
        self.w.removeOverlap = CheckBox((20, 170, -20, 20), "Remove Overlap", value=True, sizeStyle="small")
        
        self.w.contourOrder = CheckBox((20, 190, -20, 20), "Auto Contour Order", value=True, sizeStyle="small")
        self.w.correctDirection = CheckBox((20, 210, -20, 20), "Correct Contour Direction", value=True, sizeStyle="small")
        self.w.startPoints = CheckBox((20, 230, -20, 20), "Auto Start Points", value=True, sizeStyle="small")
        self.w.countNodes = CheckBox((20, 250, -20, 20), "Count and Compare Points Between Masters", value=True, sizeStyle="small")
        self.w.countExplain = TextBox((34, 270, -30, 30), "Conflicting glyphs marked in red. Duplicate points indicated with guides", sizeStyle="mini")
        
        
        
        #start button
        self.w.startButton = Button((10, 310, -10, 20), "Run Preparations", callback=self.runPrep)
        
        self.w.open()

    def runPrep(self, sender):
        
        if self.w.cleanSlate.get():
            self.cleanSlateRun()  
            
        if self.w.removeOverlap.get():
            self.removeOverlapRun()
            
        if self.w.contourOrder.get():
            self.contourOrderRun()
            

            
        if self.w.correctDirection.get():
            self.correctDirectionRun()
            
        if self.w.startPoints.get():
            self.startPointsRun()
            
        if self.w.countNodes.get():
            self.countNodesRun()
            
        print 'done'        
                            
    def cleanSlateRun(self):
        #print 'cleanSlate'
        for font in self.master_fonts:
            for glyph in font:
                #print 'resetting mark color'
                glyph.mark = None

                #remove unneeded guides
                #print 'removing duplicate point guides'        
                for guide in glyph.guides:
                    if (guide.name == 'duplicate point'):
                        glyph.removeGuide(guide)
                        
    def removeOverlapRun(self):
        
        for font in self.master_fonts:
            for glyph in font:
                glyph.removeOverlap()
    
                        
    def contourOrderRun(self):
        #print 'contourOrder'
        for font in self.master_fonts:
            for glyph in font:
                glyph.autoContourOrder()
        
            
    def correctDirectionRun(self):
        #print 'correctDirection'
        for font in self.master_fonts:
            for glyph in font:
                glyph.correctDirection()
        
    def startPointsRun(self):
        #print 'startPoints'
        for font in self.master_fonts:
            for glyph in font:       
                for contour in glyph:
                    contour.autoStartSegment()
        
    def countNodesRun(self):
        #print 'countNotes'
        
        for glyph in self.master_fonts[0]:
            num_points_a = 0
            num_points_b = 0
    
            for contour_a in glyph:
                num_points_a = num_points_a + len(contour_a.points)
    
            for contour_b in self.master_fonts[1][glyph.name]:
                num_points_b = num_points_b + len(contour_b.points)


            if (num_points_a != num_points_b):
        
                target_glyph = glyph
        
                if (num_points_a < num_points_b):
                    target_glyph = self.master_fonts[1][glyph.name]
        
                target_glyph.mark = (200,0,0, 100)
                print target_glyph.name + ': ' + str(num_points_a) + ', ' + str(num_points_b)
        
                #identify duplicate points and add guides
        
                for contour in target_glyph:
        
                    points = contour.points
                    seen = set()
                    for n in points:
                        if str(n) in seen:
                            #print "duplicate:", n
                        
                            target_glyph.addGuide((n.x, n.y), 0, name="duplicate point")
                            target_glyph.addGuide((n.x, n.y), 90, name="duplicate point")
                            glyph.mark = (200,0,200, 100)
                
                    
                        else:
                            seen.add(str(n))
    
    
    def chooseMaster1(self, sender):
        self.master_fonts[0] = self.all_f[sender.get()]
        
    
    def chooseMaster2(self, sender):
        self.master_fonts[1] = self.all_f[sender.get()]
    

    def runAll():
        all_f = AllFonts()


        for font in all_f:
    
            print font
    
            for glyph in font:
                #print 'correcting contour direction'
                glyph.correctDirection()
        
                #print 'correcting contour order'
                glyph.autoContourOrder()
        
                #print 'resetting mark color'
                glyph.mark = (256,256,256, 0)
        
                #remove unneeded guides
                #print 'removing duplicate point guides'        
                for guide in glyph.guides:
                    if (guide.name == 'duplicate point'):
                        glyph.removeGuide(guide)
    
                #print 'correcting start points'
                for contour in glyph:
                    contour.autoStartSegment()
            
            font.update()
 

        #count and compare contours. mark red if there are conflicts
        print 'counting and comparing number of points'
        for glyph in all_f[0]:
            num_points_a = 0
            num_points_b = 0
    
            for contour_a in glyph:
                num_points_a = num_points_a + len(contour_a.points)
    
            for contour_b in all_f[1][glyph.name]:
                num_points_b = num_points_b + len(contour_b.points)


            if (num_points_a != num_points_b):
        
                target_glyph = glyph
        
                if (num_points_a < num_points_b):
                    target_glyph = all_f[1][glyph.name]
        
                target_glyph.mark = (200,0,0, 100)
                print target_glyph.name + ': ' + str(num_points_a) + ', ' + str(num_points_b)
        
                #identify duplicate points and add guides
        
                for contour in target_glyph:
        
                    points = contour.points
                    seen = set()
                    for n in points:
                        if str(n) in seen:
                            #print "duplicate:", n
                        
                            target_glyph.addGuide((n.x, n.y), 0, name="duplicate point")
                            target_glyph.addGuide((n.x, n.y), 90, name="duplicate point")
                            glyph.mark = (200,0,200, 100)
                
                    
                        else:
                            seen.add(str(n))
            
            
            
        

prepOutlines()

print 'Ready'