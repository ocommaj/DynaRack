#import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import Operator

class DYNARACK_OT_add_mount_points(Operator):
    """adds collection of MountPoints"""
    bl_idname = 'object.add_mount_points'
    bl_label = 'Add Mount Points'
    bl_options = { "REGISTER", "UNDO" }
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DynaRack"

    def execute(self, context):

        return { "FINISHED" }

def register() :
    register_class(DYNARACK_OT_add_mount_points)

def unregister() :
    unregister_class(DYNARACK_OT_add_mount_points)
