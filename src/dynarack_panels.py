from bpy.utils import register_class, unregister_class
from bpy.types import Panel

class ComponentsPanel(Panel):
    bl_idname = "DYNARACK_PT_components_panel"
    bl_label = "Component"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DynaRack"

    def draw(self, context):
        layout = self.layout
        enum_data = context.scene.HardwareMounts

        layout.prop_menu_enum(enum_data, "components")

class MountPointsPanel(Panel):
    bl_idname = "DYNARACK_PT_board_panel"
    bl_label = "Standoff Collection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DynaRack"

    def draw(self, context):
        layout = self.layout
        collection_data = context.scene.MountPoints

        layout.operator("scene.add_mount_points", icon="MESH_CUBE")
        layout.prop(collection_data, "count")

        box = layout.box()
        for i,item in enumerate(collection_data.items):
            label = box.label(text=item.name)
            row = box.row()
            row.prop(item, "x_position", text="X:")
            row.prop(item, "y_position", text="Y:")

class TestStandoffPanel(Panel):
    bl_idname = "DYNARACK_PT_standoff_panel"
    bl_label = "Test Standoff"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DynaRack"

    def draw(self, context):
        layout = self.layout
        standoff_data = context.scene.Standoff

        layout.operator(
            "scene.add_test_standoff",
            icon='MESH_CUBE',
            text="Add Test Standoff"
            )

        column = layout.column()
        column.prop(standoff_data, 'metric_diameter')
        column.prop(standoff_data, 'height')

def register():
    register_class(ComponentsPanel)
    register_class(MountPointsPanel)
    register_class(TestStandoffPanel)

def unregister():
    unregister_class(ComponentsPanel)
    unregister_class(MountPointsPanel)
    unregister_class(TestStandoffPanel)
