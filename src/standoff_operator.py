import bpy

class DYNARACK_OT_test_standoff_add(bpy.types.Operator):
    """adds standoff to test add-on registered ok"""
    bl_idname = 'scene.add_test_standoff'
    bl_label = 'Add Test Standoff'
    bl_options = { "REGISTER", "UNDO" }

    def execute(self, context):
        name = "Standoff"
        standoff = context.scene.Standoff
        collection = context.scene.collection
        obj = bpy.data.objects.new(name, standoff.mesh)

        collection.objects.link(obj)
        obj.select_set(True)
        context.view_layer.objects.active = obj

        return {"FINISHED"}

def register() :
    bpy.utils.register_class(DYNARACK_OT_test_standoff_add)

def unregister() :
    bpy.utils.unregister_class(DYNARACK_OT_test_standoff_add)
