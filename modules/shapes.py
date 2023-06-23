from lib import *

class Box:
    def __init__(self,name=None, origin=None, size=(1, 1, 1), rot=(0, 0, 0),
                 x=0, y=0, z=0):
        self.name = name
        box(name,origin,size,rot,x,y,z)