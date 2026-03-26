**Lab 05 bpy – Generator Lasu z Typami Roślin i Biomami**

**Opis**
Kod robiony na bazie kodu z laboratorium 4 do którego został dodany zaawansowany system podziału na biomy, który automatycznie wybiera typ roślinności (drzewo, krzew lub paproć) w zależności od odległości od centrum pola, co tworzy naturalną strukturę lasu. Została dodana także baza parametrów roślin TYPY_ROSLIN, przechowująca unikalne zakresy wysokości, liczby liści oraz kolorystyki dla każdego gatunku, co pozwala na generowanie różnorodnych osobników przy użyciu funkcji random. Kolejnym dodanym elementem jest system losowania pozycji i parametrów. Dodano także wielowarstwową strukturę liści w funkcji dodaj_liscie, gdzie każda warstwa posiada inne nachylenie i skalę, nadając roślinom bardziej naturalny kształt. Ostatnim elementem jest automatyczne zarządzanie kolekcjami w Blenderze, które czyści scenę przed każdym generowaniem i grupuje wszystkie obiekty w nowo utworzonej kolekcji "Las".

**Aktywacja**
Aktywacja przy pomocy kodu Generowanie_Lasu.py w srodowisku blender, albo przy pomocy pliku KwiatSkrypt.blend
Renderowany plik las_biomy_render.png domyślnie zapisuje się w tym samym folderze, w którym znajduje się plik .blend