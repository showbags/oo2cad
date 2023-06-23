from lib import *

import bpy
import mathutils
import math
from mathutils import Vector
   
def run(origo):
    setup()
    
    jt = 0.018 #thickness of jarrah material (18mm)
    sd = 0.45-jt #shelf depth
    rd = 0.06 #depth of the rail (below top of bracket)
    
    jt2 = jt/2
    st = 0.014 #thickness of shelf
    
    we = 0.065 #width of the shelf edging
    ww = 0.05 #width of the wall attachment
    
    we2 = we+st
    wb = we #width of the brace
    sl = 2.5   #total length of shelf
    
    hb = 0.02 #height of the bottom of the brace
    #h = sd-st+wb+hb+jt2-st   #height of the wall attachment
    td = sd-jt-jt2 #top piece depth
    h = td+wb+hb   #height of the wall attachment
    lb = h*math.sqrt(2)  #length of the brace
    
    bx = (ww-jt)/2 #x position of the brace parts
    bx2 = (ww-jt)/2 #x position of the brace parts
    #1. position the wall attachement
    wall = box( name="wall", origin=(0,0,0), size=( ww, jt, h ) )
    top = box( name="top", origin=(bx2,jt2,h-wb), size=(jt, -td, wb) )
    brace = box( name="brace", origin=(bx,jt2,hb), size=(jt, wb, lb), rot=(math.radians(45),0,0) )
    vcutter = box( origin=( 0, jt2, 0 ), size=( 1, 1, 1 ) )
    subtract(brace,vcutter)
    hcutter = box( origin=( -0.5, 0, h-wb ), size=( 1, -1, 1 ) )
    subtract(brace,hcutter)
    
    brace = join(["wall","top","brace"],newname="triangle")
    duplicate(brace, off=(0.5,0,0), ncopy=3 )
    
    asl = sl-2*jt #actual shelf length
    asl2 = asl/2
    shelf1 = box( origin=(-0.5+jt, jt, h), size=(asl2,-sd,st) )
    shelf2 = box( origin=(-0.5+jt+asl2, jt, h), size=(asl2,-sd,st) )
    
    el2 = (sl-2*jt)/2 #half the main edge length
    edge1 = box( name="edge1", origin=(-0.5+jt, -sd+jt, h), size=(el2,jt,-we) )
    edge2 = box( name="edge2", origin=(-0.5+jt+el2, -sd+jt, h), size=(el2,jt,-we) )
    
    edge_end1 = box( name="edge end 1",origin=(-0.5, -sd+jt, h+st), size=(jt,sd,-we2) )
    edge_end2 = box( name="edge end 2",origin=(2.0-jt, -sd+jt, h+st), size=(jt,sd,-we2) )
    
    rail = cylinder( namein="rail", origin=(-0.5, -sd/2, h-rd), size=(0.02,0.02,sl), rot=(0,math.radians(90),0)) 
    
    return
 
if __name__ == "__main__":
    run((0,0,0))
