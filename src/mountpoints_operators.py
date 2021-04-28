import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import Operator
from .standoff_mesh import Standoff

class DYNARACK_OT_add_mount_points(Operator):
    """adds collection of MountPoints"""
    bl_idname = 'scene.add_mount_points'
    bl_label = 'Add Mount Points'
    bl_options = { "REGISTER", "UNDO" }
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DynaRack"

    def execute(self, context):
        scene = context.scene;
        collection = scene.collection;
        mp_collection = bpy.data.collections.new("Mount Points")

        mountpoints_props = scene.MountPoints
        standoff_props = scene.Standoff
        collection.children.link(mp_collection)

        for mp in mountpoints_props.items:
            mp.standoff.metric_diameter = standoff_props.metric_diameter
            mp.standoff.height = standoff_props.height

            mountpoint = Standoff(
                mp.name,
                mp.standoff.metric_diameter,
                mp.standoff.height)

            obj = bpy.data.objects.new(mountpoint.name, mountpoint.mesh)
            obj.location.x = mp.x_position
            obj.location.y = mp.y_position

            mp_collection.objects.link(obj)

        return { "FINISHED" }

def register() :
    register_class(DYNARACK_OT_add_mount_points)

def unregister() :
    unregister_class(DYNARACK_OT_add_mount_points)
