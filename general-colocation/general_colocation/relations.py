import numpy as np
import geopandas as gpd

def meters_to_dist(m):
    return m * 25e-6

def is_spatial_relation_dist_unit(col1,col2,thold):
    col1 = gpd.GeoSeries(col1)
    col2 = gpd.GeoSeries(col2)
    return col1.distance(col2) < thold

def is_spatial_relation_dist_m(col1,col2, thold):
    thold = meters_to_dist(thold)
    s1 = gpd.GeoSeries(col1, crs="EPSG:3857")
    s2 = gpd.GeoSeries(col2, crs="EPSG:3857")
    return s1.distance(s2) < thold

def get_relation(relation):
    if(relation == 'meter'):
            relation = is_spatial_relation_dist_m
    elif(relation == 'unit'):
        relation = is_spatial_relation_dist_unit
    else:
        if not callable(relation):
            relation = is_spatial_relation_dist_unit
    return relation
