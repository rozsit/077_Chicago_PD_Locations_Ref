# map_plotter.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.lines import Line2D
from py_components.utils import add_north_arrow, add_scale_bar


class MapPlotter:
    def __init__(self, neighborhoods, street_gdf, street_df):
        self.gdf_neighborhoods = neighborhoods
        self.gdf_streets = street_gdf
        self.street_df = street_df
        self.min_size = 20
        self.max_size = 120

    def plot(self, output_path):
        fig, ax = plt.subplots(figsize=(14, 12))
        fig.suptitle("Chicago PD Season 9 Story Locations",
                     fontsize=16, weight='bold')

        self.gdf_neighborhoods.plot(
            ax=ax, edgecolor="black", facecolor="none", linewidth=1, zorder=12)

        for idx, row in self.gdf_neighborhoods.iterrows():
            x, y = row["centroid"].x, row["centroid"].y
            ax.text(x, y, str(row.Neighborhood_ID), fontsize=9,
                    ha="center", va="center", color="blue")

        sns.kdeplot(
            x=self.street_df["Longitude"],
            y=self.street_df["Latitude"],
            weights=self.street_df["Weight"],
            ax=ax,
            cmap="Oranges",
            fill=True,
            alpha=0.6,
            bw_adjust=0.7)

        weights = self.gdf_streets['Weight']
        scaled_sizes = ((weights - weights.min()) / (weights.max() - weights.min()) *
                        (self.max_size - self.min_size)) + self.min_size
        self.gdf_streets.plot(
            ax=ax,
            color="red",
            markersize=scaled_sizes,
            alpha=0.7)

        ax.set_xlim(self.gdf_neighborhoods.total_bounds[[0, 2]])
        ax.set_ylim(self.gdf_neighborhoods.total_bounds[[1, 3]])
        ax.set_axis_on()
        ax.tick_params(labelsize=10)
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

        add_north_arrow(ax)
        add_scale_bar(ax)

        self._add_labels(fig)
        self._add_legend(fig)
        self._add_datasource(fig)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

    def _add_labels(self, fig):
        labels = [f"{row['Neighborhood_ID']} - {row['PRI_NEIGH']}" for _,
                  row in self.gdf_neighborhoods.iterrows()]
        n = len(labels)
        cols = 2
        rows = (n + cols - 1) // cols
        columns = [labels[i * rows:(i + 1) * rows] for i in range(cols)]
        x_positions = [0.85, 0.99]

        fig.text(0.965, 0.86, "Chicago Neighborhoods", fontsize=12,
                 fontstyle='italic', weight='bold', ha='center')
        for i, col in enumerate(columns):
            text_block = "\n".join(col)
            fig.text(x_positions[i], 0.5, text_block,
                     fontsize=10, va='center', ha='left')

    def _add_legend(self, fig):
        weights = self.street_df["Weight"]
        legend_weights = [int(weights.min()), int(weights.max())]
        scaled_sizes = ((np.array(legend_weights) - weights.min()) /
                        (weights.max() - weights.min())) * (self.max_size - self.min_size) + self.min_size
        legend_elements = [
            Line2D([0], [0], marker='o', color='none', label=f'{w} mentions',
                   markerfacecolor='red', markersize=np.sqrt(s), alpha=0.7)
            for w, s in zip(legend_weights, scaled_sizes)]

        fig.legend(handles=legend_elements,
                   title="Locations",
                   loc='center',
                   bbox_to_anchor=(0.24, 0.19),
                   frameon=True,
                   framealpha=0.5,
                   fontsize=8,
                   title_fontsize=9)

    def _add_datasource(self, fig):
        fig.text(0.20, 0.08,
                 "Datasource:\n"
                 "1. Chicago Data Portal: https://data.cityofchicago.org\n"
                 "2. Wikipedia: https://en.wikipedia.org/wiki/Community_areas_in_Chicago\n\n"
                 "©️ Tamas Rozsahegyi",
                 fontsize=6,
                 va='bottom',
                 color='gray',
                 bbox=dict(
                     facecolor='white',
                     alpha=0.5,
                     edgecolor='none'))
