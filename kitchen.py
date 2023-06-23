import bpy
from lib import *


def run(origo):
    setup()

    #bench1: east
    #bench2: north
    #bench3: west

    bh=0.905 #bench height
    bt=0.04 #bench thickness
    bd=0.6  #bench depth
    kd=3.45    #kitchen depth
    bover=0.065 #bench overhang cupboard
    cd = bd-bover #cupboard depth

    dw = 0.455 #drawer width
    dt = 0.03 #drawer thickness
    d4h = 0.175 #drawer4 height
    d3h = 0.155 #drawer3 height
    d2h = 0.130 #drawer2 height
    d1h = 0.220 #drawer1 height

    di = 0.025 #drawer insets

    cdw = 0.33 #cupbard width
    ch = 0.755 #cupboard height
    kbh = 0.085 #kick board height

    #bench1
    b1w=1.415

    #bench2
    b2w=2.3

    #bench3
    b3w=1.675
    b3o=0.5

    ut=0.020 #dishwasher upright thickness
    ru=0.62  #position of right upright

    bench1 = box(name="bench1", size=(b1w,bd,bt), origin=(0,0,bh-bt))
    cupboard1 = box(name="cupboard1", size=(b1w,cd,bh-bt))

    drawer4 = box(name="drawer4", size=(dw, dt, d4h), origin=(di, cd, kbh))
    drawer3 = box(name="drawer3", size=(dw, dt, d3h), origin=(di, cd, kbh+d4h+di))
    drawer2 = box(name="drawer2", size=(dw, dt, d2h), origin=(di, cd, kbh+d4h+d3h+2*di))
    drawer1 = box(name="drawer1", size=(dw, dt, d1h), origin=(di, cd, kbh+d4h+d3h+d2h+3*di))

    cupboard_door1 = box(name="cupboard door1", size=(cdw, dt, ch), origin=(di+dw+di, cd, bh-bt-di-ch))
    cupboard_door2 = box(name="cupboard door2", size=(cdw, dt, ch), origin=(di+dw+cdw+di, cd, bh-bt-di-ch))
    cd3aw = b1w+bd-2*di-dw-2*cdw-cd
    cupboard_door3a = box(name="cupboard door3a", size=(cd3aw, dt, ch), origin=(2*di+dw+2*cdw, cd, bh-bt-di-ch))
    cd3bw = b2w-2*cdw-cd-dt-ru-ut
    cd3bx = cd+dt
    cupboard_door3b = box(name="cupboard door3b", size=(cd3bw, dt, ch), origin=(b1w+bd-cd, cd+dt, bh-bt-di-ch), rot=(0,0,90))

    bench2 = box(name="bench2", size=(b2w,bd,bt), origin=(0,0,bh-bt))
    bench2_sill = box(name="bench2_sill", size=(b2w-0.48,-0.14, bt), origin=(0.48, 0, bh-bt))
    cupboard2 = box(name="cupboard2", size=(b2w,cd,bh-bt), origin=(0,0,0))

    dwcl = box(name="dwcl", size=(ut,cd,bh-bt), origin=(b2w-ut,0,0))
    dwcr = box(name="dwcr", size=(ut,cd,bh-bt), origin=(b2w-(ut+ru),0,0))
    cupboard_door1 = box(name="cupboard door1", size=(cdw, dt, ch), origin=(b2w-ru-ut-cdw, cd, bh-bt-di-ch))
    cupboard_door2 = box(name="cupboard door2", size=(cdw, dt, ch), origin=(b2w-ru-ut-2*cdw, cd, bh-bt-di-ch))

    pantry_right_wall = wall(2.5, "pantry_right_wall", False, (b2w+0.11,0,0), (0, 0, 90))

    bench2 = join_objects([cupboard2,bench2, bench2_sill,dwcl,dwcr,cupboard_door1,cupboard_door2,pantry_right_wall],newname="bench2")
    set_rotation(bench2,(0,0,90))
    set_location(bench2,(b1w+bd,0,0))

    bench3 = box(name="bench3", size=(b3w,bd,bt), origin=(0,0,bh-bt))
    cupboard3 = box(name="cupboard3", size=(b3w, cd, bh), origin=(0,0,0))

    obw = 0.84 #oven box width
    ohd = bd+0.02 #over hang depth
    obh = 1.8 #oven box height
    ohh = 0.09 #over hang height
    fbd = 0.5 #flu box depth

    oven_box = box(name="oven_box", size=(obw, bd, obh), origin=(b3w, 0, 0))
    over_hang = box(name="over_hang", size=(b3w+obw, ohd, ohh), origin=(0, 0, obh))
    flu_box = box(name="flu_box", size=(b3w+obw, fbd, 1 ), origin = (0, 0, obh+ohh))
    pantry_left_wall = wall(2.5, "pantry_left_wall", False, (0,0,0), (0, 0, 90))

    bench3 = join_objects([cupboard3, bench3, oven_box, over_hang, flu_box, pantry_left_wall], newname="bench3")
    set_rotation(bench3, (0,0,180))
    set_location(bench3, (b1w-b3o,kd,0))

    #kitchen wall with window
    wall(15.5, "wall",True,(b1w+bd+0.23,0,0), (0,0,90))





if __name__ == "__main__":
    run((0,0,0))

    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    #bpy.ops.group.create(name="myGroup")
    #bpy.ops.object.group_link(group="myGroup")
    bpy.ops.wm.save_as_mainfile(filepath='kitchen_out.blend')
