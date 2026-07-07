import os
import pandas as pd
import matplotlib.pyplot as plt
from src.utils.plot_config import set_matplotlib_style

set_matplotlib_style()

def plot_product_analysis(df_ab, save_dir="reports/figures"):
    """绘制Top10品牌销售额相关图表"""
    os.makedirs(save_dir, exist_ok=True)

    fig, axs = plt.subplots(1, 3, figsize=(15, 4))

    # Top10品牌 vs 其他 整体占比
    top_sales = df_ab.groupby("brand")["price"].sum().sort_values(ascending=False).head(10).sum()
    total_sales = df_ab["price"].sum()
    pd.Series({"Others": total_sales - top_sales, "Top10": top_sales}).plot(
        kind="pie", title="Top10品牌销售额占比Total",
        autopct="%.2f%%", ax=axs[0], ylabel=""
    )

    # Top10品牌各自销售额占比
    df_ab.groupby("brand")["price"].sum().sort_values(ascending=False).head(10).plot(
        kind="pie", autopct="%.1f%%", ax=axs[1], ylabel="",
        title="Top10品牌销售额占比图"
    )

    # AB类客户Top10品牌销售额堆叠柱状图
    df_ab.groupby(["brand", "user_level"])["price"].sum().unstack()\
        .sort_values(by=["B"], ascending=False).head(10).plot(
        stacked=True, kind="bar", title="Top10品牌销售额统计图",
        ax=axs[2], xlabel=""
    )

    plt.tight_layout()
    save_path = os.path.join(save_dir, "02_产品品牌分析.png")
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ 产品品牌图表已保存：{save_path}")