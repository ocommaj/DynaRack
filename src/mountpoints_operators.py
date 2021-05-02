import bpy
from bpy.utils import register_class, unregister_class
from bpy.types import Operator

class DYNARACK_OT_add_mount_points(Operator):
    """adds collection of MountPoints"""
    bl_idname = "scene.add_mount_points"
    bl_label = "Add Mount Points"
    bl_options = { "REGISTER", "UNDO" }
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DynaRack"

    def execute(self, context):
        scene = context.scene
        collection = scene.collection

        mp_props = scene.MountPoints
        standoff = scene.Standoff

        mp_collection = bpy.data.collections.new(mp_props.collection_name)
        collection.children.link(mp_collection)

        for mp in mp_props.items:
            mp.standoff.metric_diameter = standoff.metric_diameter
            mp.standoff.height = standoff.height

            obj = bpy.data.objects.new(mp.name, mp.standoff.mesh)
            obj.location.x = mp.x_position
            obj.location.y = mp.y_position

            mp_collection.objects.link(obj)

        return { "FINISHED" }

def register() :
    register_class(DYNARACK_OT_add_mount_points)

def unregister() :
    unregister_class(DYNARACK_OT_add_mount_points)
