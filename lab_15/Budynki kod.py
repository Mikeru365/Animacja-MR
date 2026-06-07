import bpy
import random
import math
from mathutils import Vector

def setup_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    if "Background" in bpy.data.worlds:
        bpy.data.worlds["Background"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

def create_emission_material(name, color, strength):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    for node in nodes:
        nodes.remove(node)
        
    node_output = nodes.new(type='ShaderNodeOutputMaterial')
    node_emission = nodes.new(type='ShaderNodeEmission')
    
    node_emission.inputs['Color'].default_value = color
    node_emission.inputs['Strength'].default_value = strength
    
    links.new(node_emission.outputs['Emission'], node_output.inputs['Surface'])
    return mat

def create_building(x_pos, y_pos, z_start, base_width, mat_dark, neon_mats, side_sign):
    floors = random.randint(5, 10)
    fixed_width = base_width
    fixed_depth = random.uniform(5.0, 7.0)
    
    current_z = z_start
    building_parts = []
    
    for i in range(floors):
        current_h = random.uniform(2.0, 3.5)
        
        x_offset = 0.0
        floor_width = fixed_width
        floor_depth = fixed_depth
        
        if random.random() < 0.35:
            extension = random.uniform(0.5, 1.2)
            floor_width += extension
            x_offset = (extension / 2) * side_sign
            
        if random.random() < 0.2:
            floor_depth += random.uniform(-0.4, 0.4)
            
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_pos + x_offset, y_pos, current_z + (current_h / 2)))
        cube = bpy.context.active_object
        cube.scale = (floor_width, floor_depth, current_h)
        bpy.ops.object.transform_apply(scale=True)
        
        if i == 0:
            cube.data.materials.append(mat_dark)
        else:
            if random.random() > 0.1:
                cube.data.materials.append(mat_dark)
            else:
                cube.data.materials.append(random.choice(neon_mats))
                
        building_parts.append(cube)
        current_z += current_h
        
    if building_parts:
        bpy.ops.object.select_all(action='DESELECT')
        for part in building_parts:
            part.select_set(True)
        bpy.context.view_layer.objects.active = building_parts[0]
        bpy.ops.object.join()
        
        final_building = bpy.context.view_layer.objects.active
        final_building.name = f"Budynek_{'L' if side_sign == -1 else 'P'}_{y_pos:.1f}"
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        bpy.ops.object.select_all(action='DESELECT')
        
    return current_z

def create_cable(p1, p2, mat_dark, cable_sag):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.curve.primitive_bezier_curve_add()
    cable = bpy.context.active_object
    
    curve_data = cable.data
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = 0.04
    curve_data.bevel_resolution = 4
    
    point_1 = curve_data.splines[0].bezier_points[0]
    point_2 = curve_data.splines[0].bezier_points[1]
    
    point_1.co = p1
    point_2.co = p2
    
    mid_point = (p1 + p2) / 2
    mid_point.z -= random.uniform(cable_sag * 0.7, cable_sag * 1.3)
    
    point_1.handle_right = mid_point
    point_2.handle_left = mid_point
    
    cable.data.materials.append(mat_dark)
    cable.name = "Kabel_Instalacja"
    bpy.ops.object.select_all(action='DESELECT')

def create_pipe(p1, p2, mat_dark, pipe_radius):
    bpy.ops.object.select_all(action='DESELECT')
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dz = p2.z - p1.z
    distance = math.sqrt(dx**2 + dy**2 + dz**2)
    
    if distance < 0.001:
        return
        
    bpy.ops.mesh.primitive_cylinder_add(radius=pipe_radius, depth=distance, location=((p1.x+p2.x)/2, (p1.y+p2.y)/2, (p1.z+p2.z)/2))
    pipe = bpy.context.active_object
    
    phi = math.atan2(dy, dx)
    theta = math.acos(dz / distance)
    
    pipe.rotation_euler = (0, theta, phi)
    pipe.data.materials.append(mat_dark)
    pipe.name = "Rura_Infrastruktura"
    bpy.ops.object.select_all(action='DESELECT')

