## Count points in glyph
# --- 
# Helpful for prepping for interpolation.
# ---
# http://www.scribbletone.com
# --

from mojo.roboFont import *

f = CurrentFont()
g = CurrentGlyph()

print g.name + ' in ' + str(f)

points = 0
bPoints = 0

for contour in g:
    points = points + len(contour.points)
    
    bPoints = bPoints + len(contour.bPoints)

    
print 'Points: ' + str(bPoints) + ', Handles: ' + str(points-bPoints)
