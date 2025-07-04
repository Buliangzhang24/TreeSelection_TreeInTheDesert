from rasterstats import zonal_stats
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import fiona
from shapely.geometry import shape

# === 输入文件路径 ===
zone_path = "D:/E_Internship/3_Specie_Selection/Tarfaya/StudyArea.shp"
raster_path = "D:/E_Internship/3_Specie_Selection/Tarfaya/L2A_NDSI.tiff"

# === 数据分析 ===
with rasterio.open(raster_path) as src:
    actual_nodata = src.nodata if src.nodata is not None else -999

stats = zonal_stats(zone_path, raster_path, stats=["mean"], nodata=actual_nodata)
mean_moisture = stats[0]['mean']

with rasterio.open(raster_path) as src:
    moisture = src.read(1).astype(float)
    moisture[moisture == src.nodata] = np.nan
    max_moisture = np.nanmax(moisture)
    min_moisture = np.nanmin(moisture)

normalized_moisture = (mean_moisture - min_moisture) / (max_moisture - min_moisture)
weighted_drought = (1 - normalized_moisture) * 0.3

# === 可视化 ===
plt.figure(figsize=(12, 8))

# 创建自定义颜色条 (蓝色表示湿润，棕色表示干旱)
cmap = LinearSegmentedColormap.from_list('moisture', ['#8B4513', '#FFFF00', '#006400'])

with rasterio.open(raster_path) as src:
    # 显示湿度数据
    img = plt.imshow(src.read(1), cmap=cmap,
                     vmin=min_moisture, vmax=max_moisture)

    # 添加研究区域边界
    with fiona.open(zone_path, "r") as shapefile:
        for feature in shapefile:
            geom = shape(feature["geometry"])
            x, y = geom.exterior.xy
            plt.plot(x, y, 'r-', linewidth=2, label='Study Area')

# 添加颜色条
cbar = plt.colorbar(img, shrink=0.6)
cbar.set_label('Moisture Index', rotation=270, labelpad=15)

# 添加标题和文本
plt.title(f"Moisture Distribution\nMean: {mean_moisture:.2f} (Drought Index: {weighted_drought:.2f})")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()

# === 保存图表 ===
output_path = "D:/E_Internship/3_Specie_Selection/Tarfaya/Moisture_Analysis.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\n图表已保存至: {output_path}")

# === 显示图表 ===
plt.tight_layout()
plt.show()

# === 控制台输出 ===
print(f"\n分析结果:")
print(f"平均湿度指数: {mean_moisture:.4f}")
print(f"最小值 (最干旱): {min_moisture:.4f}, 最大值 (最湿润): {max_moisture:.4f}")
print(f"加权干旱指数 = {weighted_drought:.4f}")