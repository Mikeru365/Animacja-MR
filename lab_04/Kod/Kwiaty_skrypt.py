import bpy
import math
import os

def stworz_materialy():
    # 1. Materiał Łodygi
    if "Mat_Lodyga" not in bpy.data.materials:
        mat_lodyga = bpy.data.materials.new(name="Mat_Lodyga")
        mat_lodyga.use_nodes = True
        bsdf = mat_lodyga.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = (0.4, 0.2, 0.1, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.9
        bsdf.inputs['Roughness'].default_value = 0.2
    
    # 2. Materiał Liścia
    if "Mat_Lisc" not in bpy.data.materials:
        mat_lisc = bpy.data.materials.new(name="Mat_Lisc")
        mat_lisc.use_nodes = True
        bsdf = mat_lisc.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = (0.0, 0.8, 1.0, 1.0)
        bsdf.inputs['Metallic'].default_value = 0.5
        bsdf.inputs['Emission Color'].default_value = (0.0, 0.5, 0.8, 1.0)
        bsdf.inputs['Emission Strength'].default_value = 15.0
        
    # 3. Materiał Korzeni 
    if "Mat_Korzen" not in bpy.data.materials:
        mat_korzen = bpy.data.materials.new(name="Mat_Korzen")
        mat_korzen.use_nodes = True
        bsdf = mat_korzen.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1.0)
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Roughness'].default_value = 0.2
        
    # 4. Materiał Podłoża
    if "Mat_Podloze" not in bpy.data.materials:
        mat_podloze = bpy.data.materials.new(name="Mat_Podloze")
        mat_podloze.use_nodes = True
        bsdf = mat_podloze.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = (0.05, 0.2, 0.02, 1.0) 
        bsdf.inputs['Metallic'].default_value = 0.3
        bsdf.inputs['Roughness'].default_value = 0.9

def dodaj_lodyge(x, wysokosc, mat):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=wysokosc, location=(x, 0, wysokosc/2))
    lodyga = bpy.context.active_object
    lodyga.data.materials.append(mat)
    return lodyga

def dodaj_liscie(x, wysokosc, liczba, promien, mat):
    for i in range(liczba):
        kat = (2 * math.pi / liczba) * i
        odsuniecie = 0.20
        lx = x + math.cos(kat) * odsuniecie
        ly = math.sin(kat) * odsuniecie
        lz = wysokosc
        
        bpy.ops.mesh.primitive_cube_add(size=promien, location=(lx, ly, lz))
        lisc = bpy.context.active_object
        lisc.data.materials.append(mat)
        lisc.rotation_euler[2] = kat
        lisc.rotation_euler[1] = math.radians(-25) 
        lisc.scale = (2.0, 0.4, 0.1)

def dodaj_korzenie(x, liczba, mat):
    for i in range(liczba):
        kat_k = (2 * math.pi / liczba) * i
        kx = x + math.cos(kat_k) * 0.2
        ky = math.sin(kat_k) * 0.2
        bpy.ops.mesh.primitive_cube_add(size=0.1, location=(kx, ky, 0.05))
        korzen = bpy.context.active_object
        korzen.data.materials.append(mat)
        korzen.rotation_euler[2] = kat_k
        korzen.rotation_euler[1] = math.radians(25) 
        korzen.scale = (3, 0.4, 0.4)

def stworz_rosline(x_offset, wysokosc=2.0, liczba_lisci=3, promien_lisci=0.3, liczba_korzeni=6):
    m_lodyga = bpy.data.materials.get("Mat_Lodyga")
    m_lisc = bpy.data.materials.get("Mat_Lisc")
    m_korzen = bpy.data.materials.get("Mat_Korzen")

    dodaj_lodyge(x_offset, wysokosc, m_lodyga)
    dodaj_liscie(x_offset, wysokosc, liczba_lisci, promien_lisci, m_lisc)
    dodaj_korzenie(x_offset, liczba_korzeni, m_korzen)

def ustaw_scene():
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
    bpy.ops.object.camera_add(location=(0, -10, 4.7), rotation=(math.radians(64), 0, 0))
    bpy.context.scene.camera = bpy.context.active_object
    
    bpy.ops.object.light_add(type='SUN', location=(7, -2, 10))
    sun = bpy.context.active_object
    sun.data.energy = 30.0
    sun.rotation_euler[0] = math.radians(-25) 
    sun.rotation_euler[2] = math.radians(250)

    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE' 
    if hasattr(scene.eevee, "use_bloom"):
        scene.eevee.use_bloom = True
        scene.eevee.bloom_intensity = 1.0    
        scene.eevee.bloom_radius = 10.0      
        scene.eevee.bloom_threshold = 0.5
    
    if bpy.data.is_saved:
        base_dir = os.path.dirname(bpy.data.filepath)
    else:
        base_dir = os.path.expanduser("~")

    output_path = os.path.join(base_dir, "kwiaty_render.png")
    
    scene.render.filepath = output_path
    scene.render.image_settings.file_format = 'PNG'
    scene.render.resolution_x = 800
    scene.render.resolution_y = 600

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

stworz_materialy()

# Podłoże
bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
podloze = bpy.context.active_object
podloze.data.materials.append(bpy.data.materials.get("Mat_Podloze"))

# Generowanie roślin
stworz_rosline(x_offset=3, wysokosc=1.0, liczba_lisci=3, liczba_korzeni = 3)
stworz_rosline(x_offset=0,  wysokosc=1.5, liczba_lisci=6)
stworz_rosline(x_offset=-3,  wysokosc=2.0, liczba_lisci=10, liczba_korzeni = 10)

ustaw_scene()
bpy.ops.render.render(write_still=True)