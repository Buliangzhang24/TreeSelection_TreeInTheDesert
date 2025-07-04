from rasterstats import zonal_stats
import rasterio
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
import fiona
from shapely.geometry import shape
from matplotlib.patches import Patch

# === Data paths ===
zone_path = "D:/E_Internship/3_Specie_Selection/Tarfaya/StudyArea.shp"
raster_path = "D:/E_Internship/3_Specie_Selection/Tarfaya/L2A_NDSI.tiff"

# === Step 1: Mean NDSI inside polygon ===
with rasterio.open(raster_path) as src:
    actual_nodata = src.nodata if src.nodata is not None else -999

stats = zonal_stats(zone_path, raster_path, stats=["mean"], nodata=actual_nodata)
mean_ndsi = stats[0]['mean']

# === Step 2: Max NDSI in full raster ===
with rasterio.open(raster_path) as src:
    ndsi = src.read(1).astype(float)
    ndsi[ndsi == src.nodata] = np.nan
    max_ndsi = np.nanmax(ndsi)

# === Step 3: Weighted Salinity ===
weighted_salinity = (mean_ndsi / max_ndsi) * 0.4

# === Visualization ===
fig, ax = plt.subplots(figsize=(10, 8))

# Plot raster
with rasterio.open(raster_path) as src:
    # Create masked array for clean plotting
    ndsi_ma = np.ma.masked_equal(src.read(1), src.nodata if src.nodata is not None else -999)

    # Plot with colorbar
    raster_plot = show(src, ax=ax, cmap='coolwarm', vmin=np.nanmin(ndsi), vmax=np.nanmax(ndsi))
    cbar = fig.colorbar(raster_plot.get_images()[0], ax=ax, shrink=0.6)
    cbar.set_label('NDSI Value', rotation=270, labelpad=15)

# Plot study area polygon
with fiona.open(zone_path, "r") as shapefile:
    for feature in shapefile:
        geom = shape(feature["geometry"])
        x, y = geom.exterior.xy
        ax.plot(x, y, color='lime', linewidth=2, label='Study Area')

# Add plot elements
ax.set_title(f"NDSI Distribution\n(Mean in Study Area: {mean_ndsi:.2f}, Max: {max_ndsi:.2f})")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Create custom legend
legend_elements = [
    Patch(facecolor='none', edgecolor='lime', linewidth=2, label='Study Area Boundary'),
    Patch(facecolor='none', edgecolor='none', label=f'Weighted Salinity: {weighted_salinity:.4f}')
]
ax.legend(handles=legend_elements, loc='upper right')

# === 在 plt.show() 之前添加这行 ===
output_path = "D:/E_Internship/3_Specie_Selection/Tarfaya/NDSI_Plot.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')  # facecolor确保背景为白色
print(f"\n图表已保存至: {output_path}")

# === 然后才显示图表 ===
plt.tight_layout()
plt.show()

# === Console Output ===
print(f"\nResults:")
print(f"Mean NDSI in polygon: {mean_ndsi:.4f}")
print(f"Max NDSI in region: {max_ndsi:.4f}")
print(f"Weighted Salinity = {weighted_salinity:.4f}")