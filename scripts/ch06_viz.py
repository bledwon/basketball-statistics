#!/usr/bin/env python3
"""Runnable Chapter 6 visualization exercises.
Saves plots to ./figures.
"""
from os import path, getenv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE = '/Users/benledwon/Desktop/Github_connection/basketball_statistics'
DATA_DIR = getenv('DATA_DIR', '/Users/benledwon/Desktop/LearnPythonBB/code-basketball-files-main/data')
FIG_DIR = path.join(BASE, 'figures')

# Load team game data
file = path.join(DATA_DIR, 'team_games.csv')
dftg = pd.read_csv(file)

# 6.1 distribution of 3pt attempts
plt.figure(figsize=(8,5))
plt.hist(dftg['fg3a'], bins=30)
plt.title('Distribution of 3PT Attempts')
plt.xlabel('3PT Attempts')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(path.join(FIG_DIR, 'ch06_3pa_dist.png'), dpi=200)
plt.close()

# (b) win/loss overlay
wins = dftg[dftg['wl'] == 'W']['fg3a']
loss = dftg[dftg['wl'] == 'L']['fg3a']
plt.figure(figsize=(8,5))
plt.hist([wins, loss], bins=30, label=['Win','Loss'], alpha=0.7)
plt.title('3PT Attempts by Win/Loss')
plt.legend()
plt.tight_layout()
plt.savefig(path.join(FIG_DIR, 'ch06_3pa_winloss_overlay.png'), dpi=200)
plt.close()

# (c) separate plots
fig, ax = plt.subplots(1,2, figsize=(10,4))
ax[0].hist(wins, bins=30); ax[0].set_title('Wins')
ax[1].hist(loss, bins=30); ax[1].set_title('Losses')
for a in ax:
    a.set_xlabel('3PT Attempts')
    a.set_ylabel('Count')
plt.tight_layout()
plt.savefig(path.join(FIG_DIR, 'ch06_3pa_winloss_split.png'), dpi=200)
plt.close()

# (e) by team (small multiples)
teams = dftg['team'].unique()
cols = 5
rows = (len(teams) + cols - 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(cols*3, rows*2.5))
axes = axes.flatten()
for i, t in enumerate(teams):
    axes[i].hist(dftg[dftg['team']==t]['fg3a'], bins=15)
    axes[i].set_title(t, fontsize=8)
for j in range(i+1, len(axes)):
    axes[j].axis('off')
plt.tight_layout()
plt.savefig(path.join(FIG_DIR, 'ch06_3pa_by_team.png'), dpi=200)
plt.close()

# 6.2 scatter + jitter + correlation
plt.figure(figsize=(7,5))
plt.scatter(dftg['fg3a'], dftg['ft_pct'])
plt.title('3PT Attempts vs FT%')
plt.xlabel('3PT Attempts')
plt.ylabel('FT%')
plt.tight_layout()
plt.savefig(path.join(FIG_DIR, 'ch06_3pa_vs_ft.png'), dpi=200)
plt.close()

plt.figure(figsize=(7,5))
plt.scatter(dftg['fg3a'] + np.random.normal(0, 0.5, len(dftg)), dftg['ft_pct'])
plt.title('3PT Attempts vs FT% (Jittered)')
plt.xlabel('3PT Attempts')
plt.ylabel('FT%')
plt.tight_layout()
plt.savefig(path.join(FIG_DIR, 'ch06_3pa_vs_ft_jitter.png'), dpi=200)
plt.close()

corr = dftg['fg3a'].corr(dftg['ft_pct'])
print('Correlation (fg3a vs ft_pct):', round(corr, 4))
print('Saved plots in figures/.')
