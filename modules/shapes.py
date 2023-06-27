from lib import *

class Shape:

    _ob = None

    def setLocation(self, at=(0, 0, 0), minx=None, midx=None, maxx=None, miny=None, midy=None, maxy=None, minz=None, midz=None, maxz=None):
        setLocation(self._ob, at, minx, midx, maxx, miny, midy, maxy, minz, midz, maxz)

    def setOrigin(self, origin):
        setOrigin(self._ob, origin)

    def setRotation(self, rot):
        setRotation(self._ob, rot)



class Box(Shape):


  def __init__(self,name=None, origin=None, size=(1, 1, 1), rot=None,
               at=(0, 0, 0),
               minx=None, midx=None, maxx=None,
               miny=None, midy=None, maxy=None,
               minz=None, midz=None, maxz=None):
    self.name = name
    box(name=name,size=size)
    self._ob = bpy.context.object
    self.setLocation(at, minx, midx, maxx, miny, midy, maxy, minz, midz, maxz)
    if origin is not None:
      self.setOrigin(origin)
    if rot is not None:
      self.setRotation(rot)

