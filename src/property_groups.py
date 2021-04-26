from bpy.props import (
    FloatProperty,
    IntProperty,
    CollectionProperty,
    PointerProperty
    )
from bpy.types import PropertyGroup, Scene
from bpy.utils import register_class, unregister_class

def get_diameter(self):
    return self.get_diameter()

def set_diameter(self, value):
    self.set_diameter(value)

def get_height(self):
    return self.get_height()

def set_height(self, value):
    self.set_height(value)

def get_count(self):
    return self.get_count()

def set_count(self, value):
    self.set_count(value)

def PropertyUpdate(self, context):
    self.update(context)

class PG_StandoffBase(PropertyGroup):
    metric_diameter: FloatProperty(
        name="Inner Diameter (Metric)",
        default=2.5,
        min=2,
        max=5,
        step=50,
        precision=1,
        set=set_diameter,
        get=get_diameter
        )
    height: FloatProperty(
        name="Standoff Height",
        default=3,
        min=2,
        max=6,
        step=25,
        precision=2,
        set=set_height,
        get=get_height,
        )

    def get_diameter(self):
        try:
            diameter = self["metric_diameter"]
        except:
            self.set_diameter(2.5)
            diameter = self["metric_diameter"]
        finally:
            return diameter

    def set_diameter(self, value):
        self["metric_diameter"] = value

    def get_height(self):
        try:
            height = self["height"]
        except:
            self.set_height(3)
            height = self["height"]
        finally:
            return height

    def set_height(self, value):
        self["height"] = value

class PG_MountPoint(PropertyGroup):
    standoff: PointerProperty(type=PG_StandoffBase)
    x_position: FloatProperty(name="x position", default=0)
    y_position: FloatProperty(name="y position", default=0)

class PG_MountPointCollection(PropertyGroup):
    count: IntProperty(
        name="Number of Mounts",
        min=2,
        max=6,
        set=set_count,
        get=get_count,
        update=PropertyUpdate
    )
    items: CollectionProperty(type=PG_MountPoint, name="Positions")

    def get_count(self):
        try:
            count = self["count"]
        except:
            default = 2
            self.set_count(default)
            for i in range(default):
                self.add_mount_point(i)
            count = self["count"]
        finally:
            return count

    def set_count(self, value):
        self["count"] = value

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

    def add_mount_point(self, counter):
        mount_point = self.items.add()
        mount_point.name = f"Mount Position {counter+1}"

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
