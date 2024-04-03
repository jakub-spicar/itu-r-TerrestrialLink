# itu-r-TerrestrialLink

Tento projekt se zaměřuje na výpočet a vizualizaci výškového profilu bezdrátového spoje mezi dvěma body. Projekty zahrnuje výpočet výškového profilu na základě digitálního modelu terénu (DEM), výpočet zakřivení Země a výpočet Fresnelovy zóny pro bezdrátový spoj.

## Požadavky

- Python 3.x
- NumPy
- Matplotlib
- Pandas
- GDAL (pro práci s DEM soubory)

## Instalace

1. Instalace závislostí: `$ conda create --name env --file requirements.txt`
2. Stažení DEM souboru: DEM soubor je potřebný pro výpočet výškového profilu. Soubor by měl být umístěn ve složce `data`. DEM pro vzorovou oblast `N50E014` byl stažen z [ASTER](https://gdemdl.aster.jspacesystems.or.jp/index_en.html)

Note: For package management is used [MiniConda](https://docs.anaconda.com/free/miniconda/index.html)

## Funkcionalita

- Výpočet výškového profilu: Skript vypočítá výškový profil bezdrátového spoje na základě digitálního modelu terénu (DEM).
- Výpočet zakřivení Země: Skript vypočítá, jak se zakřiví Země podél spoje, což ovlivňuje výškový profil.
- Výpočet Fresnelovy zóny: Skript vypočítá Fresnelovu zónu pro bezdrátový spoj, která je důležitá pro výpočet dostupnosti spoje.
- Vizualizace výsledků: Skript vytvoří grafy výškového profilu, zakřivení Země a Fresnelovy zóny.
