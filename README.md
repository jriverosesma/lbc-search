![Version](https://img.shields.io/badge/version-0.1.0-blue?style=for-the-badge)
[![License](https://img.shields.io/github/license/jriverosesma/lbc-search?style=for-the-badge)](https://github.com/jriverosesma/lbc-search/blob/main/LICENSE)
# LBC Search

## Overview

Small util using [this](https://github.com/etienne-hd/lbc) Python package to search in [leboncoin](https://www.leboncoin.fr) and export - only - the relevant information in JSON format.

## Installation

```bash
pip install git+https://github.com/jriverosesma/lbc-search.git
```

## Usage

```bash
lbc --url <search-url> # Copy URL from browser
lbc --help # Show all options
```

Example:

```bash
lbc --url "https://www.leboncoin.fr/recherche?category=20&text=aspirateur"
```

Output result:

`lbc_results.json`
```json
[
    {
        "title": "Kobold PB7",
        "description": "Quitte textile, PB7 \nCompatible avec aspirateur kobold, VK sept. Possibilité de tester le bon fonctionnement.\nNeuf jamais utilisé encore dans l’emballage. \nEn vente sur le Worwerk à 349€",
        "date": "2026-02-22 16:37:30",
        "price": 180.0,
        "user_score": 5,
        "nb_user_evaluations": 3,
        "url": "https://www.leboncoin.fr/ad/electromenager/3149528941"
    },
    {
        "title": "Aspirateur balai sans fils neuf Verslife Z8",
        "description": "Jamais utilisé, vendu avec boîte d’origine, chargeur secteur, accessoires, notice.\n\nVersLife Z8 Aspirateur Balai Sans Fil, 40Kpa/45Min/500W/6 En 1 Aspirateur Balai Léger avec LED Verte, Filtration En 6 Étapes, Écran LED, Autoportant pour Poils D’animaux, sols Durs et Moquettes (Gris)",
        "date": "2026-02-22 10:51:15",
        "price": 65.0,
        "user_score": 4.95,
        "nb_user_evaluations": 31,
        "url": "https://www.leboncoin.fr/ad/electromenager/3149242254"
    },
    ...
]
```

## Development (using Pixi as package manager)

```bash
git clone https://github.com/jriverosesma/lbc-search.git
cd lbc-search
pixi install
pixi run setup
```
