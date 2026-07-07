from src.data_loader import load_raw_data
from src.data_cleaner import clean_data
from src.user_segment import segment_ab_users
from src.demographic_analysis import plot_demographic_analysis
from src.product_analysis import plot_product_analysis
from src.sales_analysis import run_sales_analysis
from src.rfm_analysis import run_rfm_analysis

def main():
    print("=" * 50)
    print("  电子产品销售分析项目启动")
    print("=" * 50)

    # 1. 读取原始数据
    print("\n[1/7] 读取原始数据...")
    raw_df = load_raw_data()

    # 2. 数据清洗
    print("\n[2/7] 数据清洗与预处理...")
    clean_df = clean_data(raw_df)

    # 3. 用户AB分层
    print("\n[3/7] 用户AB分层...")
    df_ab = segment_ab_users(clean_df)
    df_b = df_ab[df_ab["user_level"] == "B"]

    # 4. 人群画像分析
    print("\n[4/7] 生成人群画像分析图表...")
    plot_demographic_analysis(clean_df)

    # 5. 产品品牌分析
    print("\n[5/7] 生成产品品牌分析图表...")
    plot_product_analysis(df_ab)

    # 6. 销量与运营分析
    print("\n[6/7] 生成销量与运营分析图表...")
    run_sales_analysis(clean_df, df_ab)

    # 7. RFM会员价值分析
    print("\n[7/7] 生成RFM会员价值分析...")
    run_rfm_analysis(df_b)

    print("\n" + "=" * 50)
    print("🎉 项目运行完成！")
    print("📊 图表输出位置：reports/figures/")
    print("📁 数据结果位置：data/processed/")
    print("=" * 50)

if __name__ == "__main__":
    main()