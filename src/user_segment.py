import pandas as pd

def segment_ab_users(df_clean):
    """
    按订单数将用户分为A类（高频>=30单）和B类（普通<30单）
    返回带user_level字段的完整数据集
    """
    df = df_clean.copy()

    # 统计每个用户的订单数
    user_record = df.groupby("user_id")["order_id"].count().sort_values(ascending=False)
    
    # 拆分B类用户（订单数<30）
    df_b = df.loc[df["user_id"].isin(user_record[user_record < 30].index)]
    df_b["user_level"] = "B"
    
    # 拆分A类用户（订单数>=30）
    df_a = df.loc[~df["user_id"].isin(list(df_b["user_id"]))]
    df_a["user_level"] = "A"
    
    # 合并两类用户
    df_ab = pd.concat([df_a, df_b], axis=0)
    return df_ab

if __name__ == "__main__":
    from src.data_loader import load_raw_data
    from src.data_cleaner import clean_data
    
    raw_df = load_raw_data()
    clean_df = clean_data(raw_df)
    df_ab = segment_ab_users(clean_df)
    
    print("用户分层完成")
    print(df_ab.groupby("user_level")["user_id"].nunique())