import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import imageio
import os

def adjust_bounds(bounds):
    xmin, ymin, xmax, ymax = bounds
    plot_ratio = 1.5
    margins = 1.1

    height = ymax - ymin
    width = xmax - xmin

    opt_height = max(height, width / plot_ratio)
    opt_width  = max(width , height*plot_ratio)

    # If plot is too narrow, increase xmin. If plot is too wide, increase ylim

    if opt_height > height :
        ymid = (ymax + ymin)/2
        mid_height = opt_height * margins / 2
        ymin = ymid - mid_height
        ymax = ymid + mid_height
    if opt_width > width:
        xmid = (xmin + xmax)/2
        mid_width = opt_width* margins/2
        xmin = xmid - mid_width
        xmax = xmid + mid_width
    return xmin, ymin, xmax, ymax

def plot_emergent(E, T, class_column, id_column, title, shape_file, out=None):
    ids = pd.unique(T[['new_id','old_id']].values.ravel('K'))
    to_plot = E[E[id_column].isin(ids)]

    fig, ax = plt.subplots(figsize=(50,10))

    if(shape_file):
        shape = gpd.read_file(shape_file)
        shape.set_crs(crs='EPSG:4326')
        bounds = shape.geometry.total_bounds
        shape.plot(ax=ax, color = 'grey', alpha=0.5)
        
    else:
        bounds = to_plot.geometry.total_bounds

    xmin, ymin, xmax, ymax = adjust_bounds(bounds)

    if len(to_plot) == 0:
        to_plot = E.head(1)
        to_plot = to_plot.set_geometry([Point(0,ymin-50)])
        empty_message = 'No Colocations for This Date'
        to_plot.loc[:,class_column] = empty_message +' ' * E[class_column].map(len).max()

    to_plot.plot(class_column, ax=ax, legend=True, legend_kwds={'title':'Categories','loc':'center left', 'bbox_to_anchor':(1.0,0.5)})
    
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    plt.title(title)
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)

    if out is not None:
        plt.savefig(out+'/'+str(title)+'.png', bbox_inches='tight')

    return plt

def emergent_to_gif(png_dir):
    frames_per_plot = 10
    files = []
    for (_,_, filenames) in os.walk(png_dir):
        files.extend(filenames)
    files.sort()
    with imageio.get_writer(png_dir+'/emergent_gif.gif', mode='i') as writer:
        for plot in files:
            image = imageio.imread(png_dir+'/'+plot)

            for _ in range(frames_per_plot):
                writer.append_data(image)