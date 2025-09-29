import pandas as pd
import json
from datetime import datetime

# 读取分析结果
with open('analysis_result.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. 创建共同字段详细表格
print("正在生成结构化表格...")

# 共同字段表格
common_fields_data = []
for field, files in data['common_fields'].items():
    common_fields_data.append({
        '字段名称': field,
        '出现次数': len(files),
        '出现的表格': ', '.join([f.replace('.xlsx', '').replace('.xls', '') for f in files])
    })

common_df = pd.DataFrame(common_fields_data)
common_df = common_df.sort_values('出现次数', ascending=False)

# 2. 创建各表格字段统计表格
table_stats_data = []
for table, fields in data['all_headers'].items():
    table_name = table.replace('.xlsx', '').replace('.xls', '').replace('.docx', '').replace('.doc', '')
    table_stats_data.append({
        '表格名称': table_name,
        '字段总数': len(fields),
        '共同字段数': sum(1 for field in fields if field in data['common_fields']),
        '独特字段数': sum(1 for field in fields if field in data['unique_fields']),
        '主要字段': ', '.join(fields[:5]) + ('...' if len(fields) > 5 else '')
    })

table_stats_df = pd.DataFrame(table_stats_data)
table_stats_df = table_stats_df.sort_values('字段总数', ascending=False)

# 3. 创建字段分类表格
field_categories = {
    '基本信息字段': ['姓名', '性别', '年龄', '身份证号码', '联系电话', '联系方式'],
    '地址位置字段': ['地址', '居住地址', '乡镇', '镇乡', '村', '村（社区）', '行政村'],
    '时间日期字段': ['年', '填报日期', '出生日期', '外出日期', '排查时间', '整改时限'],
    '状态标识字段': ['备注', '类别', '性质', '状况', '情况', '是否'],
    '编号序列字段': ['序号', '序 号', '人员编号'],
    '填报管理字段': ['填报单位', '填报人', '审核人', '检查人员']
}

category_stats = []
for category, keywords in field_categories.items():
    matching_fields = []
    for field in data['field_count'].keys():
        if any(keyword in field for keyword in keywords):
            matching_fields.append(field)
    
    category_stats.append({
        '字段分类': category,
        '匹配字段数': len(matching_fields),
        '代表字段': ', '.join(matching_fields[:3]) + ('...' if len(matching_fields) > 3 else '')
    })

category_df = pd.DataFrame(category_stats)

# 4. 创建表格功能分类表格
table_categories = {
    '人员管理类': ['后备干部', '外出人员', '留守老人', '流出党员', '婴儿出生', '医保参保'],
    '房屋建筑类': ['房屋基本情况', '自建房', '违建', '经营性自建房'],
    '安全管理类': ['消防安全', '生猪网格化'],
    '党建工作类': ['民主评议', '党建工作'],
    '经济统计类': ['农业年报', '畜牧生产', '商超物流'],
    '基础保障类': ['基层基础保障', '困难群众', '培训调查']
}

functional_stats = []
for category, keywords in table_categories.items():
    matching_tables = []
    for table in data['all_headers'].keys():
        if any(keyword in table for keyword in keywords):
            matching_tables.append(table.replace('.xlsx', '').replace('.xls', '').replace('.docx', '').replace('.doc', ''))
    
    total_fields = sum(len(data['all_headers'][table]) for table in data['all_headers'].keys() 
                      if any(keyword in table for keyword in keywords))
    
    functional_stats.append({
        '功能分类': category,
        '表格数量': len(matching_tables),
        '总字段数': total_fields,
        '平均字段数': round(total_fields / len(matching_tables), 1) if matching_tables else 0,
        '包含表格': ', '.join(matching_tables)
    })

functional_df = pd.DataFrame(functional_stats)

# 5. 保存所有表格到Excel文件
with pd.ExcelWriter('刘营社区表格字段分析报告.xlsx', engine='openpyxl') as writer:
    # 概览表
    overview_data = {
        '统计项目': ['总表格数量', '总字段数量', '共同字段数量', '独特字段数量', '最多字段的表格', '最少字段的表格'],
        '数值': [
            len(data['all_headers']),
            len(data['field_count']),
            len(data['common_fields']),
            len(data['unique_fields']),
            table_stats_df.iloc[0]['表格名称'] + f" ({table_stats_df.iloc[0]['字段总数']}个)",
            table_stats_df.iloc[-1]['表格名称'] + f" ({table_stats_df.iloc[-1]['字段总数']}个)"
        ]
    }
    overview_df = pd.DataFrame(overview_data)
    overview_df.to_excel(writer, sheet_name='分析概览', index=False)
    
    # 共同字段表
    common_df.to_excel(writer, sheet_name='共同字段分析', index=False)
    
    # 表格统计表
    table_stats_df.to_excel(writer, sheet_name='各表格统计', index=False)
    
    # 字段分类表
    category_df.to_excel(writer, sheet_name='字段分类统计', index=False)
    
    # 功能分类表
    functional_df.to_excel(writer, sheet_name='表格功能分类', index=False)
    
    # 详细字段清单
    detailed_fields = []
    for table, fields in data['all_headers'].items():
        for field in fields:
            field_type = '共同字段' if field in data['common_fields'] else '独特字段'
            detailed_fields.append({
                '表格名称': table.replace('.xlsx', '').replace('.xls', '').replace('.docx', '').replace('.doc', ''),
                '字段名称': field,
                '字段类型': field_type,
                '出现次数': len(data['field_count'][field]) if field in data['field_count'] else 1
            })
    
    detailed_df = pd.DataFrame(detailed_fields)
    detailed_df.to_excel(writer, sheet_name='详细字段清单', index=False)

print("结构化表格已生成并保存为 '刘营社区表格字段分析报告.xlsx'")

# 打印主要统计信息
print("\n=== 刘营社区表格字段分析报告 ===")
print(f"分析时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
print(f"总表格数量: {len(data['all_headers'])} 个")
print(f"总字段数量: {len(data['field_count'])} 个")
print(f"共同字段数量: {len(data['common_fields'])} 个")
print(f"独特字段数量: {len(data['unique_fields'])} 个")

print("\n=== 共同字段TOP5 ===")
for i, (field, files) in enumerate(sorted(data['common_fields'].items(), key=lambda x: len(x[1]), reverse=True)[:5]):
    print(f"{i+1}. '{field}' - 出现在 {len(files)} 个表格中")

print("\n=== 字段最多的表格TOP5 ===")
for i, row in table_stats_df.head().iterrows():
    print(f"{i+1}. {row['表格名称']} - {row['字段总数']} 个字段")

print("\n=== 功能分类统计 ===")
for i, row in functional_df.iterrows():
    print(f"• {row['功能分类']}: {row['表格数量']} 个表格, 平均 {row['平均字段数']} 个字段")