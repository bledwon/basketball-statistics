import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "nba_2024_25_team_styles.csv")
FIG_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "figures"))

os.makedirs(FIG_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# Correlation bar chart
metrics = ["eDiff", "ORtg", "DRtg", "eFG%", "TOV%", "Pace", "ORB%"]
correlations = df[metrics + ["PCT"]].corr(numeric_only=True)["PCT"].drop("PCT")
correlations = correlations.sort_values(ascending=True)

plt.figure(figsize=(8, 5))
colors = ["#d9534f" if v < 0 else "#5cb85c" for v in correlations.values]
plt.barh(correlations.index, correlations.values, color=colors)
plt.axvline(0, color="#333333", linewidth=1)
plt.title("Correlation With Win% (2024–25)")
plt.xlabel("Correlation")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "insight_corr_winpct.png"), dpi=200)
plt.close()


def scatter_with_trend(x_col, y_col, title, out_name, x_label=None, y_label=None):
    x = df[x_col].to_numpy()
    y = df[y_col].to_numpy()
    plt.figure(figsize=(6.5, 5))
    plt.scatter(x, y, alpha=0.75, edgecolor="white", linewidth=0.5)
    # Trend line
    coef = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 100)
    ys = coef[0] * xs + coef[1]
    plt.plot(xs, ys, color="#333333", linewidth=2)
    plt.title(title)
    plt.xlabel(x_label or x_col)
    plt.ylabel(y_label or y_col)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, out_name), dpi=200)
    plt.close()

scatter_with_trend(
    "eFG%",
    "PCT",
    "Shooting Efficiency vs Win% (2024–25)",
    "insight_efg_winpct.png",
    x_label="Team eFG%",
    y_label="Win%",
)

scatter_with_trend(
    "TOV%",
    "PCT",
    "Turnover Rate vs Win% (2024–25)",
    "insight_tov_winpct.png",
    x_label="Team TOV%",
    y_label="Win%",
)

scatter_with_trend(
    "DRtg",
    "PCT",
    "Defensive Rating vs Win% (2024–25)",
    "insight_drtg_winpct.png",
    x_label="Team Defensive Rating",
    y_label="Win%",
)

print("Saved insight charts to", FIG_DIR)
