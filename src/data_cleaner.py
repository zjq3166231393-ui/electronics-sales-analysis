import pandas as pd

def clean_data(df_raw):
    """
    数据清洗与预处理
    1. 删除无用列
    2. 缺失值填充
    3. 按订单ID去重
    4. 时间字段修正与转换
    5. 新增月份字段
    """
    df = df_raw.copy()

    # 删除无用列（如果存在）
    if "category_code" in df.columns:
        del df["category_code"]
    
    # 品牌缺失值填充
    df["brand"].fillna("no_brand", inplace=True)
    
    # 按订单ID去重
    df = df.drop_duplicates("order_id")
    
    # 时间字段修正（1970替换为2020）与日期转换
    df["event_time"] = df["event_time"].str.replace("1970", "2020")
    df["event_time"] = pd.to_datetime(df["event_time"]).dt.to_period("D")
    
    # 设置时间索引
    df = df.set_index("event_time", drop=False)
    
    # 新增月份字段
    df["month"] = df["event_time"].dt.month

    return df

if __name__ == "__main__":
    from src.data_loader import load_raw_data
    raw_df = load_raw_data()
    clean_df = clean_data(raw_df)
    print("数据清洗完成")
    print(f"清洗后数据量：{len(clean_df)} 行")
    print(clean_df.dtypes)