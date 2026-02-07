# Chapter 3 — Pandas (Exercises)

All solutions assume your data files are in a local `DATA_DIR` and can be loaded with pandas. Replace file names as needed.

```python
import pandas as pd
from os import path
DATA_DIR = './data'
```

## 3.0 — Basics (games)
```python
# 3.0.1
games = pd.read_csv(path.join(DATA_DIR, 'games.csv'))

# 3.0.2
games['date'] = pd.to_datetime(games['date'])
game50 = games.sort_values('date').head(50)

# 3.0.3
games_sorted = games.sort_values('home_pts', ascending=False)

# 3.0.4
type(games.sort_values('home_pts'))  # pandas.DataFrame

# 3.0.5
cols = ['date','home','away','home_pts','away_pts']
game_simple = games[cols].copy()

game_simple = game_simple[['home','away','date','home_pts','away_pts']]

game_simple['game_id'] = games['game_id']

game_simple.to_csv(path.join(DATA_DIR, 'game_simple.txt'), sep='|', index=False)
```

## 3.1 — Columns (player_game)
```python
pg = pd.read_csv(path.join(DATA_DIR, 'player_game.csv'))

pg['net_takeaways'] = pg['stl'] - pg['tov']

pg['player_desc'] = pg['name'] + ' is the ' + pg['team'] + ' ' + pg['position']

pg['bad_game'] = (pg['fga'] > 20) & (pg['pts'] < 15)

pg['len_last_name'] = pg['name'].str.split().str[-1].str.len()

pg['game_id'] = pg['game_id'].astype(str)

# replace underscores with spaces
pg.columns = [c.replace('_', ' ') for c in pg.columns]
# revert if desired
pg.columns = [c.replace(' ', '_') for c in pg.columns]

pg['oreb_percentage'] = pg['oreb'] / pg['reb']
pg['oreb_percentage'] = pg['oreb_percentage'].fillna(-99)

pg = pg.drop(columns=['oreb_percentage'])
```

## 3.2 — Summary stats
```python
pg = pd.read_csv(path.join(DATA_DIR, 'player_game.csv'))

pg['total_shots1'] = pg['fga'] + pg['fta']
pg['total_shots2'] = pg[['fga','fta']].sum(axis=1)

pg[['pts','fga','reb']].mean()

n_40_10 = pg[(pg['pts'] >= 40) & (pg['reb'] >= 10)].shape[0]

pct_40_10 = n_40_10 / pg[pg['pts'] >= 40].shape[0]

total_3pa = pg['fg3a'].sum()

team_counts = pg['team'].value_counts()
most_team = team_counts.idxmax()
least_team = team_counts.idxmin()
```

## 3.3 — Filtering
```python
dftg = pd.read_csv(path.join(DATA_DIR, 'team_game.csv'))

cols = ['team','date','pts','fgm','fga']

# loc
chi = dftg.loc[dftg['team'] == 'CHI', cols]
# query
chi2 = dftg.query("team == 'CHI'")[cols]

no_chi = dftg.loc[dftg['team'] != 'CHI', cols]

# duplicate shooting performances
fg_dup = dftg.duplicated(subset=['fgm','fga','fg3m','fg3a'], keep=False)
dftg_fg_dup = dftg[fg_dup]
dftg_fg_no_dup = dftg[~fg_dup]

# three_pt_desc
pct3 = dftg['fg3m'] / dftg['fg3a']

dftg['three_pt_desc'] = pd.NA
dftg.loc[pct3 > 0.50, 'three_pt_desc'] = 'great'
dftg.loc[pct3 <= 0.25, 'three_pt_desc'] = 'brutal'

no_desc1 = dftg.loc[dftg['three_pt_desc'].isna()]
no_desc2 = dftg.query('three_pt_desc.isna()')
```

## 3.4 — Granularity / groupby
```python
# 3.4.1 — Conceptual answer:
#   Moving to higher granularity (more detail) increases row count and detail;
#   lower granularity (aggregation) reduces detail but can highlight trends.

# 3.4.2
team_avg_pts = dftg.groupby('team')['pts'].mean()

pct_100 = dftg.assign(ge100 = dftg['pts'] >= 100).groupby('team')['ge100'].mean()

teams_150 = dftg.groupby('team')['pts'].max().loc[lambda s: s >= 150]

# count vs sum
counts = dftg.groupby('date')['team_id'].count()
sums = dftg.groupby('date')['team_id'].sum()

# 3.4.3
agg = dftg.groupby(['team_id','wl']).agg(
    ave_pts=('pts','mean'),
    ave_fgm=('fgm','mean'),
    ave_fga=('fga','mean'),
    ave_fg3m=('fg3m','mean'),
    ave_fg3a=('fg3a','mean'),
    n=('wl','count')
).reset_index()

loss_high = agg[(agg['wl'] == 'L') & (agg['ave_pts'] > 110)]

agg_team = dftg.groupby(['team','wl']).agg(
    ave_pts=('pts','mean'),
    ave_fgm=('fgm','mean'),
    ave_fga=('fga','mean'),
    ave_fg3m=('fg3m','mean'),
    ave_fg3a=('fg3a','mean'),
    n=('wl','count')
)
```

## 3.5 — Combining DataFrames
```python
# combine1
pts = pd.read_csv(path.join(DATA_DIR, 'problems/combine1/pts.csv'))
reb = pd.read_csv(path.join(DATA_DIR, 'problems/combine1/reb.csv'))
defense = pd.read_csv(path.join(DATA_DIR, 'problems/combine1/def.csv'))

# merge (outer to keep all players)
merge1 = pts.merge(reb, on='player_id', how='outer').merge(defense, on='player_id', how='outer')
merge1 = merge1.fillna(0)

# concat (set index first)
pts_i = pts.set_index('player_id')
reb_i = reb.set_index('player_id')
def_i = defense.set_index('player_id')
concat1 = pd.concat([pts_i, reb_i, def_i], axis=1).fillna(0).reset_index()

# combine2 (vertical split)
parts = [pd.read_csv(path.join(DATA_DIR, 'problems/combine2', f)) for f in ['guards.csv','wings.csv','bigs.csv']]
combined = pd.concat(parts, axis=0).reset_index(drop=True)

# teams by conference
teams = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))
for conf, df in teams.groupby('conference'):
    df.to_csv(path.join(DATA_DIR, f'teams_{conf}.csv'), index=False)

# one‑liner reload + concat
conf_frames = [pd.read_csv(path.join(DATA_DIR, f'teams_{c}.csv')) for c in ['East','West']]
teams_all = pd.concat(conf_frames, axis=0, ignore_index=True)
```

## R equivalents (optional)
```r
library(dplyr)
# Example: avg points by team
team_avg_pts <- dftg %>% group_by(team) %>% summarise(avg_pts = mean(pts, na.rm=TRUE))
```
