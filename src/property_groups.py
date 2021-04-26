from bpy.props import (
    FloatProperty,
    IntProperty,
    CollectionProperty,
    PointerProperty
    )
from bpy.types import PropertyGroup, Scene
from bpy.utils import register_class, unregister_class

def prop_methods(call, prop=None):
    if call == "UPDATE":
        def update(self, context):
            self.update(context)
        return update
    if call == "GET":
        def getter(self):
            try:
                value = self[prop]
            except:
                set_default = prop_methods("SET", prop)
                set_default(self, self.defaults[prop])
                if hasattr(self, "on_load"):
                    self.on_load()
                value = self[prop]
            finally:
                return value
        return getter
    if call == "SET":
        def setter(self, value):
            self[prop] = value
        return setter

class PG_StandoffBase(PropertyGroup):
    metric_diameter: FloatProperty(
        name="Inner Diameter (Metric)",
        default=2.5,
        min=2,
        max=5,
        step=50,
        precision=1,
        set=prop_methods("SET", "metric_diameter"),
        get=prop_methods("GET", "metric_diameter")
        )
    height: FloatProperty(
        name="Standoff Height",
        default=3,
        min=2,
        max=6,
        step=25,
        precision=2,
        set=prop_methods("SET", "height"),
        get=prop_methods("GET", "height"),
        )

    defaults = { "metric_diameter":  2.5, "height": 3 }

class PG_MountPoint(PropertyGroup):
    standoff: PointerProperty(type=PG_StandoffBase)
    x_position: FloatProperty(name="x position", default=0)
    y_position: FloatProperty(name="y position", default=0)

class PG_MountPointCollection(PropertyGroup):
    count: IntProperty(
        name="Number of Mounts",
        min=2,
        max=6,
        set=prop_methods("SET", "count"),
        get=prop_methods("GET", "count"),
        update=prop_methods("UPDATE")
        )

    items: CollectionProperty(type=PG_MountPoint, name="Positions")

    defaults = { "count": 2 }

    def on_load(self):
        count = self.defaults["count"]
        for i in range(count):
            self.add_mount_point(i)

    def add_mount_point(self, counter):
        mount_point = self.items.add()
        mount_point.name = f"Mount Position {counter+1}"

    def update(self, context):
        current_length = len(self.items)
        if current_length > self.count:
            while not current_length < self.count:
                self.items.remove(current_length)
                current_length -= 1
            return {"FINISHED"}
        if current_length < self.count:
            while current_length != self.count:
                self.add_mount_point(current_length)
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
