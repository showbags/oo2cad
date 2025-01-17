from lib import *

def boxob():
    bpy.ops.mesh.primitive_cube_add(enter_editmode=False)
    ob = bpy.context.object
    return ob

def cylob():
    bpy.ops.mesh.primitive_cylinder_add(enter_editmode=False, vertices=32)
    ob = bpy.context.object
    return ob

class Shape:

    _ob = None

    def __init__(self, ob=None, name=None, origin=None, size=(1, 1, 1), rot=None,
                 at=(0, 0, 0),
                 minx=None, midx=None, maxx=None,
                 miny=None, midy=None, maxy=None,
                 minz=None, midz=None, maxz=None):
        self.name = name
        ob.name = name
        ob.show_name = True
        ob.data.name = name + 'Mesh'
        ob.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
        bpy.ops.object.transform_apply(scale=True)

        self._ob = bpy.context.object
        self.setLocation(at, minx, midx, maxx, miny, midy, maxy, minz, midz, maxz)
        if origin is not None:
            self.setOrigin(origin)
        if rot is not None:
            self.setRotation(rot)

    def setLocation(self, at=(0, 0, 0), minx=None, midx=None, maxx=None, miny=None, midy=None, maxy=None, minz=None, midz=None, maxz=None):
        setLocation(self._ob, at, minx, midx, maxx, miny, midy, maxy, minz, midz, maxz)

    def setOrigin(self, origin):
        setOrigin(self._ob, origin)

    def setRotation(self, rot):
        setRotation(self._ob, rot)

    def subtract(self, shape):
        subtract(self._ob, shape._ob)

    def intersect(self, shape):
        intersect(self._ob, shape._ob)



class Box(Shape):
    def __init__(self,name=None, origin=None, size=(1, 1, 1), rot=None,
                 at=(0, 0, 0),
                 minx=None, midx=None, maxx=None,
                 miny=None, midy=None, maxy=None,
                 minz=None, midz=None, maxz=None):
        super().__init__(boxob(), name, origin, size, rot, at, minx,midx,maxx, miny,midy,maxy, minz,midz,maxz)

class Cylinder(Shape):
    def __init__(self,name=None, origin=None, size=(1, 1, 1), rot=None,
                 at=(0, 0, 0),
                 minx=None, midx=None, maxx=None,
                 miny=None, midy=None, maxy=None,
                 minz=None, midz=None, maxz=None):
        super().__init__(cylob(), name, origin, size, rot, at, minx,midx,maxx, miny,midy,maxy, minz,midz,maxz)