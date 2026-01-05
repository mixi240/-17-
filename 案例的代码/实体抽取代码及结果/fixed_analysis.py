# fixed_analysis.py - 修复版分析
import json
import csv
from collections import Counter, defaultdict

print("哪吒知识图谱 - 最终分析报告")
print("=" * 70)

# 1. 基本信息
print("\n📊 一、基本信息统计")
print("-" * 40)

try:
    with open('output/statistics.json', 'r', encoding='utf-8') as f:
        stats = json.load(f)
    
    text_length = stats.get('text_length', 'N/A')
    if text_length != 'N/A':
        print(f"• 文本处理长度: {text_length:,} 字符")
    else:
        print(f"• 文本处理长度: {text_length} 字符")
    
    print(f"• 识别实体总数: {stats.get('total_entities', 'N/A')}")
    print(f"• 抽取关系总数: {stats.get('total_relations', 'N/A')}")
    print(f"• 构建三元组总数: {stats.get('total_triples', 'N/A')}")
    print(f"• 哪吒相关三元组: {stats.get('nezha_triples', 'N/A')}")
    
except Exception as e:
    print(f"读取统计信息失败: {e}")

# 2. 查看哪吒相关三元组
print("\n🌟 二、哪吒核心关系网络")
print("-" * 40)

nezha_data = []
try:
    # 先尝试从CSV读取
    with open('output/nezha_triples.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            if len(row) >= 3:
                nezha_data.append({
                    'subject': row[0],
                    'predicate': row[1],
                    'object': row[2]
                })
except:
    try:
        # 如果CSV失败，从JSON读取
        with open('output/nezha_triples.json', 'r', encoding='utf-8') as f:
            nezha_data = json.load(f)
    except Exception as e:
        print(f"读取哪吒数据失败: {e}")
        nezha_data = []

if nezha_data:
    print(f"找到 {len(nezha_data)} 个哪吒相关关系")
    
    # 按关系类型分组
    rel_groups = defaultdict(list)
    for item in nezha_data:
        if isinstance(item, dict):
            pred = item.get('predicate', '未知')
            rel_groups[pred].append(item)
    
    print("\n关系类型分布:")
    for rel_type, items in sorted(rel_groups.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {rel_type}: {len(items)} 个")
    
    # 显示最重要的关系
    print("\n最重要的哪吒关系:")
    important_relations = []
    
    # 优先显示这些关键关系
    priority_relations = ['父亲', '师父', '创作', '导演', '改编自', '出现于']
    
    for rel_type in priority_relations:
        if rel_type in rel_groups:
            for item in rel_groups[rel_type][:3]:  # 每种类型显示前3个
                subject = item.get('subject', '')
                object_ = item.get('object', '')
                if subject and object_:
                    important_relations.append((subject, rel_type, object_))
    
    # 显示其他关系
    other_count = 0
    for rel_type, items in rel_groups.items():
        if rel_type not in priority_relations:
            other_count += len(items)
    
    if other_count > 0:
        important_relations.append(("其他", f"{other_count}个", "各种关系"))
    
    for i, (subject, predicate, object_) in enumerate(important_relations, 1):
        print(f"  {i:2d}. {subject} --[{predicate}]--> {object_}")

# 3. 知识发现总结
print("\n💡 三、重要知识发现")
print("-" * 40)

# 检查哪些关键知识被提取到了
key_knowledge = [
    ("哪吒", "父亲", "李靖"),
    ("哪吒", "师父", "太乙真人"),
    ("哪吒", "出现于", "《封神演义》"),
    ("吴承恩", "创作", "《西游记》"),
    ("许仲琳", "创作", "《封神演义》"),
    ("饺子", "导演", "《哪吒之魔童降世》"),
    ("《哪吒之魔童降世》", "改编自", "《封神演义》"),
]

found = []
not_found = []

for subject, predicate, object_ in key_knowledge:
    found_it = False
    for item in nezha_data:
        if isinstance(item, dict):
            if (item.get('subject') == subject and 
                item.get('predicate') == predicate and 
                item.get('object') == object_):
                found_it = True
                break
    
    if found_it:
        found.append((subject, predicate, object_))
    else:
        not_found.append((subject, predicate, object_))

print(f"关键知识发现: {len(found)}/{len(key_knowledge)}")
if found:
    print("\n✓ 已发现的重要知识:")
    for subject, predicate, object_ in found:
        print(f"  • {subject} --[{predicate}]--> {object_}")
if not_found:
    print("\n○ 未发现但预期的重要知识:")
    for subject, predicate, object_ in not_found:
        print(f"  • {subject} --[{predicate}]--> {object_}")

# 4. 查看部分三元组示例
print("\n📋 四、三元组示例")
print("-" * 40)

# 读取所有三元组
all_triples = []
try:
    with open('output/triples.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = next(reader)
        count = 0
        for row in reader:
            if len(row) >= 3:
                all_triples.append(row)
                count += 1
                if count >= 15:  # 只显示15个
                    break
except Exception as e:
    print(f"读取三元组失败: {e}")
    all_triples = []

if all_triples:
    print("部分三元组示例:")
    for i, row in enumerate(all_triples, 1):
        if len(row) >= 3:
            print(f"  {i:2d}. {row[0]} --[{row[1]}]--> {row[2]}")
else:
    print("无三元组数据")

print("\n" + "=" * 70)
print("分析完成！")
print("=" * 70)

# 提供简单统计
if nezha_data:
    print(f"\n总结: 从文本中成功提取了 {len(nezha_data)} 个哪吒相关关系")
    print("其中包括哪吒的家庭关系、师徒关系、作品关系等")