import matplotlib.pyplot as plt

def set_matplotlib_style():
    """Windows环境中文字体配置，顺序：先加载样式，再覆盖字体参数"""
    # 第一步：先应用样式主题
    plt.style.use("seaborn-v0_8-whitegrid")
    
    # 第二步：样式加载完成后，再强制设置字体（不会被覆盖）
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
    # 解决负号显示为方块的问题
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 100