# General Colocation Miner
___
> This repository contains the code for the colocation package, which 
> primarily implements the main algorithm from ***Discovering Colocation Patterns from Spatial Datasets: A General Approach*** by Huang et al.(2004). 
___
# The Colocation Package
Would it be useful to export the source code as a PyPi package?
## Installation
```python
pip install spatial-colocation
```
## Usage

### General Colocation
```python
T,R = colocation.general(data, position_column, class_column, id_column, k=3, theta=0.6, alpha=0.5, 
                        relation='meter', threshold=100, plot=False, shape_file=None, out_plot=None, out_csv=None):
```

Configurable to: 
- show a plot of all k-colocations with a participation index of theta or higher
- store the plot of each set of co-locations for k=1,...,k as a .png file
- store the items in the set of prevalent k-colocations as a .csv file

Returns:
- a list of DataFrames T, one for each k=1,...,k
- the set of association rules R with conditional probability of alpha or higher

### Emergent Colocation
```python
T,R = emergent(data, new_events, position_column, class_column, id_column, time_column, time_freq=None, old_events=None, theta=0.6, alpha=0.5,
               relation='meter', threshold=100, plot=False, shape_file=None, out_plot=None, out_csv=None, gif=False)
```

Configurable to:
- find prevalent colocations of new events with existing events across a series of time steps 
- show the final plot of all time steps together in a single plot
- store the plot of prevalent colocations each time step as a .csv file
- write the plots of all separate time steps together as a .gif file in time order

Returns:
- a dictionary of DataFrames T, the colocations with participation index greater than theta for each time step indexed by time
- the set of association rules R with conditional probability of alpha or higher for the final set of prevalent colocations in T

Assumes new_locations has a date column

### Toy Example
To verify that the code is working correctly, execute the following code snippet:

```python
    data = pd.read_csv('data/toy_data.txt')
    data['pos'] = gpd.points_from_xy(data.x,data.y)

    T,R = general(data, 'pos','class','id',relation='unit',threshold=2.3)

    
    print('\n',T[-1],'\n')
    
    for r in R:
        print(r)
```

By running the command:
```
    python3 colocation.py
```

The terminal output should look something like this (timing may vary slightly):
```
    |C1| = 4, |P1| = 4, |R1| = 0, Rows in T1 = 6, Elapsed Time: 0:00:00.002245
    |C2| = 6, |P2| = 3, |R2| = 6, Rows in T2 = 7, Elapsed Time: 0:00:00.028943
    |C3| = 1, |P3| = 1, |R3| = 3, Rows in T3 = 2, Elapsed Time: 0:00:00.046490

            cat1  id1      cat2  id2      cat3  id3                     pos3
    1  empty_ci    1  solid_ci    1  solid_sq    1  POINT (1.00000 3.00000)
    5  empty_ci    2  solid_ci    1  solid_sq    1  POINT (1.00000 3.00000) 

    {solid_sq} => empty_ci (1.0, 1.0)
    {empty_ci} => solid_sq (1.0, 1.0)
    {empty_ci} => solid_ci (1.0, 1.0)
    {solid_sq} => solid_ci (1.0, 1.0)
    {empty_ci, solid_sq} => solid_ci (1.0, 1.0)
    {solid_ci} => empty_ci (1.0, 1.0)
    {empty_ci, solid_ci} => solid_sq (1.0, 1.0)
    {solid_ci, solid_sq} => empty_ci (1.0, 1.0)
    {solid_ci} => solid_sq (1.0, 1.0)
```