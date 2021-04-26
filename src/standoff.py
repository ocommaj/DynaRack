import bpy
import bmesh

class Standoff():
    def __init__(self, metric_diameter=3, depth=3, segments=64):
        self.depth = depth
        self.segments = segments
        self.radii = {
            "inner": metric_diameter/2,
            "outer": metric_diameter*1.25
            }

        self.drum = bmesh_to_mesh( self._create_drum_bmesh() )

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

def bmesh_to_mesh(bm, me=None):
    """
    optional 'me' arg accepts instance of bpy.types.Mesh or creates new
    'me' variable name is BMesh convention following docs example:
    https://docs.blender.org/api/current/bmesh.html
    """
    if not me:
        me = bpy.data.meshes.new("Mesh")
    bm.to_mesh(me)
    bm.free()
    return me

def add_mesh_to_collection(me, obj=None, collection=None):
    if not collection:
        collection = bpy.context.collection.objects
    if not obj:
        obj = bpy.data.objects.new("Object", me)
    collection.link(obj)
    return obj

def test(metric_diameter=2.5, depth=3):
    standoff = Standoff(metric_diameter, depth)
    return add_mesh_to_collection(standoff.drum)

if __name__ == "__main__":
    test()