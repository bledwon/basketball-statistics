# Chapter 4 — SQL (Exercises)

Assumes tables: `player_game` (pg), `player` (p), `team` (t), `game` (g).

## 4.1 Player‑game summary for Central division
```sql
SELECT
  g.date,
  p.name,
  pg.fgm,
  pg.fga,
  pg.pts AS points
FROM player_game pg
JOIN player p ON pg.player_id = p.player_id
JOIN team t ON pg.team_id = t.team_id
JOIN game g ON pg.game_id = g.game_id
WHERE t.division = 'Central';
```

## 4.2 Use first/last name and table aliases
```sql
SELECT
  g.date,
  p.first AS first_name,
  p.last  AS last_name,
  pg.fgm,
  pg.fga,
  pg.pts AS points
FROM player_game AS pg
JOIN player AS p ON pg.player_id = p.player_id
JOIN team   AS t ON pg.team_id = t.team_id
JOIN game   AS g ON pg.game_id = g.game_id
WHERE t.division = 'Central';
```
