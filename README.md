电子产品销售分析项目
项目简介
本项目基于电商电子产品销售数据，从销售趋势、用户结构、产品品牌、会员价值四个维度展开全链路分析，通过用户分层、RFM 价值模型等方法拆解业务问题，输出可落地的运营优化建议。项目采用工程化目录结构，支持一键运行生成分析结果，同时配套完整的分析笔记与业务思考。
技术栈： Python / Pandas / Matplotlib
分析目标
拆解销售波动的核心驱动因素，定位业务增长与下滑的本质原因
基于消费行为对用户分层，识别高价值客群与流失风险人群
评估产品品牌结构，挖掘选品优化空间
搭建 RFM 会员价值体系，输出差异化运营策略
目录结构
plaintext
electronics-sales-analysis
├── data/
│   └── raw/                # 原始数据目录（Bronze层）
│       └── electronics_sales.csv
├── src/                    # 核心分析代码（可复用函数模块）
│   ├── utils/              # 通用工具（字体配置等）
│   ├── data_loader.py      # 数据加载模块
│   ├── data_cleaner.py     # 数据清洗模块
│   ├── user_segment.py     # 用户AB分层模块
│   ├── demographic_analysis.py  # 人群画像分析
│   ├── product_analysis.py      # 产品品牌分析
│   ├── sales_analysis.py        # 销售与运营分析
│   └── rfm_analysis.py          # RFM会员价值分析
├── notebooks/              # 分析笔记与草稿（逐模块拆解+业务理解）
│   └── original_project_analysis.ipynb
├── reports/
│   └── figures/            # 分析图表输出目录
├── dashboard/              # 交互式看板预留目录
├── docs/                   # 分析报告与文档预留目录
├── images/                 # README配图目录
├── main.py                 # 项目主入口，一键运行全流程
├── requirements.txt        # 项目依赖
└── README.md
环境与运行
环境要求
Python 3.8+
Pandas、Numpy、Matplotlib
运行方式
克隆仓库到本地
安装依赖：pip install -r requirements.txt
执行主程序：python main.py
生成的分析图表将输出至 reports/figures/ 目录
完整逐模块分析与业务思考笔记见 notebooks/original_project_analysis.ipynb
核心结论
销售趋势：4-8 月增长由新用户流量拉动，8 月后下滑源于获客断层，业务整体偏流量驱动，抗波动能力较弱。
用户结构：二八效应显著，不足 2% 的高频用户贡献近 20% 销售额，普通用户是营收基本盘，分层运营必要性强。
产品结构：头部品牌集中度高，Top2 贡献近半数销售额，中腰部品牌潜力未充分释放，选品宽度不足。
会员价值：高价值流失用户占比偏高，唤回空间大；用户二次复购黄金周期为 50 天，触达节奏仍有优化空间。
数据说明
数据周期：2020 年 4 月 - 11 月
核心字段：订单 ID、用户 ID、消费金额、品牌、地区、性别、年龄、下单时间
数据分层：原始数据（raw）→ 加工数据（processed）→ 分析结果（reports）
后续拓展方向
补充成本数据，做利润维度拆解与 ROI 测算
分析品类复购关联，优化搭配推荐策略
搭建销量预测模型，辅助库存规划决策
设计 AB 测试方案，量化验证运营策略效果