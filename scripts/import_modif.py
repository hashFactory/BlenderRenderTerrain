import bpy
import sys, os
from mathutils import *

def get_obj_from_name(desired_name):
    all_objects = bpy.context.selectable_objects
    for o in all_objects:
        if desired_name in o.name:
            return o

# setup variables
obj_name = "ri"
file = "/Users/tristan/Downloads/ri.ply"

# setting
desired_dim = 6.3 #(meters)
desired_x = -1
desired_y = 1

# import the object
bpy.ops.import_mesh.ply(filepath=file)
imported_obj = get_obj_from_name(obj_name)
imported_obj.select_set(True)
bpy.context.view_layer.objects.active = imported_obj

# get dim of object and set ratio1
bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center='BOUNDS')
x, y, z = imported_obj.dimensions
scale_ratio = max(x, y) / desired_dim
imported_obj.scale[0] = 1.0 / scale_ratio
imported_obj.scale[1] = 1.0 / scale_ratio
imported_obj.dimensions[2] = 0.2
bpy.ops.object.transform_apply(location=True, scale=True)

#center = 0.125 * sum((Vector(b) for b in imported_obj.bound_box), Vector())
#gc = imported_obj.matrix_world @ center
#imported_obj.location -= gc
imported_obj.location = (desired_x, desired_y, 0)
bpy.ops.object.transform_apply(location=True, scale=True)

"""
# scale it to fit in dimensions
for i in range(0, 3):
    imported_obj.scale[i] = 1.0 / scale_ratio

# move it back to the center
# idk why but it needs to do this several times
for j in range(0, 4):
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
    imported_obj.location[0] = desired_x
    imported_obj.location[1] = desired_y
    imported_obj.location[2] = 0
"""

# set back to default
bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN")

ca = get_obj_from_name("Camera")
ca.select_set(True)
bpy.context.view_layer.objects.active = ca
ca.location[0] = 7.05
ca.location[1] = -7.05
ca.location[2] = 5
bpy.ops.object.transform_apply(location=True, scale=True)

# fetch my gradient material
gradient = bpy.data.materials['gradient']

# assign to imported tile
if len(imported_obj.material_slots) < 1:
    imported_obj.data.materials.append(gradient)
else:
    imported_obj.material_slots[0].material = gradient