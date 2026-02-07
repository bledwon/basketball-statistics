#!/usr/bin/env python3
"""Runnable Chapter 7 modeling exercises (OLS, logit, random forest).
"""
from os import path, getenv
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

DATA_DIR = getenv('DATA_DIR', '/Users/benledwon/Desktop/LearnPythonBB/code-basketball-files-main/data')

# 7.1 OLS: probability of make
shots = pd.read_csv(path.join(DATA_DIR, 'shots.csv'))
shots['dist_sq'] = shots['dist']**2
shots['made'] = shots['made'].astype(int)

ols = smf.ols('made ~ dist + dist_sq + C(value)', data=shots).fit()
print('OLS summary (truncated):')
print(ols.params.head())

# 7.2 Coinflip sim
import statsmodels.api as sm

def run_sim_get_pvalue(n=100):
    flips = np.random.binomial(1, 0.5, n)
    x = np.arange(n)
    X = sm.add_constant(x)
    model = sm.OLS(flips, X).fit()
    return model.pvalues[1]

vals = pd.Series([run_sim_get_pvalue() for _ in range(1000)])
print('Avg p-value:', round(vals.mean(), 4))

# 7.3 Logit win/loss
team_games = pd.read_csv(path.join(DATA_DIR, 'team_games.csv'))
team_games['win'] = (team_games['wl'] == 'W').astype(int)

logit = smf.logit('win ~ fg3_pct + oreb + dreb + stl + tov + blk', data=team_games).fit(disp=False)
print('Logit params:')
print(logit.params)

# 7.4 Random forest team prediction
# use numeric features only and remove identifiers
num_cols = team_games.select_dtypes(include='number').columns
drop_cols = {'team_id','game_id','season'}
X = team_games[num_cols.drop([c for c in num_cols if c in drop_cols])]
y = team_games['team']

rf = RandomForestClassifier(n_estimators=200, random_state=42)
cv_scores = cross_val_score(rf, X, y, cv=5)
print('RF CV accuracy:', round(cv_scores.mean(), 4), 'range', (round(cv_scores.min(),4), round(cv_scores.max(),4)))

rf.fit(X, y)
importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print('Top features:', importances.head(10))
