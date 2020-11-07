import bpy
import sys, os
from mathutils import *

# INSTRUCTIONS
# place gradient_blank.blend, import_file.py, and your .obj in the same directory

#TODO make a better parser + optional config
#TODO organize a bit better

# EDIT THIS
output_folder = "output_small/small_render_"
output_blend = "small.blend"
obj_name = "small"
res_x = 3840
res_y = 2160
use_CUDA = True
use_obj = False
use_ply = not use_obj

#TODO: eventually read from a config file in directory
if os.path.exists("render.config"):
    with f as open("render.config", "r"):
        output_folder = f.readline()
        output_blend = f.readline()
        obj_name = f.readline()
        if f.readline().lower().contains("p"):
            use_ply = True
            use_obj = not use_ply

# just for debug print the config
def print_config():
    print("Using config:\n"\
        "output_folder/pre: " + output_folder + \
        "output_blend:      " + output_blend + \
        "obj_name:          " + obj_name + \
        "res:               " + str(res_x) + "x" + str(res_y))
print_config()

# get prefs
prefs = bpy.context.preferences.addons['cycles'].preferences

# set CUDA
if use_CUDA:
    prefs.get_devices()
    
    prefs.compute_device_type = 'CUDA'
    prefs.devices[0].use = True
    
    # make sure we got CUDA device
    print(prefs.devices[0])

# set output path
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
bpy.context.scene.render.filepath = output_folder

# set render tile size
for scene in bpy.data.scenes:
    scene.render.tile_x = 512
    scene.render.tile_y = 512

# set output resolution
for scene in bpy.data.scenes:
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    
# save preferences
bpy.ops.wm.save_userpref()

# helper function
def get_obj_from_name(desired_name):
    all_objects = bpy.context.selectable_objects
    for o in all_objects:
        if desired_name in o.name:
            return o

# imported tile settings
desired_dim = 6.3 #(meters)
desired_x = -1
desired_y = 1

# import the object
if use_obj:
	bpy.ops.import_scene.obj(filepath=obj_name+".obj", axis_forward="Y", axis_up="Z", use_image_search=False)
else:
	bpy.ops.import_mesh.ply(filepath=obj_name+".ply")

print("Started importing " + obj_name)
imported_obj = get_obj_from_name(obj_name)
print("Finished importing")
"""
# get dim of object and set ratio
x, y, z = imported_obj.dimensions
scale_ratio = max(x, y) / desired_dim

# scale it to fit in dimensions
for i in range(0, 1):
    imported_obj.scale = (1.0 / scale_ratio, 1.0 / scale_ratio, 1)
imported_obj.dimensions[2] = 0.22

# move it back to the center
# idk why but it needs to do this several times
for j in range(0, 2):
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
    imported_obj.location = (desired_x, desired_y, 0)

# set back to default
bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN")
"""
# set plane to be at the lowest point of imported object
plane = get_obj_from_name("Plane")
new_z = imported_obj.location[2]
bbox = [Vector(v) @ imported_obj.matrix_world for v in imported_obj.bound_box]
lz = 10000
for v in bbox:
    if v[2] < lz:
        lz = v[2]
plane.location[2] = lz - 0.05

# set material of imported tile to gradient
gradient = bpy.data.materials['gradient']
if len(imported_obj.material_slots) < 1:
    imported_obj.data.materials.append(gradient)
else:
    imported_obj.material_slots[0].material = gradient

bpy.ops.wm.save_as_mainfile(filepath=output_blend)
