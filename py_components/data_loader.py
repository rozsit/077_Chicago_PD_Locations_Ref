# data_loader.py

import pandas as pd
import geopandas as gpd

class DataLoader:
    def __init__(self, neighborhood_path, street_path):
        self.neighborhood_path = neighborhood_path
        self.street_path = street_path

    def load_neighborhoods(self):
        gdf = gpd.read_file(self.neighborhood_path)
        gdf = gdf.reset_index(drop=True)
        gdf["Neighborhood_ID"] = gdf.index + 1
        gdf = gdf.to_crs(epsg=4326)
        gdf_projected = gdf.to_crs(epsg=26971)
        gdf["centroid"] = gdf_projected.centroid.to_crs(epsg=4326)
        return gdf

    def load_street_data(self):
        df = pd.read_csv(self.street_path).dropna(subset=["Latitude", "Longitude"])
        gdf = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df.Longitude, df.Latitude),
            crs="EPSG:4326")
        return gdf, df
