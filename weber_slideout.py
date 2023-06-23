import bpy
from lib import *

tunnel_h = 0.500
tunnel_w = 0.550
tunnel_l = 2.000
tunnel_opening_h = 0.34
tunnel_opening_w = 0.51
tunnel_opening_depth = 0.02  # the thickness of the lip of the opening
tunnel_cut_z = 0.02  # height of the opening above floor of tunnel
bench_thickness = 0.016
bench_l = 0.85
bench_w = tunnel_opening_w - 0.02

weber_base_w = 0.560
weber_base_l = 0.330
weber_base_h = 0.009 #9mm plywood

def tunnel(origo):
    t = 0.01  # the thickness of the tunnel material
    t2 = t / 2

    tunnel = box(name="tunnel", size=(tunnel_w + t, tunnel_l + t, tunnel_h + t), origin=origo)
    tunnel_cut = box(name="tunnel_cut", size=(tunnel_w, tunnel_l - tunnel_opening_depth + t2, tunnel_h),
                     align_midx=tunnel, y=tunnel_opening_depth, align_midz=tunnel)
    subtract(tunnel, tunnel_cut)
    tunnel_opening_cut = box(name="tunnel_opening_cut", size=(tunnel_opening_w, 2, tunnel_opening_h, tunnel_h),
                             align_midx=tunnel, z=tunnel_cut_z)
    subtract(tunnel, tunnel_opening_cut)


def bench(origo):

    bench_h = bench_thickness

    tunnel = get('tunnel')

    box(name="bench", size=(bench_w, bench_l, bench_h), align_midx=tunnel, y=tunnel_opening_depth, z=tunnel_cut_z)


def weber(origo):
    # weber_w = 0.41
    weber_w = 0.34
    weber_h = 0.25
    weber_l = 0.81
    # weber_o = vector_add( origo, (tunnel_w/2-weber_w/2, tunnel_opening_depth, tunnel_cut_z+bench_thickness))
    # box( name="weber", size=(weber_w, weber_l, weber_h), origin=weber_o)
    bench = get("bench")
    weber = box(name="weber", y=0.01, size=(weber_w, weber_l, weber_h), align_midx=bench, z=maxz(bench))
    slide_travel = 0.75
    box(name="weber2", y=miny(weber)-slide_travel, size=(weber_w, weber_l, weber_h), align_midx=weber, z=maxz(bench))
    lid_w = 0.45
    lid_l = 0.61
    lid_h = 0.2
    tunnel = get("tunnel")
    weber_lid = box(name="lid", size=(lid_w, lid_l, lid_h), align_midx=bench, y=0.1, align_maxz=tunnel)
    weber.color=[0,0,0,1]
    weber_lid.color=[1,0,0,1]

def drawer_slide(orig):
    slide_w = 0.01 #slide width
    slide_h = 0.03 #slide height
    slide_l = bench_l #slide length
    slide_mt = 0.002 #slide material thickness

    bench = get("bench")
    rail_slider = box(name="rail_slider1", size=(slide_w, slide_l, 0.014), x=maxx(bench), y=miny(bench), align_midz=bench)

    slide_box = box(name="slide_box1", size=(slide_w,slide_l,slide_h))
    slide_box_cut = box(name="slide_box_cut", size=(slide_w,slide_l-2*slide_mt,2*slide_h), x=+slide_mt, y=slide_mt, z=-slide_h/2)
    subtract(slide_box, slide_box_cut)

    set_min_x(slide_box, maxx(rail_slider))
    set_min_y(slide_box, miny(rail_slider))
    set_mid_z(slide_box, midz(rail_slider))

    slide_box.color=[0.5,0.5,0.5,1.0]
    xmirror(rail_slider, offset=-bench_w, name="rail_slider2")
    xmirror(slide_box, offset=-(bench_w+slide_w*2), name="slide_box2")


    return slide_box

def weber_plate():
    bench = get("bench")
    cleat_h = 0.01
    cleat_w = 0.2
    plate = box(name="weber_plate", size=(weber_base_w, weber_base_l, weber_base_h), align_midx=bench, align_miny=bench, above=bench )
    cleat = box(name="cleat", size=(cleat_w, 0.015, cleat_h), align_midx=plate, align_maxy=plate, below=plate)

    #edge = nearest_edge(cleat, (0,0.5,1))
    edge = get_edge(cleat, 11)
    dovetail_angle=math.radians(10)
    move_edge( cleat, edge, (0,cleat_h*math.sin(dovetail_angle),0))

    #copy the cleat for chopping into bench
    cleat_extrude = duplicate(cleat, name="cleat_extrude")
    move_face(cleat_extrude, cleat_extrude.data.polygons[0], (-0.01,0,0))
    move_face(cleat_extrude, cleat_extrude.data.polygons[2], (+0.01,0,0))
    move_face(cleat_extrude, cleat_extrude.data.polygons[5], (0,0,0.1))
    subtract(bench, cleat_extrude)

    join(["weber_plate","cleat"], newname="weber_plate")

def run(origo):
    setup()

    tunnel(origo)
    bench(origo)
    weber(origo)


    slide = drawer_slide(origo)
    weber_plate()

    join(["bench","rail_slider1","rail_slider2"], newname="bench_and_sliders")
    show_only(get("bench_and_sliders"), get("weber_plate"))


    #center_view(slide, 'TOP')

    set_orthographic()



if __name__ == "__main__":
    run((0, 0, 0))
    set_shading_mode(mode="WIREFRAME", shading='OBJECT')