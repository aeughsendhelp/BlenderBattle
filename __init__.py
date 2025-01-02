bl_info = {
    "name": "Blender Battle",
    "blender": (4, 2, 3),
    "category": "Object",
}

import bpy

gameTime = 60.0;

class BlenderBattlePanel(bpy.types.Panel):
    bl_label = "Blender Battle"  # Panel title
    bl_idname = "_PT_BlenderBattlePanel_PT_"  # Panel identifier
    bl_space_type = 'VIEW_3D'  # Which editor the panel appears in
    bl_region_type = 'UI'  # Which region the panel appears in (UI for tool shelf)
    bl_category = 'BB'  # The tab where the panel will be located

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Setup Menus
        layout.label(text="Click To Thing")
        layout.operator("object.join_game", text="Join Game")  

        # Timer
        layout.label(text="Time Left: {:.2f}".format(scene.timer_value))  # Display time left with two decimal places

        # Submit
        layout.label(text="Click To Submit Creation")
        layout.operator("object.submit", text="Submit")  

class JoinGame(bpy.types.Operator):
    bl_idname = "object.join_game"
    bl_label = "Join Game"

    def execute(self, context):
        context.scene.timer_value = 60.0
        self.report({'INFO'}, "Join Game Button Pressed")

        return {'FINISHED'}

class Submit(bpy.types.Operator):
    bl_idname = "object.submit"
    bl_label = "Submit"

    def execute(self, context):
        self.report({'INFO'}, "Submit Button Pressed")
        return {'FINISHED'}

# timer
def update_timer(scene):
    # Get the timer value from the scene
    print("Frame changed, updating timer...")

    timer = scene.timer_value

    # Decrease the timer by the time elapsed since the last frame (e.g., 1/60th of a second for a 60 FPS update rate)
    if timer > 0:
        scene.timer_value -= 1.0 / 60.0  # Decrease by one frame

    else:
        scene.timer_value = 0  # Stop at zero


def register():
    bpy.utils.register_class(BlenderBattlePanel)
    bpy.utils.register_class(JoinGame)
    bpy.utils.register_class(Submit)

    bpy.types.Scene.timer_value = bpy.props.FloatProperty(name="Timer", default=gameTime)  # Start timer with 60 seconds
    bpy.app.handlers.frame_change_post.append(update_timer)
def unregister():
    bpy.app.handlers.frame_change_post.remove(update_timer)  # Remove handler when unregistering

    bpy.utils.unregister_class(BlenderBattlePanel)
    bpy.utils.unregister_class(JoinGame)
    bpy.utils.unregister_class(Submit)

    del bpy.types.Scene.timer_value  # Clean up the property

# If running the script directly, register the addon
if __name__ == "__main__":
    register()
