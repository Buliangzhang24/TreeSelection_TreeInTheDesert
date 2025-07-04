import pandas as pd
import re
from sklearn.preprocessing import MinMaxScaler
# 固定权重
WEIGHTS = {
    'salinity': 0.5330,  # 盐耐受权重
    'drought': 0.4670,  # 干旱耐受权重
    'wind': 0.7578  # 抗风权重
}
ECONOMIC_WEIGHT = 0.1  # 经济价值固定10%


def clean_species_name(name):
    """统一清理物种名称：小写化、移除多余空格和特殊符号"""
    if pd.isna(name):
        return None
    name = str(name).strip().lower()
    name = re.sub(r'\s+/.*', '', name)  # 删除斜杠后的内容
    name = re.sub(r'[^\w\s]', '', name)  # 移除非字母数字字符
    name = re.sub(r'\s+', ' ', name)  # 合并多个空格
    return name


def normalize_scores(df):
    """将Total Score标准化到0-1范围"""
    scaler = MinMaxScaler()
    df['Total_Score_Normalized'] = scaler.fit_transform(df[['Total_Score']])
    return df


def load_tolerance_data(filepath):
    """加载耐受性数据，确保包含Wind Resistance列"""
    try:
        df = pd.read_csv(
            filepath,
            sep=',',  # 如果是制表符分隔则改为'\t'
            header=0,
            usecols=['Species', 'Salt_Tolerance', 'Drought_Tolerance', 'Wind_Resistance'],
            dtype={
                'Species': str,
                'Salt_Tolerance': float,
                'Drought_Tolerance': float,
                'Wind_Resistance': float
            }
        )
        df['Species'] = df['Species'].apply(clean_species_name)
        # 检查必要列是否存在
        if 'Wind_Resistance' not in df.columns:
            raise ValueError("CSV必须包含Wind_Resistance列")
        return df
    except Exception as e:
        raise ValueError(f"读取耐受性数据失败: {str(e)}")


def load_economic_data(filepath):
    """加载经济价值数据"""
    try:
        df = pd.read_csv(
            filepath,
            sep=',',
            header=0,
            names=['Species', 'Economic_Value'],
            dtype={'Species': str, 'Economic_Value': float}
        )
        df['Species'] = df['Species'].apply(clean_species_name)
        return df
    except Exception as e:
        raise ValueError(f"读取经济数据失败: {str(e)}")


def calculate_total_score(row):
    """按最新公式计算综合得分"""
    total_score = (
            (row['Salt_Tolerance'] * WEIGHTS['salinity'] * 0.4) +
            (row['Drought_Tolerance'] * WEIGHTS['drought'] * 0.3) +
            (row['Wind_Resistance'] * WEIGHTS['wind'] * 0.2) +
            (row['Economic_Value'] * ECONOMIC_WEIGHT)
    )
    return round(total_score, 4)


def main():
    # 文件路径（根据实际修改）
    economic_csv = "D:/E_Internship/3_Specie_Selection/Tarfaya/economic_values.csv"
    tolerance_csv = "D:/E_Internship/3_Specie_Selection/Tarfaya/Tolerance1.csv"

    try:
        # 1. 加载数据
        df_tolerance = load_tolerance_data(tolerance_csv)
        df_economic = load_economic_data(economic_csv)

        # 2. 合并数据
        df_merged = pd.merge(
            df_tolerance,
            df_economic,
            on='Species',
            how='left'
        )

        # 3. 处理缺失值
        if df_merged['Economic_Value'].isna().any():
            print("警告：以下树种缺少经济价值数据，已填充默认值1：")
            print(df_merged[df_merged['Economic_Value'].isna()]['Species'].to_string(index=False))
            df_merged['Economic_Value'] = df_merged['Economic_Value'].fillna(1)

        # 4. 计算总分
        # 计算原始总分
        df_merged['Total_Score'] = df_merged.apply(calculate_total_score, axis=1).round(4)

        # 标准化到0-1范围
        df_merged = normalize_scores(df_merged)

        # 按标准化后的分数排序
        df_result = df_merged.sort_values('Total_Score_Normalized', ascending=False)

        # 打印结果（显示标准化后的分数）
        print("TOP 10 树种排名（标准化分数0-1）：")
        print(df_result[['Species', 'Total_Score_Normalized',
                         'Salt_Tolerance', 'Drought_Tolerance',
                         'Wind_Resistance', 'Economic_Value']].head(10).to_string(index=False))
        # 5. 排序并保存
#        df_result = df_merged.sort_values('Total_Score', ascending=False)
#        output_path = "D:/E_Internship/3_Specie_Selection/Tarfaya/Species_Ranking_Final.csv"
#        df_result.to_csv(output_path, index=False)

#        print(f"\n完整结果已保存至：{output_path}")

    except Exception as e:
        print(f"程序运行失败: {str(e)}")


if __name__ == "__main__":
    main()