# blender -b -P enableaddon.py
import bpy

# bpy.ops.preferences.addon_install(filepath='/home/shane/Downloads/testaddon.py')

# find . | grep -i addon | grep -i free
bpy.ops.preferences.addon_enable(module='render_freestyle_svg')
bpy.ops.wm.save_userpref()

# http://blog.floriancargoet.com/slow-down-or-speed-up-a-gif-with-imagemagick/