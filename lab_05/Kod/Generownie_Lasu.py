import bpy
import math
import random
import os

TYPY_ROSLIN = {
    "drzewo": {
        "wysokosc": (3.0, 5.0),   # zakres (min, max) dla random.uniform()
        "liczba_lisci": (4, 6),
        "promien_lisci": (0.4, 0.7),
        "liczba_korzeni": (4, 6),
        "kolor_lodygi": (0.15, 0.08, 0.02, 1),  # ciemny brąz
        "kolor_lisci": (0.05, 0.35, 0.1, 1),   # ciemna zieleń
        "kolor_korzeni":(0.15, 0.08, 0.02, 1),
    },
    "krzew": {
        "wysokosc": (0.8, 1.8),
        "liczba_lisci": (5, 8),
        "promien_lisci": (0.5, 0.9),
        "liczba_korzeni": (2, 4),
        "kolor_lodygi": (0.25, 0.15, 0.05, 1),  # jasny brąz
        "kolor_lisci": (0.1, 0.5, 0.05, 1),     # żywa zieleń
        "kolor_korzeni":(0.25, 0.15, 0.05, 1),
    },
    "paproc": {
        "wysokosc": (0.5, 1.2),
        "liczba_lisci": (6, 10),
        "promien_lisci": (0.6, 1.0),
        "liczba_korzeni": (2, 3),
        "kolor_lodygi": (0.2, 0.3, 0.1, 1),     # oliwkowy
        "kolor_lisci": (0.0, 0.6, 0.15, 1),     # soczysty zielony
        "kolor_korzeni":(0.2, 0.3, 0.1, 1),
    },
}

def dodaj_lodyge(pozycja, wysokosc, kolor):
    x, y, z = pozycja
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=wysokosc, location=(x, y, z + wysokosc/2))
    lodyga = bpy.context.active_object
    mat = bpy.data.materials.new(name="Mat_Lodyga")
    mat.use_nodes = True
    mat.node_tree.nodes.get("Principled BSDF").inputs['Base Color'].default_value = kolor
    lodyga.data.materials.append(mat)
    return lodyga

def dodaj_liscie(pozycja, wysokosc, liczba, promien, kolor):
    x, y, z = pozycja
    stworzone_liscie = []
    mat = bpy.data.materials.new(name="Mat_Lisc")
    mat.use_nodes = True
    mat.node_tree.nodes.get("Principled BSDF").inputs['Base Color'].default_value = kolor
    
    warstwy = [
        (0.0, -25, (2.0, 0.4, 0.1)),
        (0.2, -70, (1.4, 0.3, 0.1)),
        (0.1, -45, (1.7, 0.35, 0.1))
    ]
    
    for h_off, rot_x, skala in warstwy:
        for i in range(liczba):
            kat = (2 * math.pi / liczba) * i + random.uniform(-0.1, 0.1)
            lx = x + math.cos(kat) * 0.15
            ly = y + math.sin(kat) * 0.15
            lz = z + wysokosc + h_off
            bpy.ops.mesh.primitive_cube_add(size=promien, location=(lx, ly, lz))
            lisc = bpy.context.active_object
            lisc.data.materials.append(mat)
            lisc.rotation_euler[2] = kat
            lisc.rotation_euler[1] = math.radians(rot_x)
            lisc.scale = skala
            stworzone_liscie.append(lisc)
    return stworzone_liscie

def dodaj_korzenie(pozycja, liczba, kolor):
    x, y, z = pozycja
    stworzone_korzenie = []
    mat = bpy.data.materials.new(name="Mat_Lisc")
    mat.use_nodes = True
    mat.node_tree.nodes.get("Principled BSDF").inputs['Base Color'].default_value = kolor
    for i in range(liczba):
        kat_k = (2 * math.pi / liczba) * i
        kx = x + math.cos(kat_k) * 0.35
        ky = y + math.sin(kat_k) * 0.35
        bpy.ops.mesh.primitive_cube_add(size=0.25, location=(kx, ky, z + 0.05))
        korzen = bpy.context.active_object
        korzen.data.materials.append(mat)
        korzen.rotation_euler[1] = math.radians(25)
        korzen.rotation_euler[2] = kat_k
        korzen.scale = (3, 0.4, 0.4)
        stworzone_korzenie.append(korzen)
    return stworzone_korzenie

