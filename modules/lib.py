import bpy
import math
from mathutils.bvhtree import BVHTree
from mathutils import Vector

def editMode():
    bpy.ops.object.mode_set(mode='EDIT')


def objectMode():
    bpy.ops.object.mode_set(mode='OBJECT')


def cleanup(ob):
    bpy.context.view_layer.objects.active = ob  # bpy.context.scene.objects.get(ob)
    # Clean up the mesh a bit
    editMode()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.normals_make_consistent(inside=False)
    objectMode()


def createMeshFromData(verts, faces, name='Mesh', origin=(0, 0, 0)):
    # Create mesh and object
    me = bpy.data.meshes.new(name + 'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True

    # Link object to scene and make active
    scn = bpy.context.scene
    # scn.objects.link(ob)
    bpy.context.collection.objects.link(ob)
    # scn.objects.active = ob
    bpy.context.object = ob
    ob.select_set(True)

    # Create mesh from given verts, faces.
    me.from_pydata(verts, [], faces)
    # Update mesh with new data
    me.update()

    cleanup(ob)

    return ob


def zface(w, l):
    return (0, 0, 0), (w, 0, 0), (w, l, 0), (0, l, 0)


def xface(l, h):
    return (0, 0, 0), (0, l, 0), (0, l, h), (0, 0, h)


def yface(w, h):
    return (0, 0, 0), (w, 0, 0), (w, 0, h), (0, 0, h)


def makeFaces(verts):
    faces = []
    for i in range(int(len(verts) / 4)):
        face = (i * 4, i * 4 + 1, i * 4 + 2, i * 4 + 3)
        faces.append(face)
    return faces

def select(name):
  return bpy.ops.object.select_pattern(pattern=name)

def select(ob):
  ob.select_set(True)

def deselect(ob):
  ob.select_set(False)

def selectall():
  bpy.ops.object.select_all(action='SELECT')

def deselectall():
  bpy.ops.object.select_all(action='DESELECT')

def select_only(*objs):
  for ob in bpy.data.objects:
    ob.select_set(False)
  for ob in objs:
    ob.select_set(False)

def removeall():
  selectall()
  bpy.ops.object.delete(use_global=False)

def setup():
    removeall()
    bpy.context.preferences.view.show_splash = False
    # Set to mm
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 0.001
    # Get the active camera
    camera = bpy.context.scene.camera

    # Iterate through all areas in the current screen
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            # Access the 3D Viewport space
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    # Set the back clipping distance
                    space.clip_end = 10000.0  # Set this to your desired value


def setLocation(ob, loc=(0,0,0),
                minx=None, miny=None, minz=None,
                maxx=None, maxy=None, maxz=None,
                midx=None, midy=None, midz=None):
  x=loc[0]
  y=loc[1]
  z=loc[2]

  size=ob.dimensions

  # Honour any alignments requested
  x = x if minx is None else calcmaxx(minx) + size[0] / 2
  y = y if miny is None else calcminy(miny) + size[1] / 2
  z = z if minz is None else calcminz(minz) + size[2] / 2

  x = x if maxx is None else calcmaxx(maxx) - size[0] / 2
  y = y if maxy is None else calcmaxy(maxy) - size[1] / 2
  z = z if maxz is None else calcmaxz(maxz) - size[2] / 2

  x = x if midx is None else calcmidx(midx)
  y = y if midy is None else calcmidy(midy)
  z = z if midz is None else calcmidz(midz)

  print ('x,y,z: ',x,y,z)
  ob.location = (x, y, z)
  bpy.ops.object.transform_apply(location=True)
  bpy.ops.object.transforms_to_deltas(mode='ALL')


def setOrigin(ob, origin):
  select(ob)
  saved_location = bpy.context.scene.cursor.location.copy()
  bpy.context.scene.cursor.location = origin
  bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
  bpy.context.scene.cursor.location = saved_location


def setRotation(obj, rot):
  obj.rotation_euler = (math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]))
  #bpy.ops.object.transform_apply(rotation=True)
  #bpy.ops.object.transforms_to_deltas(mode='ALL')
  bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

def box(name=None, size=(1, 1, 1), at=(0, 0, 0),
        minx=None, midx=None, maxx=None,
        miny=None, midy=None, maxy=None,
        minz=None, midz=None, maxz=None):

    bpy.ops.mesh.primitive_cube_add(enter_editmode=False)
    ob = bpy.context.object
    name = 'Box' if name is None else name
    ob.name = name
    ob.show_name = True
    ob.data.name = name + 'Mesh'
    ob.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)

    #setLocation(ob, at, minx, midx, maxx, miny, midy, maxy, minz, midz, maxz)

    return ob

