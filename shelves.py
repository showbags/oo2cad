from lib import *

import bpy
import mathutils
import math
from mathutils import Vector
   
def run(origo):
    setup()
    
    origin = Vector(origo)
    
    t = 0.016 #thickness of melamine (16mm)
    t2 = t/2  #half thickness
    hv = 1.66+t #height of the inner verticals
    hs = hv+t #height of the end verticals
    ds = 0.34 #depth of the sides and top
    dv = 0.295 #depth of the inner verticals
    ln = 2.4 #length of central pieces
    oln = ln+2*t #overall length
    #dxv = ln/7 #x spacing between verticals
    
    dzs1 = 0.33   #shelf z gap 1
    dzs2 = 0.25  #shelf z gap 2
    hs1 = dzs1   #height of first shelf
    hs2 = 2*hs1+t  #height of second shelf
    
    hs5 = hs2+3*dzs2
    
    #1. position the top
    top = box( name="top", origin=(t,0,hv), size=( ln, ds, t ) )
    
    #2. sides
    side1 = box( name="side1", origin=(0,0,0), size=( t, ds, hs ) )
    side2 = duplicate ( side1, off= (ln+t, 0, 0) )

    #3. verticals
    verticals=[]
    v1 = (ln-6*t)/7+t
    dxv = v1
    
    for xoff in frange( v1, oln-dxv, dxv ):
      verticals.append(box( origin=(xoff, ds-dv, 0), size=( t, dv, hv) ))
    
    
    #4. shelves
    #   cutters
    shelves=[]
    cutters=[]
    for xoff in frange( v1, oln-dxv, dxv ):
      cutter = box( origin=(xoff, ds-dv+dv/2, 0), size=( t, dv/2, hv) )
      cutters.append(cutter)
      
    shelves.append( box( origin=(t, 0, hs1), size=(ln, ds, t) ) )#shelf 1
    for zoff in frange( hs2, hs5+t, dzs2 ):         #shelves 2-5
      shelf = box( origin=(t, 0, zoff), size=(ln, ds, t) )
      shelves.append(shelf)
      
    for shelf in shelves:
      for cutter in cutters:
        subtract(shelf, cutter, True)
      
    #   remove cutters
    for cutter in cutters:      
      remove(cutter)
    
    for vertical in verticals:
      for shelf in shelves:
        subtract(vertical,shelf,True)
    
      
      
    return
 
if __name__ == "__main__":
    run((0,0,0))
