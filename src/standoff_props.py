from bpy.props import (
    FloatProperty,
    IntProperty,
    CollectionProperty,
    PointerProperty
    )
from bpy.types import PropertyGroup, Scene
from bpy.utils import register_class, unregister_class

def CollectionUpdate(self, context):
    self.update(context)

class PG_StandoffBase(PropertyGroup):
    metric_diameter: FloatProperty(
        name="Inner Diameter (Metric)",
        default=2.5,
        min=2,
        max=5,
        step=50,
        precision=1)
    height: FloatProperty(
        name="Standoff Height",
        default=3,
        min=2,
        max=6,
        step=25,
        precision=2)

class PG_MountPoint(PropertyGroup):
    standoff: PointerProperty(type=PG_StandoffBase)
    x_position: FloatProperty(name="x position", default=0)
    y_position: FloatProperty(name="y position", default=0)

class PG_MountPointCollection(PropertyGroup):
    count: IntProperty(
        name="Number of Mounts",
        #default=2,
        min=2,
        max=6,
        update=CollectionUpdate
    )
    items: CollectionProperty(type=PG_MountPoint, name="Positions")

    def update(self, context):
        current_length = len(self.items)
        if current_length > self.count:
            while not current_length < self.count:
                self.items.remove(current_length)
                current_length -= 1
            return {"FINISHED"}
        if current_length < self.count:
            while current_length != self.count:
                mount_point = self.items.add()
                mount_point.name = f"MountPoint_{current_length+1}"
                current_length += 1
            return {"FINISHED"}

def register():
    register_class(PG_StandoffBase)
    register_class(PG_MountPoint)
    register_class(PG_MountPointCollection)
    Scene.Standoff = PointerProperty(type=PG_StandoffBase)
    Scene.MountPoint = PointerProperty(type=PG_MountPoint)
    Scene.MountPoints = PointerProperty(type=PG_MountPointCollection)

def unregister():
    unregister_class(PG_StandoffBase)
    unregister_class(PG_MountPoint)
    unregister_class(PG_MountPointCollection)
    del Scene.Standoff
    del Scene.MountPoint
    del Scene.MountPoints
