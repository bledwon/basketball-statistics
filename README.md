# Basketball Statistics — Chapter Exercises

This repo contains my **solutions** to the end‑of‑chapter exercises from *Learn to Code with Basketball*. I focused on **pandas (Python)**, **R**, and **Tableau‑oriented visualization steps**, with SQL where required.

## What’s Included
- `solutions/ch01_introduction.md`
- `solutions/ch02_python.md`
- `solutions/ch03_pandas.md`
- `solutions/ch04_sql.md`
- `solutions/ch06_data_viz.md`
- `solutions/ch07_modeling.md`
- `scripts/` — runnable scripts for Chapters 3, 6, 7
- `figures/` — generated plots from Chapter 6

## Tableau Dashboard
I built a **strong, interactive Tableau dashboard** to explore team shooting behavior and outcomes, with linked views for distributions, scatter relationships, and team rankings.

Key views:
- 3PT Attempts Distribution (Win vs Loss)
- 3PT Attempts vs FT% (scatter with win/loss color)
- Average 3PT Attempts by Team
- Win Rate by Team

Images:
![Tableau NBA Data Dashboard](figures/Tableau%20NBA%20Data%20Dashboard.png)
![3PT Attempts Distribution](figures/3PT%20Attempts%20Distribution.png)
![3PT Attempts vs FT percent](figures/3PT%20Attempts%20vs%20FT%20percent.png)
![Average 3PT Attempts by Team](figures/Average%203PT%20Attempts%20by%20Team.png)
![Win Rate by Team](figures/Win%20Rate%20by%20Team.png)

## Tools Used
- Python (pandas, matplotlib, statsmodels, scikit‑learn)
- R (dplyr, ggplot2, randomForest)
- SQL (standard / SQLite style)
- Tableau (visualization workflow notes)

## Notes
- The PDF book is **not** included in this repo.
- Some exercises depend on local datasets referenced in the book (e.g., `./data/...`). The solutions show the code and logic; you can plug in your local paths to run them.
  - Set `DATA_DIR` when running scripts, e.g. `DATA_DIR=/path/to/data python3 scripts/ch06_viz.py`.

If you want me to convert any chapter into runnable scripts or notebooks, I can do that next.
