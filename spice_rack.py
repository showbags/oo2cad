from lib import *

import bpy
import mathutils
import math
from mathutils import Vector
   
def run(origo):
    setup()
    
    origin = Vector(origo)
    
    h = 0.56    
    w = 0.45
    dt = 0.05 #depth at the top
    db = 0.078 #depth at the bottom
    t = 0.016
    st = 0.016
    sto2 = st/2
    to2 = t/2
    h_t = h-t
    w_st = w-st
    w_2t = w-2*t
    
    #1. make side rails
    verts = ((0,0,0), (0, 0, h), (0, dt, h), (0, db, 0))
    rail1 = createMeshFromData(verts=verts, faces=makeFaces(verts), name='A face')
    extrudex(st)
    rail2 = duplicate(rail1, (w_st,0,0))
    
    #2. make shelves
    shelf1 = box( origin=(sto2,0,0), size=(w_st, db, t))
    shelf2 = duplicate(shelf1, (0, 0, h_t/3))
    shelf3 = duplicate(shelf1, (0, 0, 2*h_t/3))
    shelf4 = duplicate(shelf1, (0, 0, 3*h_t/3))
    
    #3. cut grooves from rails using shelves
    for shelf in [shelf1,shelf2,shelf3,shelf4]:
      subtract(rail1,shelf,True)
      subtract(rail2,shelf,True)    
    
    #4. cut fronts off of shelves
    rad = math.atan2(db-dt,h)
    shelf_cutter = box( origin=(0,db,0), size=(w, db, h), rot=(rad,0,0))
    subtract(shelf1,shelf_cutter,True)
    subtract(shelf2,shelf_cutter,True)
    subtract(shelf3,shelf_cutter,True)
    subtract(shelf4,shelf_cutter,False)
    
    
    #5. add some small bottles
    gap=0.0015 #gap between bottles
    small_d = 0.04
    small_r = small_d/2
    bot_h = 0.105 #bottle height
    for off in frange( small_r+st+gap, w-st-small_r, small_d+gap ):
      cylinder( size=(small_d, small_d, bot_h), origin=(off,small_r, t+h_t/3) )
      cylinder( size=(small_d, small_d, bot_h), origin=(off,small_r, t+2*h_t/3) )
      
    #6. add some large bottles
    gap=0.0015 #gap between bottles
    large_d = 0.05
    large_r = large_d/2
    large_h = 0.115
    for off in frange( large_r+st+gap, w-st-large_r, large_d+gap ):
      cylinder( size=(large_d, large_d, large_h), origin=(off,large_r, t) )
    
    #7. rails to keep them in
    rod_d=0.005 #radius of aluminium
    cylinder( name='rod1',size=(rod_d, rod_d, w_st), origin=(sto2,small_d+rod_d, t+2*h_t/3+bot_h/3), rot=(0,90,0) )
    cylinder( name='rod2',size=(rod_d, rod_d, w_st), origin=(sto2,small_d+rod_d, t+1*h_t/3+bot_h/3), rot=(0,90,0) )
    cylinder( name='rod3',size=(rod_d, rod_d, w_st), origin=(sto2,large_d+rod_d, t+0*h_t/3+bot_h/3), rot=(0,90,0) )
    
    
      
    
    return
 
if __name__ == "__main__":
    run((0,0,0))
