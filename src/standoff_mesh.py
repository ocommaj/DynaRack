import bpy
import bmesh

class Standoff():
    def __init__(self, name="Std", metric_diameter=3, depth=3, segments=64):
        self.name = name
        self.depth = depth
        self.segments = segments
        self.radii = {
            "inner": metric_diameter/2,
            "outer": metric_diameter*1.25
            }

        self.mesh = bmesh_to_mesh( self._create_drum_bmesh(), "Standoff" )

    def _create_drum_bmesh(self):
        """
        returns new bmesh instance for current self geometry values
        'bm' variable name is BMesh convention following docs:
        https://docs.blender.org/api/current/bmesh.html
        """
        bm = bmesh.new()

        to_extrude = self._make_footprint(bm)
        extrude_faces(bm, to_extrude["faces"], self.depth)

        return bm

    def _make_footprint(self, bm):
        """
        takes bmesh instance,
        returns dict with keys 'faces', 'edges' from bmesh.ops.bridge_loops
        """
        def circumference(radius):
            """
            for radius, create circle in bm, return edges list
            """
            edges = []
            circ = bmesh.ops.create_circle(
                bm,
                radius=radius,
                segments=self.segments,
                cap_ends=False
                )
            [ edges.append(e) for v in circ["verts"]
              for e in v.link_edges
              if e not in edges ]
            return edges

        edges = [ e for r in self.radii.values() for e in circumference(r) ]
        bridged = bmesh.ops.bridge_loops(bm, edges=edges)
        return bridged

def extrude_faces(bm, faces, depth=1.0):
    extruded = bmesh.ops.extrude_face_region(bm, geom=faces)
    verts=[e for e in extruded["geom"] if isinstance(e, bmesh.types.BMVert)]
    del extruded

    bmesh.ops.translate(bm, verts=verts, vec=(0.0, 0.0, depth))

def clean_for_manifold(bm):
    """helper method to remove doubles; not needed with clean/simple extrude"""
    MERGE_DISTANCE = 0.0001
    verts = bm.verts
    bmesh.ops.remove_doubles(bm, verts=verts, dist=MERGE_DISTANCE)

def bmesh_to_mesh(bm, name=None, me=None):
    """
    optional 'me' arg accepts instance of bpy.types.Mesh or creates new
    'me' variable name is BMesh convention following docs example:
    https://docs.blender.org/api/current/bmesh.html
    """
    if not name: name = "Mesh"
    if not me: me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return me

def test(metric_diameter=2.5, depth=3, name="Standoff"):
    def add_mesh_to_collection(me, name, obj=None, collection=None):
        if not collection:
            collection = bpy.context.collection.objects
        if not obj:
            obj = bpy.data.objects.new(name, me)
        collection.link(obj)
        return obj

    std = Standoff(metric_diameter=metric_diameter, depth=depth, name=name)
    return add_mesh_to_collection(std.mesh, std.name)

if __name__ == "__main__":
    test()
