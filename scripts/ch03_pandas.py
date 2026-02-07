#!/usr/bin/env python3
"""Runnable Chapter 3 (Pandas) exercises.

Usage:
  DATA_DIR=/path/to/data python3 scripts/ch03_pandas.py
"""
from os import path, getenv
import pandas as pd

DATA_DIR = getenv('DATA_DIR', '/Users/benledwon/Desktop/LearnPythonBB/code-basketball-files-main/data')

# 3.0
print('Loading games.csv')
games = pd.read_csv(path.join(DATA_DIR, 'games.csv'))

games['date'] = pd.to_datetime(games['date'])
game50 = games.sort_values('date').head(50)
print('game50 shape:', game50.shape)

games_sorted = games.sort_values('home_pts', ascending=False)
print('Top home_pts:', games_sorted[['home','away','home_pts']].head(3))

cols = ['date','home','away','home_pts','away_pts']
game_simple = games[cols].copy()

game_simple = game_simple[['home','away','date','home_pts','away_pts']]

game_simple['game_id'] = games['game_id']

game_simple.to_csv(path.join(DATA_DIR, 'game_simple.txt'), sep='|', index=False)
print('Wrote game_simple.txt')

# 3.1
pg = pd.read_csv(path.join(DATA_DIR, 'player_game.csv'))

pg['net_takeaways'] = pg['stl'] - pg['tov']
pos_col = 'position' if 'position' in pg.columns else 'pos'
pg['player_desc'] = pg['name'] + ' is the ' + pg['team'] + ' ' + pg[pos_col]
pg['bad_game'] = (pg['fga'] > 20) & (pg['pts'] < 15)
pg['len_last_name'] = pg['name'].str.split().str[-1].str.len()
pg['game_id'] = pg['game_id'].astype(str)

# underscore swap
pg.columns = [c.replace('_', ' ') for c in pg.columns]
pg.columns = [c.replace(' ', '_') for c in pg.columns]

pg['oreb_percentage'] = pg['oreb'] / pg['reb']
pg['oreb_percentage'] = pg['oreb_percentage'].fillna(-99)
pg = pg.drop(columns=['oreb_percentage'])

# 3.2
pg = pd.read_csv(path.join(DATA_DIR, 'player_game.csv'))
pg['total_shots1'] = pg['fga'] + pg['fta']
pg['total_shots2'] = pg[['fga','fta']].sum(axis=1)

print('Means:', pg[['pts','fga','reb']].mean().to_dict())

n_40_10 = pg[(pg['pts'] >= 40) & (pg['reb'] >= 10)].shape[0]

pct_40_10 = n_40_10 / pg[pg['pts'] >= 40].shape[0]
print('40pt/10reb count:', n_40_10, 'pct:', round(pct_40_10,3))

print('Total 3PA:', pg['fg3a'].sum())

team_counts = pg['team'].value_counts()
print('Most team:', team_counts.idxmax(), 'Least team:', team_counts.idxmin())

# 3.3
print('Loading team_games.csv')
dftg = pd.read_csv(path.join(DATA_DIR, 'team_games.csv'))

cols = ['team','date','pts','fgm','fga']
chi = dftg.loc[dftg['team'] == 'CHI', cols]
chi2 = dftg.query("team == 'CHI'")[cols]

no_chi = dftg.loc[dftg['team'] != 'CHI', cols]

fg_dup = dftg.duplicated(subset=['fgm','fga','fg3m','fg3a'], keep=False)
dftg_fg_dup = dftg[fg_dup]
dftg_fg_no_dup = dftg[~fg_dup]

pct3 = dftg['fg3m'] / dftg['fg3a']

dftg['three_pt_desc'] = pd.NA
dftg.loc[pct3 > 0.50, 'three_pt_desc'] = 'great'
dftg.loc[pct3 <= 0.25, 'three_pt_desc'] = 'brutal'

no_desc1 = dftg.loc[dftg['three_pt_desc'].isna()]
no_desc2 = dftg.query('three_pt_desc.isna()')

# 3.4
team_avg_pts = dftg.groupby('team')['pts'].mean()

pct_100 = dftg.assign(ge100 = dftg['pts'] >= 100).groupby('team')['ge100'].mean()

teams_150 = dftg.groupby('team')['pts'].max().loc[lambda s: s >= 150]

counts = dftg.groupby('date')['team_id'].count()
sums = dftg.groupby('date')['team_id'].sum()

agg = dftg.groupby(['team_id','wl']).agg(
    ave_pts=('pts','mean'),
    ave_fgm=('fgm','mean'),
    ave_fga=('fga','mean'),
    ave_fg3m=('fg3m','mean'),
    ave_fg3a=('fg3a','mean'),
    n=('wl','count')
).reset_index()

loss_high = agg[(agg['wl'] == 'L') & (agg['ave_pts'] > 110)]

# 3.5 combine
pts = pd.read_csv(path.join(DATA_DIR, 'problems/combine1/pts.csv'))
reb = pd.read_csv(path.join(DATA_DIR, 'problems/combine1/reb.csv'))
defense = pd.read_csv(path.join(DATA_DIR, 'problems/combine1/def.csv'))

merge1 = pts.merge(reb, on='player_id', how='outer').merge(defense, on='player_id', how='outer')
merge1 = merge1.fillna(0)

# ensure unique index for concat by aggregating duplicates
pts_g = pts.groupby('player_id', as_index=False).sum(numeric_only=True)
reb_g = reb.groupby('player_id', as_index=False).sum(numeric_only=True)
def_g = defense.groupby('player_id', as_index=False).sum(numeric_only=True)

pts_i = pts_g.set_index('player_id')
reb_i = reb_g.set_index('player_id')
def_i = def_g.set_index('player_id')
concat1 = pd.concat([pts_i, reb_i, def_i], axis=1).fillna(0).reset_index()

parts = [pd.read_csv(path.join(DATA_DIR, 'problems/combine2', f)) for f in ['guard.csv','forward.csv','center.csv']]
combined = pd.concat(parts, axis=0).reset_index(drop=True)

teams = pd.read_csv(path.join(DATA_DIR, 'teams.csv'))
for conf, df in teams.groupby('conference'):
    df.to_csv(path.join(DATA_DIR, f'teams_{conf}.csv'), index=False)

conf_frames = [pd.read_csv(path.join(DATA_DIR, f'teams_{c}.csv')) for c in ['East','West']]
teams_all = pd.concat(conf_frames, axis=0, ignore_index=True)

print('Chapter 3 script finished.')
