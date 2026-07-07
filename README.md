# 📊 电子产品销售分析项目

基于电商销售数据，从 **销售趋势、用户结构、产品品牌、会员价值** 四个维度展开全链路分析，结合用户分层与 RFM 模型，输出可落地的运营优化建议。

**技术栈**：Python · Pandas · Matplotlib

---

## 🎯 分析目标
- 拆解销售波动的核心驱动因素  
- 基于消费行为对用户分层，识别高价值与流失风险人群  
- 评估产品品牌结构，挖掘选品优化空间  
- 搭建 RFM 会员价值体系，输出差异化运营策略  

---

## 📁 目录结构
electronics-sales-analysis/
├── data/raw/ # 原始数据（Bronze层）
│ └── electronics_sales.csv
├── src/ # 核心分析模块
│ ├── utils/ # 通用工具（字体配置等）
│ ├── data_loader.py
│ ├── data_cleaner.py
│ ├── user_segment.py
│ ├── demographic_analysis.py
│ ├── product_analysis.py
│ ├── sales_analysis.py
│ └── rfm_analysis.py
├── notebooks/ # 完整分析笔记（含业务思考）
│ └── original_project_analysis.ipynb
├── reports/figures/ # 图表输出目录
├── dashboard/ # 看板预留
├── docs/ # 报告文档预留
├── images/ # README配图
├── main.py # 一键运行入口
├── requirements.txt
└── README.md

## ⚙️ 环境与运行

### 环境要求
- Python 3.8+
- Pandas, NumPy, Matplotlib

### 运行步骤
```bash
git clone <仓库地址>
cd electronics-sales-analysis
pip install -r requirements.txt
python main.py