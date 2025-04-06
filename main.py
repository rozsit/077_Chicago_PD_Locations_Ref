# main.py

from py_components.config import NEIGHBORHOOD_SHP, STREET_CSV, OUTPUT_IMAGE
from py_components.data_loader import DataLoader
from py_components.map_plotter import MapPlotter

def main():
    loader = DataLoader(NEIGHBORHOOD_SHP, STREET_CSV)
    neighborhoods = loader.load_neighborhoods()
    street_gdf, street_df = loader.load_street_data()

    plotter = MapPlotter(neighborhoods, street_gdf, street_df)
    plotter.plot(OUTPUT_IMAGE)
    print(f"Map saved to {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
