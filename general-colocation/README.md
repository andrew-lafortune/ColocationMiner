# General Co-location Miner
___
> This repository contains the code for the spatial-colocation package, which implements the main algorithm from:
>
>Shekhar, S., Huang, Y. (2001). Discovering Spatial Co-location Patterns: A Summary of Results. In: Jensen, C.S., Schneider, M., Seeger, B., Tsotras, V.J. (eds) Advances in Spatial and Temporal Databases. SSTD 2001. Lecture Notes in Computer Science, vol 2121. Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-47724-1_13

___
# The Co-location Package

## Installation
```python
pip install general-colocation
```
## Usage

### __Data Pre-Processing__
The input to the `general` function is a pandas DataFrame with, at a minimum, columns for:
1. position: By default, items in this column must be a GeoPandas datatype (Point, Polygon, Line) so that distance calculations may be performed. It may be possible to define a custom spatial relation function that works with other data types, but none are included in the `relations.py` file of the package.
2. class: Labels to separate features by. 
3. id: Unique identifiers for each instance of a class.

### __Optional Configurations__
There are several optional parameters for the `general` function that modify the spatial relation, prevalence, and conditional probability thresholds as well as the format of the output data. See the explanation of key concepts section for more details on terms like prevalence and event-centric conditional probability.

- k: The largest size co-location to find. All co-locations of size k=1,...,k will be returned as items in the output list T.
- theta: The prevalence threshold. Co-locations with a participation index below theta will be pruned from the output.
- alpha: The conditional probability threshold. Association rules with an event-centric conditional probability below alpha will be pruned from the output.
- relation: The spatial relation function to use when determining an item's neighborhood. The relation is a minimum distance in meters by default, but can be changed to a unit distance with the string "unit", or to a custom function by passing a function name to this parameter.
- threshold: The distance threshold for the chosen relation function in the basic cases. Some other type of threshold may be used in user-defined relation functions.
- plot: If True, a scatter plot of all instances of prevalent co-locations will be shown. This only works when using a backend that will produce graphics or in an interactive environment like Jupyter Notebook.
- shape_file: A path to a directory with a shape object to plot co-locations on top of.
- out_plot: A path to a directory in which to store a scatter plot of co-locations for each value k=1,...,k
- out_csv: A path to a directory in which to store a .csv file with one row for each co-location instance of size k

### __General Co-location__
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

### Toy Example
To verify that the code is working correctly, execute the following code snippet:

```python
    d = {'x':[1,2,2,3,4,6],'y':[3,1,5,3,5,1],'class':['solid_sq','empty_ci','empty_ci','solid_ci','dotted_sq','dotted_sq'],'id':[1,1,2,1,1,2]}
    data = pd.DataFrame(data=d)
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