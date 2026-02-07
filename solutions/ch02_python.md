# Chapter 2 — Python (Exercises)

## 2.1 Valid variable names
Valid: ` _throwaway_data`, `n_shots`, `numOfBoards`, `flagrant2`.
Invalid: `3_pt_percentage` (starts with number), `coach name` (space), `@home_or_away` (symbol), `'ft_attempts'` (quotes).

## 2.2 Final value
```python
# total_points ends at:
133
```

## 2.3 commentary function
```python
def commentary(player, play):
    return f"{player} with the {play}!"
```

## 2.4 islower
`islower()` returns a **boolean** indicating if all cased letters are lowercase.
```python
"abc".islower()        # True
"Abc".islower()        # False
"123".islower()        # False (no cased letters)
```

## 2.5 is_fox (case‑insensitive, handles apostrophe)
```python
def is_fox(name):
    cleaned = name.strip().lower().replace("’", "'")
    return cleaned == "de'aaron fox"
```

## 2.6 is_good_score
```python
def is_good_score(n):
    return f"{n} is a good score" if n >= 100 else f"{n}'s not that good"
```

## 2.7 Print list without 'james harden'
```python
roster = ['kevin durant', 'kyrie irving', 'james harden']

# a) filter
print([p for p in roster if p != 'james harden'])

# b) slice
print(roster[:2])

# c) remove copy
r2 = roster.copy()
r2.remove('james harden')
print(r2)
```

## 2.8 Dict edits
```python
shot_info = {'shooter': 'Steph Curry', 'is_3pt': True, 'went_in': False}
shot_info['shooter'] = 'Devin Booker'

def toggle3(d):
    d = d.copy()
    d['is_3pt'] = not d['is_3pt']
    return d
```

## 2.9 Will it error?
- `shot_info['is_ft']` → **KeyError** (missing key)
- `shot_info[shooter]` → **NameError** (unless `shooter` is a variable)
- `shot_info['distance'] = 23` → **No error** (adds key)

## 2.10 Last names + dict comprehension
```python
roster = ['kevin durant', 'kyrie irving', 'james harden']

# a) loop
for p in roster:
    print(p.split()[-1])

# b) dict of name -> length
name_len = {p: len(p) for p in roster}
```

## 2.11 roster_dict comprehensions
```python
roster_dict = {
    'PF': 'kevin durant',
    'SG': 'kyrie irving',
    'PG': 'james harden',
    'C': 'deandre jordan'
}

positions = [pos for pos in roster_dict.keys()]
last_hj = [p for p in roster_dict.values() if p.split()[-1].startswith(('h','j'))]
```

## 2.12 mapper + lambda
```python
def mapper(lst, fn):
    return [fn(x) for x in lst]

list_of_n_3pt_made = [5, 6, 1, 0, 4, 4]
pts = mapper(list_of_n_3pt_made, lambda x: x * 3)
```
