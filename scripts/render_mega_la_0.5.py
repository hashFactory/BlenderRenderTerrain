import bpy

# get prefs
prefs = bpy.context.preferences.addons['cycles'].preferences

use_CUDA = True

# set CUDA
if use_CUDA:
    prefs.get_devices()
    
    prefs.compute_device_type = 'CUDA'
    prefs.devices[0].use = True
    
    # make sure we got CUDA device
    print(prefs.devices[0])
    
# set output resolution
for scene in bpy.data.scenes:
    scene.render.resolution_x = 3840*2
    scene.render.resolution_y = 2160*2

bpy.context.scene.cycles.use_denoising = False

bpy.context.scene.frame_end = 360
bpy.context.scene.render.frame_map_new = 50

bpy.ops.wm.save_userpref()

obj = bpy.data.objects["mega_la_0.5"]
obj.select_set(True)
bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center='BOUNDS')
obj.dimensions = (6.3, 6.3, 0.2)
obj.location
bpy.ops.transform.resize(value=(6.3, 6.3, 1))
bpy.ops.transform.resize(value=(1/6.3, 1/6.3, 1))
bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center='BOUNDS')
obj.location = (-1, 1, 0)