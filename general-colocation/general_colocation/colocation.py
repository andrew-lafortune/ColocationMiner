import pandas as pd
import geopandas as gpd

from general_colocation.general import colocate
from general_colocation.utils import plot_table_instance
from general_colocation.relations import get_relation

def general(data, position_column, class_column, id_column, k=3, theta=0.6, alpha=0.5, 
            relation='meter', threshold=100, plot=False, shape_file=None, out_plot=None, out_csv=None):
    """
    Find prevalent k-itemsets of features satisfying a defined minimum participation 
    index and spatial relationship. Configurable to show plots of prevalent colocations
    and to store intermediate results as csv files. Returns a set of association rules.
    Args:
        data(pandas.DataFrame):
            Ratings or other data you wish to partition.
        position_column(string):
            The DataFrame column with positions. This should be a geometry column in a 
            GeoDataFrame if relation is not a user-defined function.
        class_column(string):
            The DataFrame column with feature classes.
        id_column(string):
            The DataFrame column with feature ids.
        k(int):
            The largest set size to consider. All sets in range [1,k] will be produced.
        theta(float):
            The minimum participation index for prevalent colocations.
        alpha(float):
            The minimum conditional probability threshold for association rules. 
        relation(str or function):
            'meter' and 'unit' are predefined string options, other strings supplied will default to 
            'meter'. 
            If function, should take in two series of positions and a threshold and return a boolean 
            series where True values indicate a spatial relation.
        threshold(int or float):
            The relation threshold passed to the relation function.
        plot(bool):
            default False. If True, a plot of all prevalent k-colocations will be 
            displayed after computation.
        shape_file(string or None):
            If specified, should be a path to a shape (.shp) file in a directory
            with other necessary files (.cpd, .dbf, .prj, .shx) to be drawn behind
            colocation points
        out_plot(string or None):
            If specified, .png files with colocation plots 
            for each k value will be stored here.
        out_csv(string or None):
            If specified, table instances of prevalent colocations for each
            k value will be stored here and accessed for computing k+1 colocations. For
            large datasets or large k values this option will help memory management.

    Returns:
        T: A list of pandas DataFrames with prevalent colocations, one for each k value 1,...,k
        R: A list of Rule objects (e.g. {A,B} => C (prevalence, conditional probability))
    """
    relation = get_relation(relation)

    # T is the table instance for k-colocations, R is the set of all colocation rules for k=1,...,k
    T,R = colocate(data, position_column, class_column, id_column, k, theta, alpha, relation, threshold)
    
    if out_plot:
        for i in range(len(T)):
            plot = plot_table_instance(gpd.GeoDataFrame(data, geometry=position_column), T, class_column, id_column, shape_file, out_plot, k=i+1)
            plot.close()
    if plot:
        last_plot = plot_table_instance(gpd.GeoDataFrame(data, geometry=position_column), T, class_column, id_column, shape_file, out_plot, k=len(T))
        last_plot.show(block=True)
    if out_csv:
        T[-1].drop(columns=['pos'+str(k)]).to_csv(out_csv+'/k'+str(k)+'.csv', index=False)

    return T,R

def main():
    d = {'x':[1,2,2,3,4,6],'y':[3,1,5,3,5,1],'class':['solid_sq','empty_ci','empty_ci','solid_ci','dotted_sq','dotted_sq'],'id':[1,1,2,1,1,2]}
    data = pd.DataFrame(data=d)
    data['pos'] = gpd.points_from_xy(data.x,data.y)

    T,R = general(data, 'pos','class','id',relation='unit',threshold=2.3)

    print('\n',T[-1],'\n')
    
    for r in R:
        print(r)

if __name__ == '__main__':
    main()