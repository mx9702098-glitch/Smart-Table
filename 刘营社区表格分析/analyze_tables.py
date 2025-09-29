import pandas as pd
import os
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def extract_headers_from_excel(file_path):
    """从Excel文件中提取表头"""
    headers = []
    try:
        # 尝试读取多个sheet
        excel_file = pd.ExcelFile(file_path)
        for sheet_name in excel_file.sheet_names:
            try:
                # 尝试不同的header行
                for header_row in [0, 1, 2, 3]:
                    try:
                        df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
                        # 过滤掉Unnamed列和空列
                        cols = [col for col in df.columns if not str(col).startswith('Unnamed') and str(col).strip() != '']
                        if cols and len(cols) > 1:  # 如果找到了有意义的列名
                            headers.extend(cols)
                            break
                    except:
                        continue
            except:
                continue
    except Exception as e:
        print(f"读取 {file_path} 时出错: {e}")
    
    return list(set(headers))  # 去重

def analyze_all_tables():
    """分析所有表格文件"""
    os.chdir('刘营社区表格')
    
    # 获取所有Excel文件
    excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
    
    all_headers = {}
    
    print("开始分析表格文件...")
    print("=" * 50)
    
    for file in excel_files:
        print(f"\n正在分析: {file}")
        headers = extract_headers_from_excel(file)
        all_headers[file] = headers
        print(f"找到字段: {headers}")
    
    return all_headers

def find_common_and_unique_fields(all_headers):
    """找出共同字段和独特字段"""
    # 统计每个字段出现的次数
    field_count = {}
    for file, headers in all_headers.items():
        for header in headers:
            if header not in field_count:
                field_count[header] = []
            field_count[header].append(file)
    
    # 分类字段
    common_fields = {}  # 出现在多个文件中的字段
    unique_fields = {}  # 只出现在一个文件中的字段
    
    for field, files in field_count.items():
        if len(files) > 1:
            common_fields[field] = files
        else:
            unique_fields[field] = files[0]
    
    return common_fields, unique_fields, field_count

# 执行分析
if __name__ == "__main__":
    all_headers = analyze_all_tables()
    common_fields, unique_fields, field_count = find_common_and_unique_fields(all_headers)
    
    print("\n" + "=" * 50)
    print("分析结果汇总")
    print("=" * 50)
    
    print(f"\n共分析了 {len(all_headers)} 个表格文件")
    print(f"总共发现 {len(field_count)} 个不同的字段")
    print(f"共同字段（出现在多个文件中）: {len(common_fields)} 个")
    print(f"独特字段（只出现在一个文件中）: {len(unique_fields)} 个")
    
    print("\n共同字段详情:")
    for field, files in sorted(common_fields.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  '{field}' - 出现在 {len(files)} 个文件中: {files}")
    
    print(f"\n独特字段详情 (共{len(unique_fields)}个):")
    for field, file in list(unique_fields.items())[:20]:  # 只显示前20个
        print(f"  '{field}' - 仅在 '{file}' 中出现")
    
    if len(unique_fields) > 20:
        print(f"  ... 还有 {len(unique_fields) - 20} 个独特字段")
    
    # 保存结果到JSON文件
    result = {
        'all_headers': all_headers,
        'common_fields': common_fields,
        'unique_fields': unique_fields,
        'field_count': field_count
    }
    
    with open('../analysis_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n详细分析结果已保存到 analysis_result.json")