def cylinder(name=None, origin=(0, 0, 0), size=(1, 1, 1), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(
        enter_editmode=False)

    ob = bpy.context.object
    name = 'Cylinder' if name is None else name
    ob.name = name
    ob.show_name = True
    ob.data.name = name + 'Mesh'
    ob.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    ob.location = (origin[0], origin[1], origin[2] + size[2] / 2)

    saved_location = bpy.context.scene.cursor.location.copy()
    bpy.context.scene.cursor.location = origin
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor.location = saved_location

    setRotation(ob, rot)
    return ob


def remove(ob):
    # bpy.context.scene.objects.unlink(ob)
    objectMode()
    # deselect all objects
    bpy.ops.object.select_all(action='DESELECT')
    # select the object
    select(ob)
    # delete all selected objects
    bpy.ops.object.delete()


def subtract(target, sub, keep=False):
    # bpy.context.object = target
    bpy.context.view_layer.objects.active = target
    boo = target.modifiers.new('Booh', 'BOOLEAN')
    boo.object = sub
    boo.operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply(modifier="Booh")
    if not keep:
        remove(sub)

    cleanup(target)

def intersect(target, inter, keep=False):
    # bpy.context.object = target
    bpy.context.view_layer.objects.active = target
    boo = target.modifiers.new('Booh', 'BOOLEAN')
    boo.object = inter
    boo.operation = 'INTERSECT'
    bpy.ops.object.modifier_apply(modifier="Booh")
    if not keep:
        remove(inter)

    cleanup(target)


def vector_add(vec1, vec2):
    return vec1[0] + vec2[0], vec1[1] + vec2[1], vec1[2] + vec2[2]


def duplicate(target, name=None, off=(0, 0, 0), ncopy=1):
    ob = None
    for i in range(ncopy):
        me_copy = target.data.copy() # use current object's data
        name_use = name if name is not None and ncopy == 1 else target.name + "_duplicate_" + str(i)
        ob = bpy.data.objects.new(name_use, me_copy)
        ob.show_name = True
        ob.location[0] = (i + 1) * off[0] + target.location[0]
        ob.location[1] = (i + 1) * off[1] + target.location[1]
        ob.location[2] = (i + 1) * off[2] + target.location[2]
        bpy.context.collection.objects.link(ob)

    return ob

def xmirror(target, offset=0, name=None):
  ob = duplicate(target, name=name)
  #select_only(ob)
  #bpy.ops.transform.mirror(constraint_axis=(True, False, False))
  ob.scale[0]*=-1
  if (offset>0):
    set_max_x(ob, -calcmaxx(target) - offset)
  elif (offset<0):
    set_min_x(ob, -calcminx(target) - offset)
  else:
    set_mid_x(ob, -calcmidx(target) - offset)
  ob.location.x = ob.location.x *-1

def set_min_x(ob, x):
  shift(ob, (x - calcminx(ob), 0, 0))

def set_min_y(ob, y):
  shift(ob, (0, y - calcminy(ob), 0))

def set_min_z(ob, z):
  shift(ob, (0, 0, z - calcminz(ob)))

def set_max_x(ob, x):
  shift(ob, (x - calcmaxx(ob), 0, 0))

def set_max_y(ob, y):
  shift(ob, (0, y - calcmaxy(ob), 0))

def set_max_z(ob, z):
  shift(ob, (0, 0, z - calcmaxz(ob)))

def set_mid_x(ob, x):
  shift(ob, (x - calcmidx(ob), 0, 0))

def set_mid_y(ob, y):
  shift(ob, (0, y - calcmidy(ob), 0))

def set_mid_z(ob, z):
  shift(ob, (0, 0, z - calcmidz(ob)))
  

def extrudex(dist):
    extrude((dist, 0, 0))
    return

def extrudey(dist):
    extrude((0, dist, 0))
    return

def extrudez(dist):
    extrude((0, 0, dist))
    return

def extrude(vec):
    editMode()
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": vec})
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    objectMode()
    return

def move_edge( object, edge, shift):
  object.data.vertices[edge.vertices[0]].co[0]+=shift[0]
  object.data.vertices[edge.vertices[0]].co[1]+=shift[1]
  object.data.vertices[edge.vertices[0]].co[2]+=shift[2]
  object.data.vertices[edge.vertices[1]].co[0]+=shift[0]
  object.data.vertices[edge.vertices[1]].co[1]+=shift[1]
  object.data.vertices[edge.vertices[1]].co[2]+=shift[2]

def move_face( obj, face, shift):
  for idx in face.vertices:
    obj.data.vertices[idx].co[0]+=shift[0]
    obj.data.vertices[idx].co[1]+=shift[1]
    obj.data.vertices[idx].co[2]+=shift[2]

  #for vert in face.vertices:
  #  object.data.vertices[edge.vertices[0]].co[0]+=shift[0]
  #  object.data.vertices[edge.vertices[0]].co[1]+=shift[1]
  #  object.data.vertices[edge.vertices[0]].co[2]+=shift[2]


def get_edge(obj, index):
  return obj.data.edges[index]

def nearest_edge(obj, location):
  # Get the object and its mesh
  mesh = obj.data
  matrix = obj.matrix_world

  # Get vertices locations
  vertices = [matrix @ v.co for v in mesh.vertices]
  # Construct polygons from edges
  polygons = [(e.vertices[0], e.vertices[1], e.vertices[0]) for e in mesh.edges]

  # Create a BVH Tree from it
  tree = BVHTree.FromPolygons( vertices, polygons, all_triangles = True )

  # Search for a location
  location = Vector( location )

  # Query the tree
  found_location, normal, index, distance = tree.find_nearest( location )

  return mesh.edges[index]

def shift(ob, shift_vec):
    ob.location.x+=shift_vec[0]
    ob.location.y+=shift_vec[1]
    ob.location.z+=shift_vec[2]

def join(names, newname="joined"):
    select_only()
    for name in names:
        select(name)
    print("calling join")
    bpy.context.view_layer.objects.active=get(names[0])
    print ('bpy.context.active_object =', bpy.context.active_object)
    bpy.ops.object.join()
    print("done called join")
    bpy.context.object.name = newname
    return bpy.context.object


def join_objects(objs, newname="joined"):
    # bpy.context.object=objs[0]
    for obj in objs:
        select(obj.name)
    bpy.ops.object.join()
    bpy.context.object.name = newname
    return bpy.context.object

def get(name):
    return bpy.data.objects[name]

def show_only(*objs):
    for ob in bpy.data.objects:
        ob.hide_set(True)
    for ob in objs:
        ob.hide_set(False)


def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step


def wall(xbricks, name="wall", double_brick=True, origin=(0, 0, 0), rot=(0, 0, 0)):
    ixbricks = math.ceil(xbricks)  # number of individual whole or half bricks
    width = 0.230 * xbricks + 0.010 * (ixbricks - 1)
    zbricks = 33  # number of courses
    height = zbricks * 0.076 + 0.010 * (zbricks - 1)
    if double_brick:
        depth = 0.230
    else:
        depth = 0.110
    return box(name, origin, (width, depth, height), rot)


def calcminx(ob):
    return ob[0] if isinstance(ob,tuple) else ob.location[0] - ob.dimensions[0] / 2

def calcminy(ob):
    return ob[1] if isinstance(ob,tuple) else ob.location[1] - ob.dimensions[1] / 2

def calcminz(ob):
    return ob[2] if isinstance(ob,tuple) else ob.location[2] - ob.dimensions[2] / 2


def calcmaxx(ob):
    return ob[0] if isinstance(ob,tuple) else calcminx(ob) + ob.dimensions[0]

def calcmaxy(ob):
    return ob[1] if isinstance(ob,tuple) else calcminy(ob) + ob.dimensions[1]

def calcmaxz(ob):
    return ob[2] if isinstance(ob,tuple) else calcminz(ob) + ob.dimensions[2]


def calcmidx(ob):
    return ob[0] if isinstance(ob,tuple) else (calcmaxx(ob) + calcminx(ob)) / 2

def calcmidy(ob):
    return ob[1] if isinstance(ob,tuple) else (calcmaxy(ob) + calcminy(ob)) / 2

def calcmidz(ob):
    return ob[2] if isinstance(ob,tuple) else (calcmaxz(ob) + calcminz(ob)) / 2


def size_x(ob):
  return ob.dimensions[0]

def size_y(ob):
  return ob.dimensions[1]

def size_z(ob):
  return ob.dimensions[2]

def set_orthographic():
    for i, a in enumerate(bpy.context.screen.areas):
      if a.type == "VIEW_3D":
        space = a.spaces.active
        space.region_3d.view_perspective = 'ORTHO'

# Center the view on this object, view_angle could be 'LEFT', 'RIGHT', 'BOTTOM', 'TOP', 'FRONT', or 'BACK'
def center_view(ob, view_angle=None):

    ob.select_set(True)
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            ctx = bpy.context.copy()
            ctx['area'] = area
            ctx['region'] = area.regions[-1]

            bpy.ops.view3d.view_selected(ctx)
            bpy.ops.view3d.snap_cursor_to_selected(ctx)

            cursor_location = bpy.context.scene.cursor.location.copy()
            # center the cursor on the active item
            bpy.ops.view3d.snap_cursor_to_selected(ctx)
            # center the view on the cursor
            bpy.ops.view3d.view_center_cursor(ctx)
            if view_angle is not None:
              bpy.ops.view3d.view_axis(ctx, type=view_angle)

            # reset the cursor location
            bpy.context.scene.cursor.location = cursor_location
            break





def set_shading_mode(mode="SOLID", screens=[], shading='OBJECT'):
    """
  Performs an action analogous to clicking on the display/shade button of
  the 3D view. Mode is one of "RENDERED", "MATERIAL", "SOLID", "WIREFRAME".
  The change is applied to the given collection of bpy.data.screens.
  If none is given, the function is applied to bpy.context.screen (the
  active screen) only. E.g. set all screens to rendered mode:
    set_shading_mode("RENDERED", bpy.data.screens)
  """
    screens = screens if screens else [bpy.context.screen]
    for s in screens:
        for spc in s.areas:
            if spc.type == "VIEW_3D":
                spc.spaces[0].shading.type = mode
                #if (mode is "WIREFRAME"):
                spc.spaces[0].shading.color_type='OBJECT' #Doesn't seem to do anything
                break  # we expect at most 1 VIEW_3D space