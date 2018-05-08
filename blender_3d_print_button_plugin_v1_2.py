bl_info = {
    "name": "3D Print Button Blender plugin",
    "version": (1, 2),
    "blender": (2, 70, 0),
    "location": "Info > File > Export",
    "description": "3D Print Button",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export"}

import bpy
import webbrowser
import requests
import os
import sys


#Panel
class PrintButtonPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Tools"
    bl_label = "3D Print Button"

    def draw(self, context):
        # Button
        self.layout.operator("object.export_stl", text="3D Print Button")
        
class ExportToStl(bpy.types.Operator):
    bl_idname = "object.export_stl"
    bl_label = "Send to 3D-button.com"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if(bpy.context.mode == 'OBJECT'):

            # Deselect Lamp and Camera, etc
            for obj in bpy.context.selected_objects:
                if obj.type == 'LAMP':
                    obj.select = False
                elif obj.type == 'CAMERA':
                    obj.select = False
                elif obj.type == 'SPEAKER':
                    obj.select = False
                elif obj.type == 'EMPTY':
                    obj.select == False
                elif obj.type == 'LATTICE':
                    obj.select == False
                elif obj.type == 'ARMATURE':
                    obj.select == False
                    
               # elif obj.type == 'MESH':
                
            # Selected Objects
            if(len(bpy.context.selected_objects)>0):
                    
                
                # Save as .stl file. Because the blender method export_mesh.stl needs a new file, 
                # a temporary file is created in the (roaming) blender directory
                # .stl file is in ascii, due to request problems
                path = os.path.dirname(os.path.abspath(__file__)) + "/temp_stl_model.stl"
                
                bpy.ops.export_mesh.stl(filepath=path, ascii=True) 
                
                file = open(path)
                
                if bpy.data.is_saved == False:
                    filename='unsaved_file'
                else:
                    # get filename
                    somename = bpy.path.basename(bpy.context.blend_data.filepath)
                    filename=somename[:-6]
                
                #HTTP POST request, using the python REQUEST lib
                url = 'https://api.3d-button.com/upload'
                
                files = {'file':(filename + ".stl", file,'application/sla')}
                fields = { "origin":"blender_1_1"}
                custom_header = {
                    "Accept":"text/plain"
                    }
                try:
                    r = requests.post(url, files=files, data=fields,headers=custom_header,verify=False)
                    # Open the returned URL
                    if sys.platform[:3]== 'win':
                        webbrowser.get('windows-default').open(r.text) 
                   # for browser in (    
                    #                    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s',
                    #                    'C:/Program Files (x86)/Mozilla Firefox/firefox.exe %s',
                    #                    'C:/Program Files/Internet Explorer/iexplore.exe %s'):
                    #    try:
                    #        b=webbrowser.get(browser)
                    #        b.open(r.text)
                    #        break
                    #    except:
                    #        pass
             
                    else:
                        webbrowser.open(r.text)
                    # Show the url
                    self.report({'INFO'},r.text)
                
                    # Deselect
                    bpy.ops.object.select_all(action='DESELECT')
                        
                    
                except:
                    #Error Message in info console
                    self.report({'INFO'},'Could not connect to server. Please check your internet connection.')
                # Remove temp file
                file.close()
                
                os.remove(path)
                      
                return {'FINISHED'}
                
            else:
                #Error Message in info console
                self.report({'INFO'},'Select an object')
                return {'FINISHED'}
                
        else:
            #Error Message in info console
            self.report({'INFO'},'Change Mode to OBJECT MODE')
            return {'FINISHED'}
            
def menu_func(self, context):
    self.layout.operator(ExportToStl.bl_idname)

def register():
    bpy.utils.register_class(ExportToStl)
    bpy.utils.register_class(PrintButtonPanel)
    bpy.types.INFO_MT_file_export.append(menu_func)
    
    
def unregister():
    bpy.utils.unregister_class(ExportToStl)
    bpy.utils.unregister_class(PrintButtonPanel)
    bpy.types.INFO_MT_file_export.remove(menu_func)
  
    
if __name__ == "__main__":
    register()
