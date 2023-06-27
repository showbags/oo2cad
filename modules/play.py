import bpy
import bmesh
from mathutils import Vector

from lib import *
from shapes import *

def make_box():
  #table top
  ttw=0.515
  ttd=0.685
  ttt=0.38
  return box(name="table top", size=(ttw,ttd,ttt))

def bevel_edge():
  table_top = make_box()
  objectMode()

  edge = nearest_edge(table_top, (0,0.5,1))
  move_edge( table_top, edge, (0.2,0,0))



def scale_single_face():
  table_top = make_box()

  editMode()

  bm = bmesh.from_edit_mesh(table_top.data)
  bm.faces.ensure_lookup_table()

  # deselect all vertices
  editMode()
  bpy.ops.mesh.select_all(action='DESELECT')

  objectMode()

  #Selects faces going side
  for face in table_top.data.polygons:
    face.select = GoingDown( face.normal )

  editMode()

  bpy.ops.transform.resize(value=(1,2,1))

def NormalInDirection( normal, direction, limit = 0.5 ):
  return direction.dot( normal ) > limit

def GoingUp( normal, limit = 0.5 ):
  return NormalInDirection( normal, Vector( (0, 0, 1 ) ), limit )

def GoingDown( normal, limit = 0.5 ):
  return NormalInDirection( normal, Vector( (0, 0, -1 ) ), limit )

def GoingSide( normal, limit = 0.5 ):
  return GoingUp( normal, limit ) == False and GoingDown( normal, limit ) == False


def parenting():
  parent_box = box(name="parent", size=(2,2,2), align_minx=(0,0,0), origin=(1,2,3), rot=(0,0,45))
  #child_box = box(name="child", size=(2,1,1), left=(0,0,0))
  #TODO: make a function for parenting
  #TODO: in that function we need to take the parents transform away from the child otherwise the following call will move it
  #child_box.parent=parent_box

def boxclass():
  box = Box(name="first_box", size=(4,2,2), origin=(0,0,0), rot=(0,0,0), at=(-2,0,0))

def run():
  setup()
  boxclass()


if __name__ == "__main__":
  run()


#API concepts
#box = Box( at=(1,2,3), size=(3,4,5), color=green )
#ball = Sphere( r=2.3, above=box ) #
#rotated_box = Box( at=box, rotate=(0,0.23,0) )


