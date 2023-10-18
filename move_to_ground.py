######################################################################
#  An operator to align an object to the ground z=0 plane.
#
#  Prefered keyboard binding: Shift Down Arrow
#
#  2023-10-18 Wed
#  Dov Grobgeld <dov.grobgeld@gmail.com>
######################################################################
import bpy
from mathutils import Vector
from bpy.types import Object
import numpy as np

bl_info = {
    "name": "Move Object to Ground",
    "blender": (2, 80, 0),
    "category": "Object",
}

# From: https://blender.stackexchange.com/questions/264568/what-is-the-fastest-way-to-set-global-vertices-coordinates-to-a-numpy-array-usin
def vertices_global_co(obj: Object) -> np.ndarray:
    """Return numpy array with object vertices global coordinates"""
    
    rotation_and_scale = obj.matrix_world.to_3x3().transposed() 
    offset = obj.matrix_world.translation 
    vertices_blender = obj.data.vertices 
    vlen = len(vertices_blender)  
    
    vertices_local = np.empty([vlen*3], dtype='f') 
    vertices_blender.foreach_get("co", vertices_local)
    vertices_local = vertices_local.reshape(vlen, 3)  
    vertices_global = np.matmul(vertices_local, rotation_and_scale) + offset
    
    return vertices_global

def main(context):
    for obj in bpy.context.selected_objects:
        vertices_world = vertices_global_co(obj)
        minz = vertices_world[:,2].min()

        # Translate the object by -minz
        obj.location = obj.location + Vector((0,0,-minz))

class MoveToGroundOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.move_to_ground"
    bl_label = "Move object to ground"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(MoveToGroundOperator.bl_idname, text=MoveToGroundOperator.bl_label)


# Register and add to the "object" menu (required to also use F3 search "MoveToGround" for quick access).
def register():
    bpy.utils.register_class(MoveToGroundOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(MoveToGroundOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

