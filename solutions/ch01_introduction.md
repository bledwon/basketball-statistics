# Chapter 1 — Introduction (Exercises)

Below are concise answers and explanations. I paraphrased the prompts and provide direct solutions.

## 1.1 Granularity (what each row represents)
- **a)** Player–game (and quarter) level. Each row is one player’s shots in a specific game/quarter.
- **b)** Team level (static team attributes).
- **c)** Team–game level (team performance in a specific game).
- **d)** Shot‑type level (aggregated by shot type).
- **e)** Jersey‑number level (aggregated by jersey number).

## 1.2 Modeling inputs/outputs
- **Inputs:** combined shooting % over last 5 games; total number of shots over last 5 games.
- **Output:** team points scored in a game (next game or same reference window).
- **Granularity:** team–game.
- **Main limitation:** ignores opponent strength/defense, pace, injuries, home/away, and other context.

## 1.3 Pipeline stage mapping
- **a)** Manipulating data (changing granularity)
- **b)** Analyzing data (modeling/insight generation)
- **c)** Manipulating data (handling missing values)
- **d)** Loading data (SQL in the pipeline)
- **e)** Collecting data (scraping)
