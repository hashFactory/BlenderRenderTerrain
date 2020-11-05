import bpy
import sys, os
from mathutils import *

def get_obj_from_name(desired_name):
    all_objects = bpy.context.selectable_objects
    for o in all_objects:
        if desired_name in o.name:
            return o

# setup variables
obj_name = "prov"
file = "/Users/tristan/Downloads/prov.ply"

# setting
desired_dim = 6.3 #(meters)
desired_height = 0.2
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
scale_z = z / desired_height
print("scale_ratio: " + str(scale_ratio) + ", scale_z: " + str(scale_z))

bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center='BOUNDS')
bpy.ops.transform.resize(value=(1.0 / scale_ratio, 1.0 / scale_ratio, 1.0 / scale_z))

for i in range(0, 2):
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center='BOUNDS')

    center = 0.125 * sum((Vector(b) for b in imported_obj.bound_box), Vector())
    gc = imported_obj.matrix_world @ center
    print(str(gc))

    bpy.ops.transform.translate(value=-gc)
    center = 0.125 * sum((Vector(b) for b in imported_obj.bound_box), Vector())
    gc = imported_obj.matrix_world @ center
    print(str(gc))
    bpy.ops.transform.translate(value=-gc)

# set back to default
bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN")

ca = get_obj_from_name("Camera")
ca.select_set(True)
bpy.context.view_layer.objects.active = ca
ca.location[0] = 7.05
ca.location[1] = -7.05
ca.location[2] = 5
bpy.ops.object.transform_apply(location=True, scale=True)

#__import__('code').interact(local=dict(globals(), **locals()))

bpy.context.view_layer.update()

dg = bpy.context.evaluated_depsgraph_get()
dg.update()

# fetch my gradient material
gradient = bpy.data.materials['gradient']

# assign to imported tile
if len(imported_obj.material_slots) < 1:
    imported_obj.data.materials.append(gradient)
else:
    imported_obj.material_slots[0].material = gradient


