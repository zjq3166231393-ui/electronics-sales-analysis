import os
import matplotlib.pyplot as plt
from src.utils.plot_config import set_matplotlib_style

set_matplotlib_style()

def plot_demographic_analysis(df_clean, save_dir="reports/figures"):
    """绘制地区、性别、年龄人群画像图表，自动保存到指定目录"""
    os.makedirs(save_dir, exist_ok=True)

    fig, axs = plt.subplots(2, 2, figsize=(14, 14))

    # 消费金额地区分布-饼图
    df_clean.groupby("local")["price"].sum().sort_values().plot(
        kind="pie", ylabel="", ax=axs[0, 0], autopct="%.0f%%",
        wedgeprops={"width": 0.3}, title="消费金额地区分布扇形图"
    )

    # 性别比例
    df_clean.groupby("sex")["user_id"].nunique().plot(
        kind="pie", title="性别比例图", ax=axs[0, 1], ylabel="",
        autopct="%.0f%%", wedgeprops={"width": 0.3}
    )

    # 消费金额地区分布-条形图
    df_clean.groupby("local")["price"].sum().sort_values().plot(
        kind="bar", ax=axs[1, 0], xlabel="", title="消费金额地区分布条形图"
    )

    # 年龄-人数&消费金额双轴图
    ax1 = df_clean.groupby("age")["user_id"].nunique().rename("人数").plot(
        title="客户年龄-消费金额关系变化图", ylabel="人数",
        ax=axs[1, 1], xlabel="", legend=1
    )
    ax2 = ax1.twinx()
    df_clean.groupby("age")["price"].sum().rename("消费总金额").plot(
        ax=ax2, color="orange", ylabel="消费金额", legend=True, xlabel=""
    )
    ax2.legend(loc=2)

    plt.tight_layout()
    save_path = os.path.join(save_dir, "01_人群画像分析.png")
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ 人群画像图表已保存：{save_path}")