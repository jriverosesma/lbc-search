# LBC Search

## Overview

Use [this](https://github.com/etienne-hd/lbc) Python to search in [leboncoin](https://www.leboncoin.fr) and export - only - the relevant information in JSON format.

## Installation

### Prod

```bash
pip install git+https://github.com/jriverosesma/lbc-search.git
```

### Dev

```bash
git clone https://github.com/jriverosesma/lbc-search.git
cd lbc-search
pixi install
pixi run setup
```

## Usage

```bash
lbc --url <search-url> # Copy URL from browser. Example: "https://www.leboncoin.fr/recherche?category=20&text=aspirateur"
lbc --help # Show all options
```
