# Chapter 7 — Modeling (Exercises)

Below are code‑first solutions using **Python (pandas/statsmodels)**, with **R equivalents** where helpful. Replace file paths as needed.

## 7.1 OLS model on shot makes
```python
import pandas as pd
import statsmodels.formula.api as smf

# df from 07_01_ols.py
# df['dist_sq'] = df['dist']**2
# df['made'] = df['made'].astype(int)

# (a) apply function to get predicted probs

def prob_of_make(row):
    return 1 / (1 + (row['dist'] / 10))  # placeholder; use your actual function


df['make_hat_alt'] = df.apply(prob_of_make, axis=1)
# compare
# df[['make_hat_alt']].head(), results.predict(df).head()

# (b) add shot value indicator
model = smf.ols('made ~ dist + dist_sq + C(value)', data=df).fit()
# interpret coefficient on C(value)[T.3] vs baseline (2)

# (c) manual dummy
# df['is_three'] = (df['value'] == 3).astype(int)
# smf.ols('made ~ dist + dist_sq + is_three', data=df).fit()
```

## 7.2 Coinflip simulation
```python
import numpy as np
import pandas as pd
import statsmodels.api as sm


def run_sim_get_pvalue(n=100):
    flips = np.random.binomial(1, 0.5, n)
    x = np.arange(n)
    X = sm.add_constant(x)
    model = sm.OLS(flips, X).fit()
    return model.pvalues[1]

# (b)
vals = pd.Series([run_sim_get_pvalue() for _ in range(1000)])
vals.mean()

# (c)

def runs_till_threshold(i=1, p=0.05):
    pv = run_sim_get_pvalue()
    return i if pv < p else runs_till_threshold(i+1, p)

runs = pd.Series([runs_till_threshold(1) for _ in range(100)])

# (d)
# Geometric mean = 1/p, median ~ ceil(log(0.5)/log(1-p))
```

## 7.3 Logit model on win/loss
```python
import statsmodels.formula.api as smf

# dftg: team-game data
# target = (wl == 'W')

dftg['win'] = (dftg['wl'] == 'W').astype(int)
model = smf.logit('win ~ fg3_pct + oreb + dreb + stl + tov + blk', data=dftg).fit()

# compare marginal effects of stl vs tov
```

### R equivalent
```r
model <- glm(win ~ fg3_pct + oreb + dreb + stl + tov + blk,
             data=dftg, family=binomial())
summary(model)
```

## 7.4 Random forest classification
```python
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

# target: team; features: stats (exclude identifiers like team_id, game_id, date)
X = dftg.drop(columns=['team','team_id','game_id','date','wl'])
y = dftg['team']

rf = RandomForestClassifier(n_estimators=300, random_state=42)
cv_scores = cross_val_score(rf, X, y, cv=5)

# Fit to inspect feature importances
rf.fit(X, y)
importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
```

### R equivalent
```r
library(randomForest)

X <- dftg %>% select(-team, -team_id, -game_id, -date, -wl)
rf <- randomForest(x=X, y=as.factor(dftg$team))
importance(rf)
```

**Notes:**
- Exclude identifiers (team_id, game_id, date) from modeling features.
- Random guessing accuracy ≈ 1 / number_of_teams.
