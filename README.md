# Game Content Design: Map Generation
* How to run the code
`python RPGGame.py`
* Fitness function:
1. River Connectivity:
Rivers ("1") should be connected. A river tile with fewer than one adjacent river results in a fitness penalty of -1000, while two adjacent rivers incur -500, and three adjacent rivers incur -100. This encourages continuous and branching rivers.
2. Resource Proximity:
Rice fields ("5") need to be near rivers for irrigation. If a rice field has fewer than two adjacent river tiles, the fitness score is reduced by -1000.
Houses ("6") should be located near rivers. If a house has fewer than two adjacent river tiles, the fitness is reduced by -10,000. However, if it has more than two adjacent river tiles, a bonus of +10,000 is given to encourage riverfront properties.
3. Riverstone Count:
Riverstone tiles ("4") are counted but not explicitly penalized unless they contribute to excessive river coverage.
4. River Overuse Penalty:
If the total number of river-related tiles exceeds 250, a penalty of (river_count - 250) * 1000 is applied to discourage overly water-dominated maps. 