def build_cyberpunk_street(config):
    street_width = config['street_width']
    street_length = config['street_length']
    sidewalk_width = config['sidewalk_width']
    sidewalk_height = config['sidewalk_height']
    
    mat_dark = create_emission_material("DarkGlow", (0.02, 0.02, 0.05, 1.0), 0.5)
    mat_cyan = create_emission_material("NeonCyan", (0.0, 0.8, 1.0, 1.0), 15.0)
    mat_pink = create_emission_material("NeonPink", (1.0, 0.0, 0.4, 1.0), 15.0)
    mat_yellow = create_emission_material("NeonYellow", (1.0, 0.7, 0.0, 1.0), 15.0)
    neon_mats = [mat_cyan, mat_pink, mat_yellow]
    
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, 0, 0))
    road = bpy.context.active_object
    road.scale = (street_width, street_length, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    road.data.materials.append(mat_dark)
    road.name = "Ulica_Podstawa"
    bpy.ops.object.select_all(action='DESELECT')
    
    x_sidewalk_left = -(street_width / 2) - (sidewalk_width / 2)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_sidewalk_left, 0, sidewalk_height / 2))
    sw_left = bpy.context.active_object
    sw_left.scale = (sidewalk_width, street_length, sidewalk_height)
    bpy.ops.object.transform_apply(scale=True)
    sw_left.data.materials.append(mat_dark)
    sw_left.name = "Chodnik_Lewy_Blok"
    
    x_sidewalk_right = (street_width / 2) + (sidewalk_width / 2)
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_sidewalk_right, 0, sidewalk_height / 2))
    sw_right = bpy.context.active_object
    sw_right.scale = (sidewalk_width, street_length, sidewalk_height)
    bpy.ops.object.transform_apply(scale=True)
    sw_right.data.materials.append(mat_dark)
    sw_right.name = "Chodnik_Prawy_Blok"
    
    bpy.ops.object.select_all(action='DESELECT')
    
    left_buildings = []
    right_buildings = []
    building_offset_x = config['building_offset_from_sidewalk']
    
    current_y = -street_length / 2
    while current_y < street_length / 2:
        b_step = random.uniform(5.0, 8.0)
        overlap = random.uniform(1.5, 3.0)
        y_pos = current_y + (b_step / 2)
        x_left = -(street_width / 2) - sidewalk_width - building_offset_x
        h = create_building(x_left, y_pos, sidewalk_height, random.uniform(4.0, 5.5), mat_dark, neon_mats, side_sign=-1)
        left_buildings.append((x_left, y_pos, h))
        current_y += (b_step - overlap)
        
    current_y = -street_length / 2
    while current_y < street_length / 2:
        b_step = random.uniform(5.0, 8.0)
        overlap = random.uniform(1.5, 3.0)
        y_pos = current_y + (b_step / 2)
        x_right = (street_width / 2) + sidewalk_width + building_offset_x
        h = create_building(x_right, y_pos, sidewalk_height, random.uniform(4.0, 5.5), mat_dark, neon_mats, side_sign=1)
        right_buildings.append((x_right, y_pos, h))
        current_y += (b_step - overlap)

    if not left_buildings or not right_buildings:
        return

    cables_created = 0
    attempts = 0
    while cables_created < config['cable_count'] and attempts < 200:
        attempts += 1
        b1 = random.choice(left_buildings)
        b2 = random.choice(right_buildings)
        
        if abs(b1[1] - b2[1]) < 20.0:
            z_height = random.uniform(5.0, min(b1[2], b2[2]) - 1.0)
            p1 = Vector((b1[0], b1[1], z_height))
            p2 = Vector((b2[0], b2[1], z_height))
            create_cable(p1, p2, mat_dark, config['cable_sag'])
            cables_created += 1

    pipes_created = 0
    attempts = 0
    while pipes_created < config['pipe_count'] and attempts < 200:
        attempts += 1
        b1 = random.choice(left_buildings)
        b2 = random.choice(right_buildings)
        
        if abs(b1[1] - b2[1]) < 15.0:
            z_height = random.uniform(5.0, min(b1[2], b2[2]) - 1.0)
            p1 = Vector((b1[0], b1[1], z_height))
            p2 = Vector((b2[0], b2[1], z_height))
            create_pipe(p1, p2, mat_dark, config['pipe_radius'])
            pipes_created += 1

if __name__ == "__main__":
    config = {
        'street_length': 200.0,                 
        'street_width': 8.0,                    
        
        'sidewalk_width': 4.0,                  
        'sidewalk_height': 0.25,                
        
        'building_offset_from_sidewalk': 1.5,   
        
        'cable_count': 50,                      
        'cable_sag': 2.0,                       
        
        'pipe_count': 10,                       
        'pipe_radius': 0.2                     
    }
    
    setup_scene()
    build_cyberpunk_street(config)