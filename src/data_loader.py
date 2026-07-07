import os
import pandas as pd

def load_raw_data():
    """读取原始销售数据"""
    file_path = os.path.join("data", "raw", "electronics_sales.csv")
    df = pd.read_csv(file_path)
    return df

if __name__ == "__main__":
    df = load_raw_data()
    print(f"数据读取成功，共 {len(df)} 行，{df.shape[1]} 列")
    print(df.head(2))