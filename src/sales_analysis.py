import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.utils.plot_config import set_matplotlib_style

set_matplotlib_style()

# ---------------------- 4.1 订单月度拆解 ----------------------
def plot_monthly_order_analysis(df_ab, df_a, df_b, save_dir="reports/figures"):
    os.makedirs(save_dir, exist_ok=True)
    fig, axs = plt.subplots(2, 3, figsize=(16, 8))

    # 销售额月度统计
    df_ab.groupby(["month", "user_level"])["price"].sum().unstack().plot(
        grid=True, title="销售额-月度统计", xlabel="", ax=axs[0, 0]
    )
    df_ab.groupby("month")["price"].sum().rename("A+B").plot(
        ax=axs[0, 0], color="r"
    ).legend(loc=2)

    # 订单数月度统计
    df_ab.groupby(["month", "user_level"])["order_id"].count().unstack().plot(
        grid=True, title="订单数-月度统计", xlabel="", ax=axs[0, 1]
    )

    # 订单均价月度变化
    (df_a.groupby("month")["price"].sum() / df_a.groupby("month")["order_id"].count()).rename("A").plot(
        xlabel="", ax=axs[0, 2]
    )
    (df_b.groupby("month")["price"].sum() / df_b.groupby("month")["order_id"].count()).rename("B").plot(
        grid=True, title="订单均价-月度变化图", xlabel="", ax=axs[0, 2]
    ).legend(loc=2)

    # 下单人数月度统计
    df_ab.groupby(["month", "user_level"]).user_id.nunique().unstack().plot(
        grid=True, title="下单人数-月度统计", xlabel="", ax=axs[1, 0]
    )

    # 人均订单数
    ax2 = (df_a.groupby("month")["order_id"].count() / df_a.groupby("month").user_id.nunique()).rename("A").plot(
        grid=True, xlabel="", ax=axs[1, 1], legend=1
    )
    (df_b.groupby("month")["order_id"].count() / df_b.groupby("month").user_id.nunique()).rename("B").plot(
        title="人均订单数-月度变化图", xlabel="", ax=ax2.twinx(), color="orange"
    ).legend(loc=2)

    # 人均客单价
    ax1 = (df_a.groupby("month")["price"].sum() / df_a.groupby("month").user_id.nunique()).rename("A").plot(
        grid=True, xlabel="", ax=axs[1, 2], legend=1
    )
    (df_b.groupby("month")["price"].sum() / df_b.groupby("month").user_id.nunique()).rename("B").plot(
        title="人均客单价-月度变化图", xlabel="", ax=ax1.twinx(), color="orange"
    ).legend(loc=6)

    plt.tight_layout()
    save_path = os.path.join(save_dir, "03_月度订单拆解分析.png")
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ 月度订单拆解图表已保存：{save_path}")


# ---------------------- 4.2 月度会员活跃度 ----------------------
def plot_user_active_status(df_clean, df_ab, save_dir="reports/figures"):
    os.makedirs(save_dir, exist_ok=True)

    columns_month = df_clean["month"].sort_values().astype("str").unique()

    def active_status(x):
        status = []
        for i in range(len(columns_month)):
            if x[i] == 0:
                if i == 0:
                    status.append("unreg")
                else:
                    status.append("unreg") if status[i-1] == "unreg" else status.append("unactive")
            else:
                if i == 0:
                    status.append("new")
                else:
                    if status[i-1] == "unreg":
                        status.append("new")
                    else:
                        status.append("return") if status[i-1] == "unactive" else status.append("active")
        return pd.Series(status, index=columns_month)

    # 构建用户月度消费矩阵
    order_record = df_clean.pivot_table(
        index="user_id", columns="month", values="price", aggfunc="sum"
    ).fillna(0).applymap(lambda i: 1 if i > 0 else 0)
    order_record.columns = columns_month

    user_active_status = order_record.apply(active_status, axis=1)

    # 绘图
    ax1 = user_active_status.apply(lambda x: pd.value_counts(x)).drop("unreg").fillna(0).T.plot(
        kind="area", figsize=(12, 6)
    )
    df_ab.groupby([df_ab["event_time"].dt.month])["price"].sum().rename("销售额").plot(
        ax=ax1.twinx(), grid=True, color="b",
        title="不同标签用户数与GMV变化关系图",
        xlabel="", use_index=False
    ).legend(loc=6)

    plt.tight_layout()
    save_path = os.path.join(save_dir, "04_会员活跃度变化.png")
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ 会员活跃度图表已保存：{save_path}")


# ---------------------- 4.3 复购率分析 ----------------------
def plot_repurchase_analysis(df_b, save_dir="reports/figures"):
    os.makedirs(save_dir, exist_ok=True)
    fig, axs = plt.subplots(1, 2, figsize=(14, 5))

    # B类客户订单数量分布
    df_b.groupby("user_id")["order_id"].count().plot(
        kind="hist", bins=30, ax=axs[0], title="B类客户订单数量分布图"
    )

    # 前10订单占比
    order_totll = df_b.groupby("user_id").agg(
        {"order_id": pd.Series.count, "price": np.max}
    ).groupby("order_id")["price"].count().head(10)
    
    order_totll.plot(
        wedgeprops={"width": 0.25, "edgecolor": "w"}, ylabel="",
        kind="pie", autopct="%.1f%%", ax=axs[1], title="B类客户前10订单占比图"
    )

    plt.tight_layout()
    save_path = os.path.join(save_dir, "05_复购率分析.png")
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ 复购率图表已保存：{save_path}")


# ---------------------- 4.4 二次订单间隔 ----------------------
def plot_second_order_interval(df_b, save_dir="reports/figures"):
    os.makedirs(save_dir, exist_ok=True)

    order_2b = df_b[["user_id", "event_time", "order_id"]].reset_index(drop=True)
    order_2b = order_2b.groupby(by=["user_id", "event_time"], as_index=False)["order_id"].count()
    order_2b = order_2b.pivot_table(index="user_id", columns="event_time", values="order_id").fillna(0)

    def data_count(x):
        fig = 0
        for i in range(len(x)):
            if x.iloc[i] != 0:
                if fig != 1:
                    fig += 1
                    a = i
                else:
                    a = i - a
                    return a

    second_order = order_2b.apply(data_count, axis=1)

    fig, axs = plt.subplots(1, 2, figsize=(14, 5))
    second_order.plot(kind="box", title="二次下单间隔-箱线图（天）", ax=axs[0])
    second_order.plot(kind="hist", title="二次下单间隔-直方图（天）", ax=axs[1], bins=60)

    plt.tight_layout()
    save_path = os.path.join(save_dir, "06_二次订单间隔.png")
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ 二次订单间隔图表已保存：{save_path}")


# 统一入口函数
def run_sales_analysis(df_clean, df_ab):
    df_a = df_ab[df_ab["user_level"] == "A"]
    df_b = df_ab[df_ab["user_level"] == "B"]
    
    plot_monthly_order_analysis(df_ab, df_a, df_b)
    plot_user_active_status(df_clean, df_ab)
    plot_repurchase_analysis(df_b)
    plot_second_order_interval(df_b)