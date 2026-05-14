import bpy
import os
import math

SCIEZKA = r"\lab_11\Skrypt render\roslinahero07ModelA.blend"
NAZWA_KOLEKCJI = "Roslina_Hero"
KLATKA_START = 1
KLATKA_KONIEC = 125

def importuj_rosline(sciezka_blend, nazwa_kolekcji):
    if not os.path.exists(sciezka_blend):
        return
    sciezka_kolekcji = os.path.join(sciezka_blend, "Collection", nazwa_kolekcji)
    bpy.ops.wm.append(
        filepath=sciezka_kolekcji,
        directory=os.path.join(sciezka_blend, "Collection"),
        filename=nazwa_kolekcji,
    )

def wyczysc_wszystkie_animacje():
    for obj in bpy.data.objects:
        if obj.animation_data:
            obj.animation_data_clear()
    for action in bpy.data.actions:
        bpy.data.actions.remove(action)

def animuj_liscie_kolysanie(obj_name, faza=0.0, czestosc=0.05, amplituda=0.05):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return
    
    rot_y_bazowa = obj.rotation_euler[1]
    for klatka in range(KLATKA_START, KLATKA_KONIEC + 1):
        obj.rotation_euler[1] = rot_y_bazowa + amplituda * math.sin(klatka * czestosc + faza)
        obj.keyframe_insert(data_path="rotation_euler", frame=klatka, index=1)

def animuj_skalowanie_odwrotne(obj_name, k_start=30, k_koniec=90, s_min=0.08, s_max=0.18):
    obj = bpy.data.objects.get(obj_name)
    if not obj: return

    obj.scale[0] = s_min
    obj.scale[1] = s_min
    obj.scale[2] = -s_min 
    obj.keyframe_insert(data_path="scale", frame=KLATKA_START)
    obj.keyframe_insert(data_path="scale", frame=k_start)

    obj.scale[0] = s_max
    obj.scale[1] = s_max
    obj.scale[2] = -s_max 
    obj.keyframe_insert(data_path="scale", frame=k_koniec)
    obj.keyframe_insert(data_path="scale", frame=KLATKA_KONIEC)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

importuj_rosline(SCIEZKA, NAZWA_KOLEKCJI)
wyczysc_wszystkie_animacje()

obiekty_do_skalowania = ["Kwiat.001", "Kwiat.002", "Kwiat.003"]

for nazwa in obiekty_do_skalowania:
    if nazwa in bpy.data.objects:
        animuj_skalowanie_odwrotne(nazwa, s_min=0.08, s_max=0.15)

if "Kwiat.001" in bpy.data.objects:
    animuj_liscie_kolysanie("Kwiat.001")