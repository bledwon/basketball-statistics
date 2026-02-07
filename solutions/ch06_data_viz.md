# Chapter 6 — Data Analysis & Visualization (Exercises)

Assume team‑game data in `dftg` with fields like `fg3a`, `fg3_pct`, `ft_pct`, `wl`, `team`.

## 6.1 Distributions of 3‑pt attempts
### Python (pandas + matplotlib)
```python
import pandas as pd
import matplotlib.pyplot as plt

# dftg = pd.read_csv('team_game.csv')

# (a) distribution
plt.hist(dftg['fg3a'], bins=30)
plt.title('Distribution of 3PT Attempts')
plt.xlabel('3PT Attempts')
plt.ylabel('Count')
plt.show()

# (b) same plot, colored by win/loss
wins = dftg[dftg['wl'] == 'W']['fg3a']
loss = dftg[dftg['wl'] == 'L']['fg3a']
plt.hist([wins, loss], bins=30, label=['Win','Loss'], alpha=0.7)
plt.title('3PT Attempts by Win/Loss')
plt.legend()
plt.show()

# (c) separate plots
fig, ax = plt.subplots(1,2, figsize=(10,4))
ax[0].hist(wins, bins=30); ax[0].set_title('Wins')
ax[1].hist(loss, bins=30); ax[1].set_title('Losses')

# (e) facet by team (small multiples)
teams = dftg['team'].unique()
cols = 5
rows = (len(teams) + cols - 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(cols*3, rows*2.5))
axes = axes.flatten()
for i, t in enumerate(teams):
    axes[i].hist(dftg[dftg['team']==t]['fg3a'], bins=15)
    axes[i].set_title(t)
for j in range(i+1, len(axes)):
    axes[j].axis('off')
plt.tight_layout()
```

### R (ggplot2)
```r
library(ggplot2)

# (a)
ggplot(dftg, aes(fg3a)) +
  geom_histogram(bins = 30) +
  labs(title = 'Distribution of 3PT Attempts')

# (b)
ggplot(dftg, aes(fg3a, fill = wl)) +
  geom_histogram(bins = 30, alpha = 0.6, position = 'identity') +
  labs(title = '3PT Attempts by Win/Loss')

# (c) separate plots
ggplot(dftg, aes(fg3a)) +
  geom_histogram(bins = 30) +
  facet_wrap(~ wl)

# (e) facet by team
ggplot(dftg, aes(fg3a)) +
  geom_histogram(bins = 15) +
  facet_wrap(~ team, ncol = 5)
```

### Tableau
- Drag `fg3a` to Columns, set **Histogram**.
- Add `wl` to Color to compare wins vs losses.
- Use **Small Multiples** by placing `team` on Rows/Columns.

## 6.2 3PT attempts vs FT%
### Python
```python
plt.scatter(dftg['fg3a'], dftg['ft_pct'])
plt.title('3PT Attempts vs FT%')
plt.xlabel('3PT Attempts')
plt.ylabel('FT%')
plt.show()

# (b) jitter
plt.scatter(dftg['fg3a'] + np.random.normal(0, 0.5, len(dftg)), dftg['ft_pct'])
plt.title('3PT Attempts vs FT% (jittered)')
plt.show()

# (c) correlation
corr = dftg['fg3a'].corr(dftg['ft_pct'])
```

### R
```r
cor(dftg$fg3a, dftg$ft_pct, use='complete.obs')
```

### Tableau
- Scatter plot with `fg3a` on Columns and `ft_pct` on Rows.
- Add trend line and show correlation in the tooltip.
