import matplotlib.pyplot as plt
import platform

def set_matplotlib_style():
    """统一matplotlib字体和风格，解决中文乱码"""
    system = platform.system()
    if system == "Windows":
        font_name = "Microsoft YaHei"
    elif system == "Darwin":  # Mac
        font_name = "PingFang SC"
    else:  # Linux
        font_name = "WenQuanYi Micro Hei"

    plt.rcParams["font.sans-serif"] = [font_name]
    plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
    plt.rcParams["figure.dpi"] = 100
    plt.style.use("seaborn-v0_8-whitegrid")