# utils.py

import numpy as np
import matplotlib.patches as patches

def add_north_arrow(ax, x=0.92, y=0.92, size=0.02):
    directions = ['N', 'E', 'S', 'W']
    angles = [0, 90, 180, 270]
    positions = [(0, 1.2), (1.2, 0), (0, -1.2), (-1.2, 0)]
    center_x, center_y = ax.transAxes.transform((x, y))
    inv = ax.transData.inverted()
    cx, cy = inv.transform((center_x, center_y))

    for angle in angles:
        theta = np.radians(angle)
        dx, dy = np.cos(theta) * size, np.sin(theta) * size
        triangle = patches.Polygon(
            [[cx, cy], [cx + dx, cy + dy], [cx - dx, cy - dy]],
            closed=True,
            edgecolor='black',
            facecolor='black' if angle % 180 == 0 else 'white',
            transform=ax.transData,
            zorder=5
        )
        ax.add_patch(triangle)

    for direction, (dx, dy) in zip(directions, positions):
        tx = cx + dx * size
        ty = cy + dy * size
        ax.text(tx, ty, direction, fontsize=10, fontweight='bold', ha='center', va='center', zorder=6)

def add_scale_bar(ax, length_km=10, location=(0.034, 0.09)):
    deg_per_km_lon = 1 / (111.32 * np.cos(np.radians(41.88)))
    deg_per_km_lat = 1 / 111.32
    length_deg = length_km * deg_per_km_lon
    height_deg = 0.3 * deg_per_km_lat

    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    x_start = xlim[0] + (xlim[1] - xlim[0]) * location[0]
    y_start = ylim[0] + (ylim[1] - ylim[0]) * location[1]

    rect1 = patches.Rectangle((x_start, y_start), length_deg / 2, height_deg,
                              edgecolor='black', facecolor='black', zorder=10)
    ax.add_patch(rect1)

    rect2 = patches.Rectangle((x_start + length_deg / 2, y_start), length_deg / 2, height_deg,
                              edgecolor='black', facecolor='lightgray', zorder=10)
    ax.add_patch(rect2)

    ax.text(x_start + length_deg / 2, y_start + height_deg * 1.5, f"{length_km} km",
            fontsize=10, ha='center', fontweight='bold', color='black', zorder=11)
