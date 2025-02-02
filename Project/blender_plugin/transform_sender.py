bl_info = {
    "name": "Transform Sender",
    "blender": (3, 0, 0),  # Minimum Blender version required
    "category": "Object",
    "version": (1, 0),
    "author": "Your Name",
    "description": "Sends object transform data to a Flask server.",
    "location": "View3D > Sidebar > Transform Tab",
    "warning": "",  # Optional: Add warnings if needed
    "doc_url": "",  # Optional: Add documentation URL
    "tracker_url": "",  # Optional: Add issue tracker URL
}

import bpy
import requests
import json

class TransformPanel(bpy.types.Panel):
    bl_label = "Transform Sender"
    bl_idname = "VIEW3D_PT_transform_sender"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Transform'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Dropdown to select the endpoint
        layout.prop(scene, "transform_endpoint")

        # Submit button
        layout.operator("object.submit_transform")

class SubmitTransformOperator(bpy.types.Operator):
    bl_idname = "object.submit_transform"
    bl_label = "Submit Transform"

    def execute(self, context):
        obj = context.object
        if obj is None:
            self.report({'ERROR'}, "No object selected!")
            return {'CANCELLED'}

        # Get the selected endpoint
        endpoint = context.scene.transform_endpoint

        # Prepare transform data based on the selected endpoint
        if endpoint == 'transform':
            transform_data = {
                "name": obj.name,
                "position": list(obj.location),
                "rotation": list(obj.rotation_euler),
                "scale": list(obj.scale)
            }
        elif endpoint == 'translation':
            transform_data = {
                "position": list(obj.location)
            }
        elif endpoint == 'rotation':
            transform_data = {
                "rotation": list(obj.rotation_euler)
            }
        elif endpoint == 'scale':
            transform_data = {
                "scale": list(obj.scale)
            }
        else:
            self.report({'ERROR'}, "Invalid endpoint selected!")
            return {'CANCELLED'}

        # Send the data to the server
        try:
            response = requests.post(
                f"http://127.0.0.1:5000/{endpoint}",
                data=json.dumps(transform_data),
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                self.report({'INFO'}, f"Transform data submitted to /{endpoint}!")
            else:
                self.report({'ERROR'}, f"Server error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            self.report({'ERROR'}, f"Failed to connect: {e}")

        return {'FINISHED'}

# Add a property to store the selected endpoint
bpy.types.Scene.transform_endpoint = bpy.props.EnumProperty(
    name="Endpoint",
    description="Select the endpoint to send transform data",
    items=[
        ('transform', 'Transform', 'Send position, rotation, and scale'),
        ('translation', 'Translation', 'Send only position'),
        ('rotation', 'Rotation', 'Send only rotation'),
        ('scale', 'Scale', 'Send only scale'),
    ],
    default='transform'
)

def register():
    bpy.utils.register_class(TransformPanel)
    bpy.utils.register_class(SubmitTransformOperator)

def unregister():
    bpy.utils.unregister_class(TransformPanel)
    bpy.utils.unregister_class(SubmitTransformOperator)

if __name__ == "__main__":
    register()