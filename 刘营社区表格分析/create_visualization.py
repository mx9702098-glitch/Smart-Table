import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
from matplotlib import rcParams
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 读取分析结果
with open('analysis_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 创建图表
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('刘营社区表格字段分析报告', fontsize=16, fontweight='bold')

# 1. 共同字段出现频率柱状图
common_fields = data['common_fields']
field_names = list(common_fields.keys())
field_counts = [len(files) for files in common_fields.values()]

bars1 = ax1.bar(range(len(field_names)), field_counts, color='skyblue', alpha=0.7)
ax1.set_xlabel('字段名称')
ax1.set_ylabel('出现次数')
ax1.set_title('共同字段出现频率分析')
ax1.set_xticks(range(len(field_names)))
ax1.set_xticklabels(field_names, rotation=45, ha='right')

# 在柱子上添加数值标签
for i, bar in enumerate(bars1):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{int(height)}', ha='center', va='bottom')

# 2. 各表格字段数量对比
all_headers = data['all_headers']
table_names = []
field_counts_per_table = []

for table, fields in all_headers.items():
    # 简化表格名称
    short_name = table.replace('.xlsx', '').replace('.xls', '').replace('.docx', '').replace('.doc', '')
    if len(short_name) > 15:
        short_name = short_name[:12] + '...'
    table_names.append(short_name)
    field_counts_per_table.append(len(fields))

bars2 = ax2.bar(range(len(table_names)), field_counts_per_table, color='lightcoral', alpha=0.7)
ax2.set_xlabel('表格名称')
ax2.set_ylabel('字段数量')
ax2.set_title('各表格字段数量对比')
ax2.set_xticks(range(len(table_names)))
ax2.set_xticklabels(table_names, rotation=45, ha='right')

# 在柱子上添加数值标签
for i, bar in enumerate(bars2):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{int(height)}', ha='center', va='bottom')

# 3. 字段类型分布饼图
total_fields = len(data['field_count'])
common_count = len(data['common_fields'])
unique_count = len(data['unique_fields'])

labels = ['共同字段', '独特字段']
sizes = [common_count, unique_count]
colors = ['lightgreen', 'orange']
explode = (0.1, 0)

ax3.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax3.set_title('字段类型分布')

# 4. 表格分类热力图（按功能分类）
# 根据表格名称进行功能分类
categories = {
    '人员管理': ['后备干部信息统计表', '外出人员信息统计表', '留守老人、空巢老人信息统计表', 
                '流出党员基本信息汇总表', '婴儿出生花名册', '医保参保清理'],
    '房屋建筑': ['农村房屋基本情况摸排表', '生产、经营、出租自建房台账', '违建台账', 
                '经营性自建房数据修正统计汇总表'],
    '安全管理': ['消防安全隐患集中整治行动统计表', '生猪网格化管理排查登记表'],
    '党建工作': ['民主评议党员测评表', '社区党建工作重点任务推进情况统计表'],
    '经济统计': ['农业年报表', '季度畜牧生产 季报', '商超、物流统计'],
    '基础保障': ['基层基础保障信息统计表', '特殊困难群众走访关爱台账', '全国培训调查问卷表']
}

# 创建分类矩阵
category_matrix = []
category_labels = []
for category, tables in categories.items():
    category_labels.append(category)
    row = []
    for table in table_names:
        # 检查表格是否属于该分类
        belongs = any(table_part in table for table_part in [t.replace('.xlsx', '').replace('.xls', '').replace('.docx', '').replace('.doc', '') for t in tables])
        row.append(1 if belongs else 0)
    category_matrix.append(row)

# 绘制热力图
im = ax4.imshow(category_matrix, cmap='YlOrRd', aspect='auto')
ax4.set_xticks(range(len(table_names)))
ax4.set_xticklabels(table_names, rotation=45, ha='right')
ax4.set_yticks(range(len(category_labels)))
ax4.set_yticklabels(category_labels)
ax4.set_title('表格功能分类热力图')

# 添加颜色条
plt.colorbar(im, ax=ax4, shrink=0.6)

plt.tight_layout()
plt.savefig('刘营社区表格字段分析图表.png', dpi=300, bbox_inches='tight')
plt.show()

print("可视化图表已生成并保存为 '刘营社区表格字段分析图表.png'")