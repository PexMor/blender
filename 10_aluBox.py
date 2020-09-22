import bpy
import bmesh

from bmesh.types import BMVert

import mathutils
from mathutils import Matrix
from mathutils import Vector

import math
from math import radians

scene = bpy.context.scene
C = bpy.context
# size of the basic unit in metres
UNIT = 0.01 * 100

# https://blender.stackexchange.com/questions/134878/selecting-curve-after-importing-svg-using-bpy
# https://blender.stackexchange.com/questions/48268/python-resize-imported-svg/48281#48281

print("----===[ exec started")
import os
print("HOME:",os.environ['HOME'])
PWD = os.environ['PWD']
print("PWD:",PWD)
# print(bpy.utils.script_path_user())
SF = os.path.dirname(os.path.realpath(__file__))
print("SF:",SF)
SF = "."

print("----===[ clean existing objects")
# Select objects by type
for o in bpy.context.scene.objects:
    print(o.name,o.type)
    if o.type == 'MESH':
        o.select_set(True)
    elif o.type == 'CURVE':
        o.select_set(True)
    elif o.type == 'ANIMATION':
        o.select_set(True)
    elif o.type == 'CAMERA':
        o.select_set(True)
    else:
        o.select_set(False)
# Call the operator only once
bpy.ops.object.delete()
bpy.ops.object.select_by_type(type='CAMERA')
bpy.ops.object.delete()

def loadBasicCurve():
    print("----===[ capture existing objects")
    names_pre_import = set([ o.name for o in C.scene.objects ])
    pth = SF+'/resources'
    # https://www.thingiverse.com/thing:1001461/files
    name = '2020.svg'
    fp = pth + "/" + name
    bpy.ops.import_curve.svg(filepath = fp)
    # Names of all objects after importing the SVG
    names_post_import = set([ o.name for o in C.scene.objects ])
    # Perform set difference to find the new name and store it
    new_object_name = names_post_import.difference( names_pre_import ).pop()
    print("ObjName:",new_object_name)
    # Reference new object
    o = C.scene.objects[ new_object_name ]
    o.name = "basicShape"
    o.data.name = "basicShape"
    o.select_set(True)
    C.view_layer.objects.active = o
    bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
    bpy.ops.transform.resize(value=(UNIT/2.13329,UNIT/2.1328,1))
    bpy.ops.object.select_all(action='DESELECT')
    print("...",o.dimensions,o.location)
    # attach object to root collection
    scene.collection.objects.link(o)
    col = bpy.data.collections.find(name)
    print("collection:",col)
    if col>-1:
        co = bpy.data.collections[col]
        co.objects.unlink(o)
        bpy.data.collections.remove(co)
    return o

def copyObj(orig,name):
    cpy = orig.copy()
    cpy.data = orig.data.copy()
    cpy.name = name
    cpy.data.name = name
    scene.collection.objects.link(cpy)
    return cpy

basicShape = loadBasicCurve()
print("basicShape.dimensions:",basicShape.dimensions,".location:",basicShape.location)

def draw(basicShape,olen,pos,which_angle,name):
    o = copyObj(basicShape,name)
    o.select_set(True)
    C.view_layer.objects.active = o
    bpy.context.object.data.dimensions = '2D'
    bpy.context.object.data.fill_mode = 'BOTH'
    bpy.context.object.data.extrude = olen / 2
    bpy.ops.object.convert(target='MESH')
    mvdist = olen / 2
    HUNIT = UNIT / 2
    if which_angle==0:
        o.location = mathutils.Vector((pos[0]+HUNIT,pos[1]+HUNIT,pos[2]+mvdist))
    elif which_angle==1:
        o.rotation_euler[0] = math.radians(90)
        o.location = mathutils.Vector((pos[0]+HUNIT,pos[1]+mvdist,pos[2]+HUNIT))
    else:
        o.rotation_euler[1] = math.radians(90)
        o.location = mathutils.Vector((pos[0]+mvdist,pos[1]+HUNIT,pos[2]+HUNIT))

