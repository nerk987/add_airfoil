bl_info = {
    "name": "Add Airfoil",
    "author": "JIan Huish",
    "version": (1, 1, 0),
    "blender": (3, 00, 0),
    "location": "Add Mesh > Add Airfoil",
    "description": "Read Dat file and create airfoil mesh",
    "warning": "",
    "wiki_url": "https://github.com/nerk987/add_airfoil",
    "tracker_url": "http://github.com/nerk987/add_airfoil/issues",
    "category": "Add Mesh",
}
# Revised to name the mesh with the text from the first line
import bpy
import bmesh
from bpy_extras.object_utils import AddObjectHelper
from bpy_extras.io_utils import ImportHelper

from bpy.props import (
    FloatProperty,
)


def add_airfoil(filename):
    """
    This function takes inputs and returns vertex and face arrays.
    no actual mesh data creation is done here.
    """
    verts = []
    AirfoilName = ""
    datFile = open(filename, 'r')
    FirstLine = True
    for line in datFile:
        if FirstLine:
            AirfoilName = line[:-1]
        FirstLine = False
        line = line.replace(","," ")
        line = line.replace(";"," ")
        print(line)
        try:
            verts.append([0.0, float(line.split()[0]), float(line.split()[1])]) 
        except Exception:
            pass
    # print("Verts: ", verts)
    datFile.close()

    return verts, AirfoilName


class AddAirfoil(bpy.types.Operator, AddObjectHelper, ImportHelper):
    """Add an airfoil"""
    bl_idname = "mesh.airfoil_add"
    bl_label = "Add Airfoil"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
         # ImportHelper mixin class uses this
        filename_ext = ".txt"

        filter_glob: StringProperty(
            default="*.txt",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
        )


        verts_loc, AirfoilName = add_airfoil(self.filepath)
        
        if AirfoilName == "" or not AirfoilName.isalpha:
            AirfoilName = "Airfoil"

        mesh = bpy.data.meshes.new(AirfoilName)

        bm = bmesh.new()

        for v_co in verts_loc:
            bm.verts.new(v_co)

        bm.verts.ensure_lookup_table()
        for i in range(len(verts_loc)-1):
            bm.edges.new([bm.verts[i], bm.verts[i+1]])
        bm.edges.new([bm.verts[0], bm.verts[-1]])
        

        bm.to_mesh(mesh)
        mesh.update()

        # add the mesh as an object into the scene with this utility module
        from bpy_extras import object_utils
        object_utils.object_data_add(context, mesh, operator=self)

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddAirfoil.bl_idname, icon='MESH_CUBE')

# Register and add to the "add mesh" menu (required to use F3 search "Add Box" for quick access)
def register():
    bpy.utils.register_class(AddAirfoil)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddAirfoil)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.mesh.airfoil_add()
