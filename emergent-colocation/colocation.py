import pandas as pd
import geopandas as gpd

from emergent import colocate_emergent
from utils import plot_emergent, emergent_to_gif
from relations import get_relation

def emergent(data, new_events, position_column, class_column, id_column, time_column, time_freq=None, old_events=None, theta=0.6, alpha=0.5,
            relation='meter', threshold=100, plot=False, shape_file=None, out_plot=None, out_csv=None, gif=False):
    """
    Find prevalent Spatio-Temporal Relations.
    Args:
        data(pandas.DataFrame):
            Full dataset with class labels, ids, and locations for each event.
        old_events(pandas.DataFrame):
            Base data to compare new events to. May be None.
        new_events(pandas.DataFrame):
            New events with some time label to group by.
        position_column(string):
            The DataFrame column with positions. This should be a geometry column in a 
            GeoDataFrame if relation is not a user-defined function.
        class_column(string):
            The DataFrame column with feature classes.
        id_column(string):
            The DataFrame column with feature ids.
        time_column(string):
            The DataFrame column with time labels to group new_events by.
        time_freq(string):
            A frequency string to pass to pandas.Grouper(). Specifies the length of time groups.
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
        gif(bool):
            If True, a gif with the progression of the colocation plots will be saved in
            out_csv.

    Returns:
        T: A dictionary of pandas DataFrames with prevalent colocations, one for each time step indexed by time
        R: A list of CascadeRule objects (A => B, Cascade Participation Index: cpi)
    """
    relation = get_relation(relation)
    grouper = pd.Grouper(key='time', freq=time_freq)

    if old_events is not None:
        old_events = old_events.rename(columns={class_column:'old_cat',id_column:'old_id',position_column:'old_pos'})
        old_events = old_events[['old_cat','old_id','old_pos']]
    else:
        old_events = pd.DataFrame(columns=['old_cat','old_id','old_pos'])

    new_events = new_events.rename(columns={time_column:'time',class_column:'new_cat',id_column:'new_id',position_column:'new_pos'})
    new_events = new_events[['time','new_cat','new_id','new_pos']]

    T,R = colocate_emergent(old_events, new_events, grouper, theta, alpha, relation, threshold)
    
    if out_plot:
        for time in T:
            plot = plot_emergent(gpd.GeoDataFrame(data, geometry=position_column), T[time], class_column, id_column, time, shape_file, out_plot)
            plot.close()

        # add one more file that is a copy of the last with a different title
        plot = plot_emergent(gpd.GeoDataFrame(data, geometry=position_column), T[time], class_column, id_column, 'All Emergent Colocations', shape_file, out_plot)
        plot.close()
        if gif:
            emergent_to_gif(out_plot)
    if plot:
        last_plot = plot_emergent(gpd.GeoDataFrame(data, geometry=position_column), T[list(T.keys())[-1]], class_column, id_column, time, shape_file, out_plot)
        last_plot.show()
    if out_csv:
        for time in T:
            T[time].to_csv(out_csv+'/'+str(time)+'.csv', index=False)

    return T,R