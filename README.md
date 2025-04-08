# PROJECT 4: MARKET STRATEGY
#### Written by: Chi Vo
#### Date: April 08, 2025
This is a class project from CECS 427 at California State University Long Beach, instructed by Dr. Oscar Morales Ponce.


### Objective
Create bipartite graphs in the "networkx" library that follow the market-clearing algorithm, using Python.

### How to run the code?
Run the following command on Windows terminal: `python ./market_strategy.py market.gml --plot --interactive`.


#### `--plot`

This parameter will print out the final illustration of the preferred-seller graph using market-clearing algorithm, with seller nodes on the left and buyer nodes on the right, and the red edges indicate the perfect matching from each seller to its buyer. 

#### `--interactive`

This parameter will illustrate each round of the preferred-seller graph, from the beginning to the final stage, including updated prices and layoffs for each round. The red edges, in this case, are the edges with the highest layoff from the seller to their potential buyers. 
