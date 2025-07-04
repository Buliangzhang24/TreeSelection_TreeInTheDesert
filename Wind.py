import xarray as xr
import geopandas as gpd
import rioxarray
from rasterio import features
import numpy as np

# === 1. 加载研究区域矢量 ===
study_area = gpd.read_file("D:/E_Internship/3_Specie_Selection/Tarfaya/StudyArea.shp")

# === 2. 加载NetCDF风速数据并裁剪 ===
ds = xr.open_dataset("D:/E_Internship/3_Specie_Selection/Tarfaya/era5_monthly_wind_gust.nc")

# 首先检查文件中可用的变量名
print("文件中包含的变量:", list(ds.data_vars.keys()))

# 根据输出结果选择正确的变量名（可能是'i10fg'或其他）
# 修改此行，使用正确的变量名
wind_gust = ds['i10fg']  # 使用错误信息中显示的'i10fg'变量

# 将NetCDF数据转换为地理坐标系（假设ERA5为WGS84）
wind_gust.rio.write_crs("EPSG:4326", inplace=True)

# 确保研究区域的CRS与数据一致
study_area = study_area.to_crs("EPSG:4326")

# 用shp裁剪区域内的风速数据
try:
    clipped_gust = wind_gust.rio.clip(study_area.geometry, study_area.crs, drop=True)
except Exception as e:
    print(f"裁剪时出错: {e}")
    # 如果裁剪失败，尝试使用所有数据
    clipped_gust = wind_gust

# === 3. 计算区域最大阵风（所有时间+空间） ===
max_regional_gust = clipped_gust.max().values

# === 4. 计算Weighted Wind Erosion（区域内逐网格点） ===
weighted_erosion = (clipped_gust / max_regional_gust) * 0.2 # 20%权重

# === 5. 输出结果 ===
print(f"研究区域最大阵风（m/s）: {max_regional_gust:.2f}")
print(f"权重风化指数示例（第一个月）:\n{weighted_erosion[0].values}")
