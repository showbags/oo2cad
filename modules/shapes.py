from lib import *

class Shape:
  def locate(self, at=(0, 0, 0), minx=None, midx=None, maxx=None, miny=None, midy=None, maxy=None, minz=None, midz=None, maxz=None):
    setLocation(self.ob(), at, minx, midx, maxx, miny, midy, maxy, minz, midz, maxz)

  def setOrigin(self, origin):
    setRotation(self.ob(), origin)

  def rotate(self, rot):
    setRotation(self.ob(), rot)



class Box(Shape):

  def __init__(self,name=None, origin=None, size=(1, 1, 1), rot=(0, 0, 0),
               at=(0, 0, 0),
               minx=None, midx=None, maxx=None,
               miny=None, midy=None, maxy=None,
               minz=None, midz=None, maxz=None):
    self.name = name
    box(name,origin,size,rot,at)
    self.ob = bpy.context.object
    self.locate(at, minx, midx, maxx, miny, midy, maxy, minz, midz, maxz)
    self.setOrigin(origin)
    self.rotate(rot)

  def ob(self):
    return self.ob


