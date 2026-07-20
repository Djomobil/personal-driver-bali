# 📸 Brief photo — Ketut Bali Driver

**Objectif** : remplacer les illustrations du site par des photos originales, authentiques,
prises par Ketut (ou un proche) avec un smartphone récent. Les photos originales de vrais
tours convertissent mieux que n'importe quelle banque d'images — et Google favorise le
contenu original.

## Règles d'or (valables pour toutes les photos)

- **Horaire** : golden hour uniquement — 6h–8h30 ou 16h30–18h30. Jamais en plein midi
  (lumière écrasée, ombres dures).
- **Format** : horizontal (paysage), au moins 1600 px de large. Nettoyer l'objectif avant !
- **Cadrage** : règle des tiers (activer la grille dans l'appli photo). Horizon droit.
- **Personnes** : au moins 1 photo sur 2 avec des humains (clients de dos, silhouettes) —
  ça raconte une histoire. Demander l'accord des clients, éviter les visages reconnaissables
  sans permission.
- **Interdits** : filtres Instagram, zoom numérique, photos floues, foule dense à l'image.

## Liste des prises de vue (dans l'ordre de priorité)

| # | Fichier attendu | Sujet | Conseil de cadrage |
|---|---|---|---|
| 1 | `assets/ketut.jpg` | **Portrait de Ketut** souriant devant sa voiture propre | Carré, à hauteur d'yeux, fond simple (voiture + verdure), lumière douce du matin |
| 2 | `assets/photos/ubud.jpg` | Rizières de **Tegalalang** | Plongée légère sur les courbes des terrasses, un palmier dans le cadre |
| 3 | `assets/photos/uluwatu.jpg` | **Uluwatu** au coucher du soleil | Temple en silhouette sur la falaise, océan doré, contre-jour assumé |
| 4 | `assets/photos/east-bali.jpg` | **Lempuyang** (Portes du Paradis) | Symétrie parfaite entre les deux portes, volcan Agung centré |
| 5 | `assets/photos/north-bali.jpg` | Cascade **Sekumpul** ou Gitgit | Pose longue si possible (mode nuit), personne minuscule pour l'échelle |
| 6 | `assets/photos/multi-sunrise.jpg` | Lever de soleil vallée de **Sidemen** | Brume matinale sur les rizières, premier plan végétal |
| 7 | `assets/photos/multi-best.jpg` | Temple **Ulun Danu Beratan** sur le lac | Reflet du temple dans l'eau, tôt le matin (lac calme) |
| 8 | `assets/photos/multi-island.jpg` | Route côtière ou falaise **Kelingking** (Nusa Penida) | Point de vue haut, courbe de la route ou de la falaise |
| 9 | `assets/photos/tanah-lot.jpg` | **Tanah Lot** à marée haute | Temple isolé par la mer, coucher de soleil |
| 10 | `assets/photos/monkey-forest.jpg` | **Monkey Forest** d'Ubud | Singe net au premier plan, statue moussue en arrière-plan flou |
| 11 | `assets/photos/melasti.jpg` | Plage de **Melasti** | Falaises blanches + eau turquoise, depuis la route en lacets |
| 12 | `assets/photos/handara.jpg` | **Handara Gate** | Symétrie frontale, personne au centre pour l'échelle |
| 13 | `assets/photos/sekumpul.jpg` | Sekumpul (vue large) | Les deux chutes dans le cadre, jungle autour |
| 14 | `assets/photos/tegalalang.jpg` | Tegalalang (variante) | Contre-plongée depuis le bas des terrasses |
| 15 | `assets/photos/kelingking.jpg` | Kelingking « T-Rex » | L'arête entière + plage blanche en bas |

**Bonus qui vendent** (à glisser dans la galerie plus tard) : la voiture climatisée propre
portes ouvertes, une pancarte d'accueil aéroport avec un nom, des clients qui trinquent à
une noix de coco, l'intérieur de la voiture avec bouteilles d'eau fraîche.

## Une fois les photos prises

1. Les transférer telles quelles (pas de compression WhatsApp : utiliser « Document »
   ou Google Drive).
2. Les renommer selon la colonne « Fichier attendu » et les déposer dans le dépôt
   (`assets/photos/`), ou me les envoyer — je m'occupe du recadrage, de la compression
   (~1400 px, < 300 Ko) et de l'intégration.
3. `python3 tools/build.py` puis push : le site bascule automatiquement sur les photos.