def rodX(olen,pos):
    pos = tuple( UNIT * no for no in pos )
    draw(basicShape,olen*UNIT,pos,2,"x-rod")

def rodY(olen,pos):
    pos = tuple( UNIT * no for no in pos )
    draw(basicShape,olen*UNIT,pos,1,"y-rod")

def rodZ(olen,pos):
    pos = tuple( UNIT * no for no in pos )
    draw(basicShape,olen*UNIT,pos,0,"z-rod")

#draw(basicShape,UNIT,(0,0,0),0,"svisle")
#draw(basicShape,UNIT,(0,0,0),1,"vodo")
#draw(basicShape,UNIT,(0,0,0),2,"dopredu")

rlen = 10
rodX(rlen,(1,0,0))
rodX(rlen,(1,0,1+rlen))
rodX(rlen,(1,1+rlen,0))
rodX(rlen,(1,1+rlen,1+rlen))

rodY(rlen,(0,1,0))
rodY(rlen,(0,1,1+rlen))
rodY(rlen,(1+rlen,1,0))
rodY(rlen,(1+rlen,1,1+rlen))

rodZ(rlen,(0,0,1))
rodZ(rlen,(1+rlen,0,1))
rodZ(rlen,(0,1+rlen,1))
rodZ(rlen,(1+rlen,1+rlen,1))

rodZ(rlen,(1+rlen/2,1+rlen/2,1))

def add_cam(location, rotation):
    bpy.ops.object.camera_add(location=location, rotation=rotation)
    return bpy.context.active_object

def add_empty(location):
    bpy.ops.object.empty_add(location=location)
    return bpy.context.active_object    

def look_at(obj_camera, point=mathutils.Vector((0.0, 0.0, 0.0)), distance=10.0):
    # loc_camera = obj_camera.matrix_world.to_translation()

    direction = obj_camera.location - point
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()
    print(rot_quat)
    obj_camera.location = rot_quat * mathutils.Quaternion((0.0, 0.0, 0.0, distance))

scene.render.resolution_x = 1920 / 5
scene.render.resolution_y = 1080 / 5
    
XDELTA = UNIT * 6.5
YDELTA = UNIT * 6.5
ZDELTA = UNIT * 5.5
CDIST = 20
cam = add_cam(location=(0+XDELTA, -CDIST+YDELTA, ZDELTA), rotation=(math.pi/2, 0, 0))

direction = cam.location - Vector((0,0,0))

rot = direction.to_track_quat('Z', 'Y').to_matrix().to_4x4()
loc = mathutils.Matrix.Translation(cam.location)

cam.matrix_world =  loc @ rot

up = cam.matrix_world.to_quaternion() @ Vector((0.0, 1.0, 0.0))
cam_direction = cam.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))
print("UP:",up,"DIR:",cam_direction,"Q:",cam.matrix_world.to_quaternion())

empty = add_empty(location=(0+XDELTA, 0+YDELTA, 0+ZDELTA))
cam.parent = empty
# look_at(cam,Vector((0+DELTA,0+DELTA,0+DELTA)))

num_frames = 10
gamma = math.pi * 2 / num_frames
for i in range(1, num_frames+1):
    empty.rotation_euler[2] = gamma * i
    empty.keyframe_insert(data_path='rotation_euler', frame=i, index=-1)

scene.camera = cam
cam.data.lens = 20.0
# cam.data.dof_distance = 7.0

scene.render.line_thickness = 0.5
# bpy.context.scene.svg_export.mode = 'FRAME'
bpy.context.scene.svg_export.use_svg_export = True
scene.svg_export.mode = 'ANIMATION'
bpy.context.scene.svg_export.split_at_invisible = True
bpy.context.scene.svg_export.object_fill = True
bpy.context.scene.render.use_freestyle = True

bpy.data.scenes["Scene"].frame_end = num_frames
bpy.data.scenes["Scene"].render.image_settings.file_format = 'AVI_JPEG'

bpy.context.scene.render.filepath = os.environ['PWD']+'/render/output'
bpy.ops.render.render(write_still = False, animation = True)
