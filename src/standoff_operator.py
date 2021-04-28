import bpy
from .standoff_mesh import Standoff

class DYNARACK_OT_test_standoff_add(bpy.types.Operator):
    """adds standoff to test add-on registered ok"""
    bl_idname = 'scene.add_test_standoff'
    bl_label = 'Add Test Standoff'
    bl_options = { "REGISTER", "UNDO" }

    def execute(self, context):
        name = "Standoff"
        props = context.scene.Standoff
        collection = context.scene.collection
        standoff = Standoff(name, props.metric_diameter, props.height)
        obj = bpy.data.objects.new(standoff.name, standoff.mesh)

        collection.objects.link(obj)
        obj.select_set(True)
        context.view_layer.objects.active = obj

        return {"FINISHED"}

def register() :
    bpy.utils.register_class(DYNARACK_OT_test_standoff_add)

def unregister() :
    bpy.utils.unregister_class(DYNARACK_OT_test_standoff_add)
