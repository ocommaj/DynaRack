from bpy.utils import register_class, unregister_class
from bpy.types import Operator

class DYNARACK_OT_add_mount_points(Operator):
    """adds collection of MountPoints"""
    bl_idname = 'scene.add_mount_points'
    bl_label = 'Add Mount Points'
    bl_options = { "REGISTER", "UNDO" }
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DynaRack"

    def execute(self, context):
        mountpoints_props = context.scene.MountPoints
        standoff_props = context.scene.Standoff
        for i,obj in enumerate(mountpoints_props.items):
            obj.standoff.metric_diameter = standoff_props.metric_diameter
            obj.standoff.height = standoff_props.height
            print(f"mountpoint {i+1} x pos: {obj.x_position}")
            print(f"mountpoint standoff diam: {obj.standoff.metric_diameter}")
            print(f"mountpoint standoff height: {obj.standoff.height}")
        return { "FINISHED" }

def register() :
    register_class(DYNARACK_OT_add_mount_points)

def unregister() :
    unregister_class(DYNARACK_OT_add_mount_points)
