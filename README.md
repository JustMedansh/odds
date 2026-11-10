# A Hunger Games Simulation - ODDS
---
some notes:
each action (and event?) is supposed to return a tuple like this:
`((contestants_participating), time, state)`

## Map viewer

Install the dependencies with `pip install -r requirements.txt`, then launch a
standalone sample map with `python -m src.visualization.map_renderer`. The
renderer reads the existing `WorldMap.tiles` and `WorldMap.positions` data and
does not change simulation state. Terrain colors and contestant names appear
in the window; close it to exit.


