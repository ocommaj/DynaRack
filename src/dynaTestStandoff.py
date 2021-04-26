import bpy
from .standoff import test

class DYNARACK_OT_test_standoff_add(bpy.types.Operator):
    """adds standoff to test add-on registered ok"""
    bl_idname = 'object.add_test_standoff'
    bl_label = 'Add Test Standoff'
    bl_options = { "REGISTER", "UNDO" }

    def execute(self, context):
        props = bpy.data.objects[0].Standoff
        obj = test(props.metric_diameter, props.height)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        return {"FINISHED"}

def register() :
    bpy.utils.register_class(DYNARACK_OT_test_standoff_add)

def unregister() :
    bpy.utils.unregister_class(DYNARACK_OT_test_standoff_add)
