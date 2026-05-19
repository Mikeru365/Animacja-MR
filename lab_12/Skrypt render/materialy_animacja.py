import bpy
import math

NAZWA_MATERIALU = "Roslina_Bioluminescencja"
NAZWA_NODE_EMISSION = "Emission"

KLATKA_START = 1
KLATKA_KONIEC = 125
KLATKA_PAK_START = 30
KLATKA_PAK_CONIEC = 90

KOLOR_START = (0.0, 0.7, 1.0, 1.0)
KOLOR_KONIEC = (0.2, 1.0, 0.4, 1.0)

def znajdz_node(mat, nazwa, typ_zapasowy=None):
    node = mat.node_tree.nodes.get(nazwa)
    if node is None and typ_zapasowy:
        for n in mat.node_tree.nodes:
            if n.type == typ_zapasowy:
                print(f"Nie znaleziono '{nazwa}', używam '{n.name}' (typ {typ_zapasowy}).")
                return n
    if node is None:
        dostepne = [n.name for n in mat.node_tree.nodes]
        raise KeyError(f"Węzeł '{nazwa}' nie istnieje w '{mat.name}'. Dostępne: {dostepne}")
    return node

def wyczysc_animacje_materialu(mat):
    if mat.node_tree.animation_data and mat.node_tree.animation_data.action:
        mat.node_tree.animation_data.action = None

def pulsuj_emission(mat, min_str=0.5, max_str_bazowy=2.0, max_str_pik=6.0, okres=25):
    emission = znajdz_node(mat, NAZWA_NODE_EMISSION, typ_zapasowy='EMISSION')
    sciezka = f'nodes["{emission.name}"].inputs["Strength"].default_value'

    for klatka in range(KLATKA_START, KLATKA_KONIEC + 1):
        if KLATKA_PAK_START <= klatka <= KLATKA_PAK_CONIEC:
            postep = (klatka - KLATKA_PAK_START) / (KLATKA_PAK_CONIEC - KLATKA_PAK_START)
            max_str = max_str_bazowy + (max_str_pik - max_str_bazowy) * postep
        elif klatka > KLATKA_PAK_CONIEC:
            max_str = max_str_pik
        else:
            max_str = max_str_bazowy

        srednia = (min_str + max_str) / 2.0
        amplituda = (max_str - min_str) / 2.0
        t = (klatka - KLATKA_START) * (2 * math.pi / okres)
        
        emission.inputs["Strength"].default_value = srednia + amplituda * math.sin(t)
        mat.node_tree.keyframe_insert(data_path=sciezka, frame=klatka)

def animuj_kolor_emisji(mat):
    emission = znajdz_node(mat, NAZWA_NODE_EMISSION, typ_zapasowy='EMISSION')
    sciezka = f'nodes["{emission.name}"].inputs["Color"].default_value'

    emission.inputs["Color"].default_value = KOLOR_START
    mat.node_tree.keyframe_insert(data_path=sciezka, frame=KLATKA_START)
    emission.inputs["Color"].default_value = KOLOR_KONIEC
    mat.node_tree.keyframe_insert(data_path=sciezka, frame=KLATKA_KONIEC)

def main_materialy():
    mat = bpy.data.materials.get(NAZWA_MATERIALU)
    if mat is None:
        print(f"Brak materiału '{NAZWA_MATERIALU}'. Dostępne: {[m.name for m in bpy.data.materials]}")
        return
    
    wyczysc_animacje_materialu(mat)
    
    pulsuj_emission(mat)
    animuj_kolor_emisji(mat)
    
    print("Animacja materiału zakończona sukcesem.")

if __name__ == "__main__":
    main_materialy()