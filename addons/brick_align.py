import bpy
import bmesh
  
bl_info = {  
 "name": "Brick",  
 "author": "Sam Howman",  
 "version": (1, 0),  
 "blender": (2, 6, 4),  
 "location": "View3D > Edit > Brick Align Object",  
 "description": "Aligns the active Object to whole brick increments",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Edit"}  
 
class BrickOperator(bpy.types.Operator):  
 """Brick Align"""  
 bl_idname = "object.brickalign_operator"  
 bl_label = "Brick Align Operator"  
 bl_options = {'REGISTER', 'UNDO'}  
  
 @staticmethod
 def execute(self,context):
  
  obj = bpy.context.scene.objects.active # active object
  if obj.mode=='OBJECT':
    #First align the selected objects
    obj.location.x = nearestx(obj.location.x)
    obj.location.y = nearesty(obj.location.y)
    obj.location.z = nearestz(obj.location.z)
  else:
  
    mesh = obj.data
    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(mesh)   # fill it in from a Mesh

    # Modify the BMesh, can do anything here...
    for vert in bm.verts:
      if vert.select:
        print( 'before %f %f %f' % (vert.co.x, vert.co.y, vert.co.z) )
        vert.co.x = nearestx(vert.co.x)
        vert.co.y = nearesty(vert.co.y)
        vert.co.z = nearestz(vert.co.z)
        print( 'after %f %f %f\n' % (vert.co.x, vert.co.y, vert.co.z) )
    mesh.update(True,True)
    # Finish up, write the bmesh back to the mesh
    bmesh.update_edit_mesh(mesh)
  
  return {'FINISHED'}
  
 @classmethod  
 def poll(cls, context):  
  ob = context.active_object  
  return ob is not None# and ob.mode == 'EDIT'  

def nearestx(x):
  d = [abs(nearest_l1(x)-x), abs(nearest_l2(x)-x), abs(nearest_w1(x)-x), abs(nearest_w2(x)-x)]   
  n = [nearest_l1(x), nearest_l2(x), nearest_w1(x), nearest_w2(x) ]
  return n[d.index(min(d))]


def nearesty(x):
  d = [abs(nearest_l1(x)-x), abs(nearest_l2(x)-x), abs(nearest_w1(x)-x), abs(nearest_w2(x)-x), abs(nearest_q1(x)-x)]   
  n = [nearest_l1(x), nearest_l2(x), nearest_w1(x), nearest_w2(x), nearest_q1(x)]
  return n[d.index(min(d))]
  #abs(nearest_q1(x)-x):nearest_q1(x),
  #abs(nearest_q2(x)-x):nearest_q2(x)
  #return d.get(min(d, key=d.get))
  
    
def nearestz(x):
  nz1 = nearest_z1(x)
  nz2 = nearest_z2(x)
  dz1 = abs(nz1-x)
  dz2 = abs(nz2-x)
  if dz1<=dz2:
    return nz1
  else:
    return nz2
   
def nearest_l1(x):
  return round(x/0.24)*0.24
  
def nearest_l2(x):
  d = -0.01 if x>0 else 0.01
  return nearest_l1(x)+d
 
def nearest_w1(x):
  return round(x/0.12)*0.12
  
def nearest_w2(x):
  d = -0.01 if x>0 else 0.01
  return nearest_w1(x)+d
  
def nearest_q1(x):
  return nearest_w1(x)-0.06
  
def nearest_q2(x):
  return nearest_w1(x)+0.06
  
def nearest_z1(x):
  return round(x/0.086)*0.086
  
def nearest_z2(x):
  d = -0.01 if x>0 else 0.01
  return nearest_z1(x)+d  

def register():
  bpy.utils.register_class(BrickOperator)
 
def unregister():
  bpy.utils.unregister_class(BrickOperator)
  
if __name__ == "__main__":  
 register()  
