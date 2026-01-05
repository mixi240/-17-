# analyze_results.py - 分析结果
import json
import csv
from collections import Counter, defaultdict

print("哪吒知识图谱分析报告")
print("=" * 60)

# 1. 加载统计信息
with open('output/statistics.json', 'r', encoding='utf-8') as f:
    stats = json.load(f)

print(f"📊 总实体数: {stats['total_entities']}")
print(f"🔗 总关系数: {stats['total_relations']}")
print(f"📋 总三元组: {stats['total_triples']}")
print(f"🌟 哪吒相关: {stats['nezha_triples']}")

# 2. 分析哪吒相关关系
print("\n" + "=" * 60)
print("哪吒的核心关系网络")
print("=" * 60)

nezha_relations = []
with open('output/nezha_triples.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        nezha_relations.append(row)

# 按关系类型分组
relation_groups = defaultdict(list)
for rel in nezha_relations:
    relation_groups[rel['predicate']].append(rel)

print(f"发现 {len(nezha_relations)} 个哪吒相关关系，涉及 {len(relation_groups)} 种关系类型")

for rel_type, rels in sorted(relation_groups.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n【{rel_type.upper()}】关系 ({len(rels)}个):")
    for rel in rels[:5]:  # 每种类型显示前5个
        print(f"  • {rel['subject']} → {rel['object']}")

# 3. 分析实体重要性
print("\n" + "=" * 60)
print("关键实体分析")
print("=" * 60)

# 加载实体
with open('output/entities.json', 'r', encoding='utf-8') as f:
    entities = json.load(f)

# 按出现频率排序
sorted_entities = sorted(entities, key=lambda x: x.get('count', 0), reverse=True)

print("出现频率最高的实体:")
for i, entity in enumerate(sorted_entities[:15], 1):
    print(f"  {i:2d}. {entity['text']:15} ({entity['type']}): {entity.get('count', 'N/A')} 次")

# 4. 发现的重要知识
print("\n" + "=" * 60)
print("重要知识发现")
print("=" * 60)

important_findings = []

# 检查哪些关键关系被发现了
key_relations_to_check = [
    ("哪吒", "父亲", "李靖"),
    ("哪吒", "师父", "太乙真人"),
    ("哪吒", "朋友", "敖丙"),
    ("哪吒", "敌人", "敖丙"),
    ("吴承恩", "创作", "《西游记》"),
    ("许仲琳", "创作", "《封神演义》"),
    ("饺子", "导演", "《哪吒之魔童降世》"),
    ("《哪吒之魔童降世》", "改编自", "《封神演义》"),
]

found_count = 0
for subj, pred, obj in key_relations_to_check:
    found = False
    for rel in nezha_relations:
        if rel['subject'] == subj and rel['predicate'] == pred and rel['object'] == obj:
            found = True
            break
    
    if found:
        print(f"✓ 发现: {subj} --[{pred}]--> {obj}")
        found_count += 1
    else:
        print(f"○ 未发现: {subj} --[{pred}]--> {obj}")

print(f"\n关键关系发现率: {found_count}/{len(key_relations_to_check)}")

# 5. 生成知识网络摘要
print("\n" + "=" * 60)
print("知识网络摘要")
print("=" * 60)

# 统计与哪吒直接相关的实体
connected_to_nezha = set()
for rel in nezha_relations:
    if rel['subject'] == '哪吒':
        connected_to_nezha.add(rel['object'])
    elif rel['object'] == '哪吒':
        connected_to_nezha.add(rel['subject'])

print(f"与哪吒直接相关的实体有 {len(connected_to_nezha)} 个:")
for i, entity in enumerate(sorted(connected_to_nezha)[:20], 1):
    print(f"  {i:2d}. {entity}")

# 6. 保存详细分析
analysis_results = {
    "summary": {
        "total_entities": stats['total_entities'],
        "total_relations": stats['total_relations'],
        "total_triples": stats['total_triples'],
        "nezha_relations": len(nezha_relations)
    },
    "key_findings": [
        f"发现 {len(nezha_relations)} 个哪吒相关关系",
        f"涉及 {len(connected_to_nezha)} 个与哪吒直接相关的实体",
        f"关键关系发现率: {found_count}/{len(key_relations_to_check)}"
    ],
    "top_entities": [e['text'] for e in sorted_entities[:10]],
    "nezha_network": list(connected_to_nezha)
}

with open('output/detailed_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_results, f, ensure_ascii=False, indent=2)

print(f"\n✓ 详细分析已保存到: output/detailed_analysis.json")
print("\n" + "=" * 60)
print("分析完成！")
print("=" * 60)