def dodaj_podloze(rozmiar_pola):
    bpy.ops.mesh.primitive_plane_add(size=rozmiar_pola, location=(0, 0, 0))
    podloze = bpy.context.active_object
    podloze.name = "Podloze_Las"
    
    mat = bpy.data.materials.new(name="Mat_Podloze")
    mat.use_nodes = True
    mat.node_tree.nodes.get("Principled BSDF").inputs['Base Color'].default_value = (0.05, 0.04, 0.02, 1)
    mat.node_tree.nodes.get("Principled BSDF").inputs['Roughness'].default_value = 1.0
    
    podloze.data.materials.append(mat)
    return podloze

def stworz_rosline_typ(x, z, typ):
    if typ not in TYPY_ROSLIN: return []
    dane = TYPY_ROSLIN[typ]
    h = random.uniform(*dane["wysokosc"])
    n_l = random.randint(*dane["liczba_lisci"])
    p_l = random.uniform(*dane["promien_lisci"])
    n_k = random.randint(*dane["liczba_korzeni"])
    
    pos = (x, z, 0)
    czesci = []
    czesci.append(dodaj_lodyge(pos, h, dane["kolor_lodygi"]))
    czesci.extend(dodaj_liscie(pos, h, n_l, p_l, dane["kolor_lisci"]))
    czesci.extend(dodaj_korzenie(pos, n_k, dane["kolor_korzeni"]))
    return czesci

def wybierz_typ_biomu(x, z, rozmiar_pola):
    max_dystans = rozmiar_pola / 2
    aktualny_dystans = max(abs(x), abs(z))
    procent = aktualny_dystans / max_dystans if max_dystans > 0 else 0
    if procent < 0.3: return "drzewo"
    elif 0.3 <= procent <= 0.7: return "krzew" if random.random() < 0.7 else "drzewo"
    else: return "paproc" if random.random() < 0.6 else "krzew"

def generuj_las(liczba_roslin=50, rozmiar_pola=20.0, seed=20):
    random.seed(seed)
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    if "Las" in bpy.data.collections:
        old_coll = bpy.data.collections["Las"]
        for obj in old_coll.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old_coll)

    kolekcja_las = bpy.data.collections.new("Las")
    bpy.context.scene.collection.children.link(kolekcja_las)

    ziemia = dodaj_podloze(rozmiar_pola)
    for coll in ziemia.users_collection:
        coll.objects.unlink(ziemia)
    kolekcja_las.objects.link(ziemia)

    for _ in range(liczba_roslin):
        x = random.uniform(-rozmiar_pola/2.2, rozmiar_pola/2.2) 
        z = random.uniform(-rozmiar_pola/2.2, rozmiar_pola/2.2)
        
        typ = wybierz_typ_biomu(x, z, rozmiar_pola)
        obiekty = stworz_rosline_typ(x, z, typ)
        
        for obj in obiekty:
            for coll in obj.users_collection:
                coll.objects.unlink(obj)
            kolekcja_las.objects.link(obj)
            
    
    bpy.ops.object.light_add(type='SUN', location=(7, -8, 10))
    sun = bpy.context.active_object
    sun.data.energy = 10.0
    sun.rotation_euler = (math.radians(45), 0, math.radians(45))

    bpy.ops.object.camera_add(location=(rozmiar_pola, -rozmiar_pola, rozmiar_pola * 1.1))
    kamera = bpy.context.active_object
    kamera.rotation_euler = (math.radians(50), 0, math.radians(45))
    bpy.context.scene.camera = kamera

    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    if hasattr(scene.eevee, "use_bloom"):
        scene.eevee.use_bloom = True
        scene.eevee.bloom_intensity = 0.8

    base_dir = os.path.dirname(bpy.data.filepath) if bpy.data.is_saved else os.path.expanduser("~")
    scene.render.filepath = os.path.join(base_dir, "las_biomy_render.png")
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720

    print(f"Renderowanie do: {scene.render.filepath}")
    bpy.ops.render.render(write_still=True)

generuj_las(liczba_roslin=100, rozmiar_pola=20.0, seed=20)