# Blackjack Turtle Demos

Small experiments built with Python's `turtle` module: three blackjack iterations (`src/blackjack_v1.py`, `src/blackjack_v2.py`, `src/blackjack_v3.py`) and a solitaire scratch file (`src/solitaire.py`). Assets live alongside the code so everything can run locally without hard‑coded absolute paths.

## Layout
- `src/`: playable scripts (v3 is the most complete), plus the solitaire prototype.
- `assets/cards/`: card face and back images.
- `assets/ui/`: background and button art (hit, stand, rules, play-again).

## Run locally
From the repo root:
- `python src/blackjack_v3.py` (recommended)  
- `python src/blackjack_v2.py`  
- `python src/blackjack_v1.py`  
- `python src/solitaire.py` (background + sample sprite only)

These scripts open a `turtle` window, so you need a Python install with `tkinter` available and a GUI session (no headless runs).

## Notes
- Asset paths are resolved relative to each script's location; keep the `assets/` folder beside `src/`.
- The card art is from Bryon Knoll (opengameart.org) and the felt background credit is embedded in the code.
