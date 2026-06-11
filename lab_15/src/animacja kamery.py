import bpy
import math

def animate_pedestrian_head_bob(start_x, start_y, start_z, target_y, duration_seconds=20, fps=24, bob_freq=4.0, bob_amp_z=0.04, bob_amp_x=0.02):

    duration_frames = duration_seconds * fps

    scene = bpy.context.scene
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = duration_frames

    bpy.ops.object.select_all(action='DESELECT')
    
    bpy.ops.object.camera_add(
        location=(start_x, start_y, start_z), 
        rotation=(1.507, 0, 0)
    )
    camera = bpy.context.active_object
    camera.name = "Widok_Postaci_Chwianie"
    scene.camera = camera

    for frame in range(1, duration_frames + 1):
        progress = (frame - 1) / (duration_frames - 1)
        current_y = start_y + (target_y - start_y) * progress
        time_factor = progress * (duration_seconds * bob_freq) * math.pi
        offset_z = math.sin(time_factor) * bob_amp_z
        offset_x = math.cos(time_factor * 0.5) * bob_amp_x
        camera.location.x = start_x + offset_x
        camera.location.y = current_y
        camera.location.z = start_z + offset_z
        camera.keyframe_insert(data_path="location", frame=frame)

    if camera.animation_data and camera.animation_data.action:
        action = camera.animation_data.action
        
        if hasattr(action, "main_bindings") and action.main_bindings:
            for binding in action.main_bindings:
                if hasattr(binding, "fcurves"):
                    for fcurve in binding.fcurves:
                        for kp in fcurve.keyframe_points:
                            kp.interpolation = 'LINEAR'

        elif hasattr(action, "fcurves"):
            for fcurve in action.fcurves:
                for kp in fcurve.keyframe_points:
                    kp.interpolation = 'LINEAR'
                
    print(f"Pomyślnie wygenerowano animację spaceru z efektem head-bobbing.")

if __name__ == "__main__":
    PARAM_START_X = -5.5
    PARAM_START_Y = -100.0
    PARAM_START_Z = 1.75
    PARAM_TARGET_Y = 30.0
    PARAM_SECONDS = 20
    PARAM_FPS = 24
    PARAM_BOB_FREQ = 4.5
    PARAM_BOB_AMP_Z = 0.035
    PARAM_BOB_AMP_X = 0.020
    
    animate_pedestrian_head_bob(
        start_x=PARAM_START_X,
        start_y=PARAM_START_Y,
        start_z=PARAM_START_Z,
        target_y=PARAM_TARGET_Y,
        duration_seconds=PARAM_SECONDS,
        fps=PARAM_FPS,
        bob_freq=PARAM_BOB_FREQ,
        bob_amp_z=PARAM_BOB_AMP_Z,
        bob_amp_x=PARAM_BOB_AMP_X
    )