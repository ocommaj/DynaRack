from bpy.types import Panel
from bpy.utils import register_class, unregister_class

class DynaRackPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DynaRack"
    bl_options = { 'DEFAULT_CLOSED' }

class HardwareMountsPanel(DynaRackPanel, Panel):
    bl_idname = "DYNARACK_PT_hardware_mounts_panel"
    bl_label = "Hardware Mount Points"

    def draw(self, context):
        layout = self.layout
        hw_data = context.scene.HardwareMounts

        layout.operator("scene.add_mount_points", icon="COLLECTION_NEW")
        layout.prop_menu_enum(hw_data, "components", text=hw_data.display_text)

class MountPointsPanel(DynaRackPanel, Panel):
    bl_idname = "DYNARACK_PT_mount_points_panel"
    bl_label = "Mount Points"
    bl_parent_id = "DYNARACK_PT_hardware_mounts_panel"

    def draw(self, context):
        layout = self.layout
        mp_data = context.scene.MountPoints

        layout.prop(mp_data, "count")
        box = layout.box()
        for i,item in enumerate(mp_data.items):
            label = box.label(text=item.name)
            row = box.row()
            row.prop(item, "x_position", text="X:")
            row.prop(item, "y_position", text="Y:")

class TestStandoffPanel(DynaRackPanel, Panel):
    bl_idname = "DYNARACK_PT_standoff_panel"
    bl_label = "Standoff Properties"

    def draw(self, context):
        layout = self.layout
        standoff_data = context.scene.Standoff

        layout.operator(
            "scene.add_test_standoff",
            icon='MESH_CUBE',
            text="Add a Test Standoff"
            )

        column = layout.column()
        column.prop(standoff_data, 'metric_diameter')
        column.prop(standoff_data, 'height')

def register():
    register_class(HardwareMountsPanel)
    register_class(MountPointsPanel)
    register_class(TestStandoffPanel)

def unregister():
    unregister_class(HardwareMountsPanel)
    unregister_class(MountPointsPanel)
    unregister_class(TestStandoffPanel)
