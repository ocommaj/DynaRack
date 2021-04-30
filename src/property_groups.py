from bpy.props import (
    CollectionProperty,
    EnumProperty,
    FloatProperty,
    IntProperty,
    StringProperty,
    PointerProperty
    )
from bpy.types import PropertyGroup, Scene
from bpy.utils import register_class, unregister_class
from .hardware_component_data import component_data

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
    x_position: FloatProperty(
        name="x position",
        step=25,
        set=prop_methods("SET", "x_position"),
        get=prop_methods("GET", "x_position")
        )
    y_position: FloatProperty(
        name="y position",
        step=25,
        set=prop_methods("SET", "y_position"),
        get=prop_methods("GET", "y_position")
        )

    defaults={ "x_position": 0, "y_position": 0 }

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

    defaults = { "count": 2, "positions": [ [0, 5], [0, -5] ] }

    def on_load(self):
        count = self.defaults["count"]
        pos = self.defaults["positions"]
        for i in range(count):
            self.add_mount_point(i, pos[i])

    def add_mount_point(self, counter, pos=None):
        mount_point = self.items.add()
        mount_point.name = f"Mount Position {counter+1}"
        if pos:
            x = pos[0]
            y = pos[1]
            mount_point.x_position = x
            mount_point.y_position = y

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

class PG_HardwareMount(PropertyGroup):
    name: StringProperty(name="Hardware Component")
    mount_points: PointerProperty(type=PG_MountPointCollection)

class PG_HardwareMounts(PropertyGroup):
    def _load_components(self, context):
        test_items = [
            ("RED", "Red", "", 1),
            ("GREEN", "Green", "", 2),
            ("YELLOW", "Yellow", "", 3),
            ("RPiB", "Rasperry Pi B", "", 4),
            ("CUSTOM", "Custom", "", 5)
        ]

        return test_items
    components: EnumProperty(
        items=_load_components,
        name="Add Component",
        update=prop_methods("UPDATE"))

    def update(self, context):
        if self.components == "RPiB":
            mp_props = component_data["RPiB"]
            standoff_base = context.scene.Standoff
            mountpoints = context.scene.MountPoints

            standoff_base.metric_diameter = mp_props["diam"]
            mountpoints.items.clear()

            for i in range(mp_props["count"]):
                name = f"RPiB Mountpoint {i+1}"
                x = mp_props["pos"][i][0]
                y = mp_props["pos"][i][1]
                mp = mountpoints.items.add()
                mp.name = name
                mp.x_position = x
                mp.y_position = y
            mountpoints.count = mp_props["count"]


def register():
    register_class(PG_StandoffBase)
    register_class(PG_MountPoint)
    register_class(PG_MountPointCollection)
    register_class(PG_HardwareMount)
    register_class(PG_HardwareMounts)
    Scene.Standoff = PointerProperty(type=PG_StandoffBase)
    Scene.MountPoint = PointerProperty(type=PG_MountPoint)
    Scene.MountPoints = PointerProperty(type=PG_MountPointCollection)
    Scene.HardwareMount = PointerProperty(type=PG_HardwareMount)
    Scene.HardwareMounts = PointerProperty(type=PG_HardwareMounts)

def unregister():
    unregister_class(PG_StandoffBase)
    unregister_class(PG_MountPoint)
    unregister_class(PG_MountPointCollection)
    unregister_class(PG_HardwareMount)
    unregister_class(PG_HardwareMounts)
    del Scene.Standoff
    del Scene.MountPoint
    del Scene.MountPoints
    del Scene.HardwareMount
    del Scene.HardwareMounts
