import bpy
from lib import *


def run(origo):
  setup()

  #table top
  ttw=0.515
  ttd=0.685
  ttt=0.038

  table_top = box(name="table top", size=(ttw,ttd,ttt))

  #miter slots
  msw = 0.018
  msd = 0.010
  m = 0.001
  m2 = 2*m
  miter_slot_left = box(name="mitre slot left", size=(msw, ttd+m2, msd+m ), origin=(0.128, -m, ttt-msd))
  miter_slot_right = box(name="mitre slot right", size=(msw, ttd+m2, msd+m ), origin=(ttw-0.096-msw, -m, ttt-msd))

  subtract( table_top, miter_slot_left)
  subtract( table_top, miter_slot_right)

  #wings
  ww = 0.255
  left_wing = box(name="left wing", size=(ww,ttd,ttt), origin=(-ww,0,0))
  right_wing = box(name="right wing", size=(ww,ttd,ttt), origin=(ttw,0,0))

  #motor box
  mbw = 0.415
  mbd = 0.490
  mbh = 0.290

  motor_box = box(name="motor box", size=(mbw,mbd,mbh), origin=((ttw-mbw)/2, (ttd-mbd)/2, -mbh))

  #base box
  bbh = 0.4

  base_box = box(name="base box", size=(mbw,mbd,bbh), origin=((ttw-mbw)/2, (ttd-mbd)/2, -mbh-bbh))

  #front fence rail
  rh = 1.143
  rw = 0.033 #diameter
  rd = 0.033 #diameter

  front_rail = cylinder(name="front rail", size=(rd,rd,rh), origin=(-ww+0.085, -0.05, -0.01), rot=(0,90,0))
  back_rail = cylinder(name="back rail", size=(rd,rd,rh), origin=(-ww+0.085, ttd+0.05, -0.01), rot=(0,90,0))

if __name__ == "__main__":
  run((0,0,0))

  bpy.ops.object.mode_set(mode='OBJECT')
  bpy.ops.object.select_all(action='SELECT')
  bpy.ops.collection.create(name="myGroup")
  bpy.ops.collection.objects_add_active(collection="myGroup")
  #bpy.ops.object.collection_link(collection="myGroup")
  #bpy.ops.wm.save_as_mainfile(filepath='table_saw_out.blend')
