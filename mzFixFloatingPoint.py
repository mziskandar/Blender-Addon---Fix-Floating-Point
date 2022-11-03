bl_info = {
    "name": "Fix Floating Point",
    "author": "MZIskandar",
    "location": "View3D > Sidebar > MISC",
    "version": (1, 0, 0),
    "blender": (3, 2, 0),
    "description": "Fixing Floating Point eg: leading 1.0003 to becomes 1.0.",
    "category": "3D View"
}

import bpy
from bpy import context

class ObjectFixFloatingPointOperator(bpy.types.Operator):    
    
    bl_idname = 'opr.object_fixfloatingpoint_operator'
    bl_label = 'Fix Floating Point'
    
    def execute(self, context):
       
        def fixFloat(f):
            result = f
            if result != 0:
                s = format(1%f,'.6f')
                if s[0] == '-':
                    sPlace = 1
                else:
                    sPlace = 0
                if s[sPlace+4] == '0':
                    if s[sPlace+5] == '0':
                        result = round(f, 3)
                elif s[sPlace+4] == '9':
                    if s[sPlace+5] == '9':
                        result = round(f, 3)    
            return result
        
        selectedObjects = bpy.context.selected_objects
        selectedObjectsMesh = []
        bpy.ops.object.mode_set(mode='OBJECT')
        for obj in selectedObjects:
            if obj.type == 'MESH':
                selectedObjectsMesh.append(obj)                
                mesh = obj.data
                for i in mesh.vertices:
                    i.co = [fixFloat(i.co[0]),fixFloat(i.co[1]),fixFloat(i.co[2])]
                    
        return {'FINISHED'}

class ObjectFixFloatingPointPanel(bpy.types.Panel):
    
    bl_idname = 'VIEW3D_PT_object_fixFP'
    bl_label = 'Fix Floating Point'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    
    def draw(self, context):
        
        layout = self.layout
        row = layout.row()
        selectedObjects = bpy.context.selected_objects
        row.label(text='Selected Object', icon='OBJECT_DATA')
        row = layout.row()
        selectedObjectsMesh = []
        for obj in selectedObjects:
            if obj.type == 'MESH':
                selectedObjectsMesh.append(obj)
                row.label(text=obj.name, icon='BLANK1')
                row = layout.row()
        if len(selectedObjectsMesh) == 0:
            row.enabled = False
        else: 
            row.enabled = True
        row.operator('opr.object_fixfloatingpoint_operator', text='Fix Floating Point')

def register():
    bpy.utils.register_class(ObjectFixFloatingPointPanel)
    bpy.utils.register_class(ObjectFixFloatingPointOperator)

def unregister():
    bpy.utils.unregister_class(ObjectFixFloatingPointPanel)
    bpy.utils.unregister_class(ObjectFixFloatingPointOperator)

if __name__ == '__main__':
    register()