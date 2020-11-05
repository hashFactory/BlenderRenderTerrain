import bpy

# get prefs
prefs = bpy.context.preferences.addons['cycles'].preferences

# set CUDA
if use_CUDA:
    prefs.get_devices()
    
    prefs.compute_device_type = 'CUDA'
    prefs.devices[0].use = True
    
    # make sure we got CUDA device
    print(prefs.devices[0])

bpy.ops.wm.save_userpref()