import bpy
from bpy.utils import register_class, unregister_class

class MountPointsPanel(bpy.types.Panel):
    bl_idname = "DYNARACK_PT_board_panel"
    bl_label = "Standoff Collection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DynaRack"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        collection_data = bpy.data.objects[0].MountPoints

        layout.operator("object.add_mount_points", icon="MESH_CUBE")
        layout.prop(collection_data, "count")

        if collection_data.count:
            box = layout.box()
            for i,item in enumerate(collection_data.items):
                label = box.label(text=f"Mount Position {i+1}")
                row = box.row()

                row.prop(item, "x_position", text="X:")
                row.prop(item, "y_position", text="Y:")

class TestStandoffPanel(bpy.types.Panel):
    bl_idname = "DYNARACK_PT_standoff_panel"
    bl_label = "Test Standoff"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DynaRack"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        standoff_data = bpy.data.objects[0].Standoff

        layout.operator("object.add_test_standoff", icon='MESH_CUBE', text="Add Test Standoff")

        column = layout.column()
        column.prop(standoff_data, 'metric_diameter')
        column.prop(standoff_data, 'height')

def register():
    register_class(MountPointsPanel)
    register_class(TestStandoffPanel)

def unregister():
    unregister_class(MountPointsPanel)
    unregister_class(TestStandoffPanel)
