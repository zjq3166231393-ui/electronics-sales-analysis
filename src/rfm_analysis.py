import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from src.utils.plot_config import set_matplotlib_style

set_matplotlib_style()

def run_rfm_analysis(df_b, save_dir="reports/figures"):
    """对B类客户做RFM分层，输出图表和结果文件"""
    os.makedirs(save_dir, exist_ok=True)

    # 计算R：最近一次消费距截止日的天数
    b_r = df_b.groupby("user_id")["event_time"].min().map(
        lambda i: pd.to_datetime("2020-11-21").to_period("D") - i
    )
    R = b_r.astype("str").map(lambda i: re.compile(r"\d*").findall(i)[1])
    R.loc[b_r.astype("str").map(lambda i: re.compile(r"\d*").findall(i)[1]) == ""] = 1
    R = R.astype("int32")

    # 计算F：消费频次
    F = df_b.groupby("user_id")["order_id"].count()

    # 计算M：消费金额
    M = df_b.groupby("user_id")["price"].sum()

    # RFM分层映射字典
    dic_rfm = {
        "111": "重要会员：倾斜更多资源，VIP服务，个性化服务，附加销售",
        "011": "重要唤回会员：DM营销，提供有用的资源，通过新的商品召唤回",
        "101": "重要深耕会员：交叉销售，制定会员忠诚度计划，推荐其他商品",
        "001": "重要挽留会员：重点联系或摆放，提高留存率",
        "110": "潜力会员：向上营销，销售价值更高的商品",
        "100": "新会员：提供免费试用，提高会员兴趣，创建品牌知名度",
        "010": "一般维持会员：积分制，分享宝贵资源，以折扣推荐热门商品",
        "000": "低价值会员：恢复会员兴趣，否者暂时放弃"
    }

    def rfm_score(x):
        r = "1" if x[0] <= 30 else "0"
        f = "1" if x[1] >= 3 else "0"
        m = "1" if x[2] >= 1257 else "0"
        return dic_rfm[r + f + m]

    b_rfm = pd.concat([R, F, M], axis=1).apply(rfm_score, axis=1)
    B_RFM = pd.concat([
        b_rfm.map(lambda i: i.split("：")[0]).rename("会员类型"),
        b_rfm.map(lambda i: i.split("：")[-1]).rename("营销策略")
    ], axis=1)

    # 绘图
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))
    B_RFM.groupby("会员类型")["营销策略"].count().sort_values().plot(
        kind="barh", title="B会员-类型分布", xlabel="", ax=axs[0], grid=1
    )
    B_RFM.groupby("会员类型")["营销策略"].count().plot(
        kind="pie", title="B会员-类型占比", autopct="%.0f%%",
        ax=axs[1], wedgeprops={"width": 0.3}, ylabel=""
    )

    plt.tight_layout()
    save_path = os.path.join(save_dir, "07_RFM会员分层.png")
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ RFM分析图表已保存：{save_path}")

    # 保存RFM分层结果到processed目录
    os.makedirs("data/processed", exist_ok=True)
    result_path = "data/processed/b类用户rfm分层结果.csv"
    B_RFM.to_csv(result_path, encoding="utf-8-sig")
    print(f"✅ RFM分层结果已保存至：{result_path}")