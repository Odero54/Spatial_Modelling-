import os
import numpy as np
import pandas as pd
import geopandas as gpd
import rioxarray as rx
from multiprocessing import Pool, cpu_count
from shapely.ops import unary_union

def union(x):
    return unary_union(x)

if __name__ == "__main__":
    print("Reading Rasters...")
    rasterPath = "C:/Users/Dell/OneDrive/Desktop/urban-green-spaces/Population/karura-neighborhood.tif"
    raster = rx.open_rasterio(rasterPath)
    x, y, population = raster.x.values, raster.y.values, raster.values
    x, y = np.meshgrid(x,y)
    x, y, population = x.flatten(), y.flatten(), population.flatten()

    print("Converting to GeoDataFrame...")
    population_pd = pd.DataFrame.from_dict({'population': population, 'x': x, 'y': y})
    population_threshold = 5
    population_pd = population_pd[population_pd['population'] > population_threshold]
    population_vector = gpd.GeoDataFrame(geometry=gpd.GeoSeries.from_xy(population_pd['x'], population_pd['y'], crs=raster.rio.crs))
    population_vector = population_vector.buffer(250, cap_style=3)
    population_vector = population_vector.to_crs('EPSG:4326')
    geom_arr = []

    # Convert GeoSeries to list of geometries
    geoms = list(population_vector)

    # Converting geometries list to nested list of geometries
    for i in range(0, len(geoms), 10000):
        geom_arr.append(geoms[i:i+10000])

    # Creating multiprocessing pool to perform union operation of chunks of geometries
    with Pool(cpu_count()) as p:
        geom_union = p.map(union, geom_arr)

    # Perform union operation on rturned unioned geometries
    total_union = unary_union(geom_union)

    # Creating GeoDataFrame for total_union
    union_vector_gdf = gpd.GeoDataFrame(geometry=gpd.GeoSeries(total_union))

    # Saving GeoDataFrame to Shapefile
    filePath = "C:/Users/Dell/OneDrive/Desktop/urban-green-spaces/Population"
    out_file = os.path.join(filePath, 'population_1000.shp')
    union_vector_gdf.to_file(out_file, crs='EPSG:4326')