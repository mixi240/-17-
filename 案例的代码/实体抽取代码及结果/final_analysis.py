# final_analysis.py - 最终分析
import json
import csv
from collections import Counter, defaultdict

print("哪吒知识图谱 - 最终分析报告")
print("=" * 70)

# 1. 基本信息
print("\n📊 一、基本信息统计")
print("-" * 40)

with open('output/statistics.json', 'r', encoding='utf-8') as f:
    stats = json.load(f)

print(f"• 文本处理长度: {stats.get('text_length', 'N/A'):,} 字符")
print(f"• 识别实体总数: {stats['total_entities']}")
print(f"• 抽取关系总数: {stats['total_relations']}")
print(f"• 构建三元组总数: {stats['total_triples']}")
print(f"• 哪吒相关三元组: {stats['nezha_triples']}")

# 2. 实体分析
print("\n👥 二、实体分析")
print("-" * 40)

with open('output/entities.json', 'r', encoding='utf-8') as f:
    entities = json.load(f)

print(f"共识别 {len(entities)} 个实体")

# 实体类型分布
type_stats = defaultdict(int)
for entity in entities:
    type_stats[entity['type']] += 1

print("\n实体类型分布:")
for etype, count in sorted(type_stats.items(), key=lambda x: x[1], reverse=True):
    print(f"  {etype:10} : {count:3d} 个")

# 出现频率最高的实体
if 'count' in entities[0]:
    top_entities = sorted(entities, key=lambda x: x.get('count', 0), reverse=True)[:15]
    print("\n出现频率最高的实体:")
    for i, entity in enumerate(top_entities, 1):
        print(f"  {i:2d}. {entity['text']:15} : {entity.get('count', 0):4d} 次 ({entity['type']})")

# 3. 关系分析
print("\n🔗 三、关系分析")
print("-" * 40)

with open('output/relations.json', 'r', encoding='utf-8') as f:
    relations = json.load(f)

print(f"共抽取 {len(relations)} 个关系")

# 关系类型分布
rel_stats = Counter([rel['predicate'] for rel in relations])
print("\n关系类型分布:")
for rel_type, count in rel_stats.most_common():
    print(f"  {rel_type:10} : {count:3d} 个")

# 4. 哪吒核心关系网络
print("\n🌟 四、哪吒核心关系网络")
print("-" * 40)

# 读取哪吒相关三元组
nezha_triples = []
try:
    with open('output/nezha_triples.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        nezha_triples = list(reader)
except:
    with open('output/nezha_triples.json', 'r', encoding='utf-8') as f:
        nezha_triples = json.load(f)

print(f"哪吒相关关系: {len(nezha_triples)} 个")

# 按关系类型分组
nezha_by_type = defaultdict(list)
for triple in nezha_triples:
    if isinstance(triple, dict):
        pred = triple.get('predicate') or triple.get('predicate', '')
        subject = triple.get('subject') or triple.get('subject', '')
        object_ = triple.get('object') or triple.get('object', '')
        nezha_by_type[pred].append((subject, object_))

print("\n哪吒关系详细分析:")
for rel_type, pairs in sorted(nezha_by_type.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n【{rel_type.upper()}】关系 ({len(pairs)}个):")
    for subject, object_ in pairs[:8]:  # 每种类型最多显示8个
        print(f"  • {subject} → {object_}")

# 5. 知识发现总结
print("\n💡 五、重要知识发现")
print("-" * 40)

# 检查关键知识是否被提取
key_knowledge = [
    ("哪吒", "父亲", "李靖", "家庭关系"),
    ("哪吒", "师父", "太乙真人", "师徒关系"),
    ("哪吒", "出现于", "《封神演义》", "作品归属"),
    ("吴承恩", "创作", "《西游记》", "文学创作"),
    ("许仲琳", "创作", "《封神演义》", "文学创作"),
    ("饺子", "导演", "《哪吒之魔童降世》", "影视创作"),
    ("《哪吒之魔童降世》", "改编自", "《封神演义》", "作品改编"),
    ("哪吒", "敌人", "敖丙", "敌对关系"),
    ("哪吒", "朋友", "敖丙", "朋友关系"),
]

found_count = 0
print("关键知识检查:")
for subject, predicate, object_, desc in key_knowledge:
    found = False
    for triple in nezha_triples:
        if isinstance(triple, dict):
            t_subj = triple.get('subject') or triple.get('subject', '')
            t_pred = triple.get('predicate') or triple.get('predicate', '')
            t_obj = triple.get('object') or triple.get('object', '')
        else:
            t_subj, t_pred, t_obj = triple[0], triple[1], triple[2]
        
        if t_subj == subject and t_pred == predicate and t_obj == object_:
            found = True
            break
    
    if found:
        print(f"  ✓ {desc}: {subject} --[{predicate}]--> {object_}")
        found_count += 1
    else:
        print(f"  ○ {desc}: {subject} --[{predicate}]--> {object_}")

print(f"\n知识发现率: {found_count}/{len(key_knowledge)} ({found_count/len(key_knowledge)*100:.1f}%)")

# 6. 导出建议
print("\n📁 六、结果文件说明")
print("-" * 40)

files_info = [
    ("triples.csv", "所有三元组", "Excel可打开，完整知识图谱"),
    ("nezha_triples.csv", "哪吒相关三元组", "核心分析对象"),
    ("entities.json", "所有实体", "JSON格式，完整实体列表"),
    ("relations.json", "所有关系", "JSON格式，完整关系列表"),
    ("statistics.json", "统计信息", "JSON格式，各类统计"),
    ("report.txt", "文本报告", "简要分析报告"),
]

print("生成的文件列表:")
for filename, name, desc in files_info:
    print(f"  • {filename:20} - {name:15} : {desc}")

# 7. 后续研究建议
print("\n🔬 七、后续研究方向建议")
print("-" * 40)

suggestions = [
    "1. 扩展实体类型：添加更多神话人物、地点、概念",
    "2. 深化关系抽取：增加时间关系、影响关系、对比关系",
    "3. 构建时间线：分析哪吒形象的历史演变",
    "4. 跨作品分析：比较不同作品中的哪吒形象差异",
    "5. 学者网络：分析研究哪吒的学者及其观点",
    "6. 可视化展示：使用Neo4j或Gephi可视化知识图谱",
]

for suggestion in suggestions:
    print(suggestion)

print("\n" + "=" * 70)
print("分析完成！哪吒知识图谱构建成功！🎉")
print("=" * 70)

# 保存详细报告
report_data = {
    "summary": {
        "total_entities": stats['total_entities'],
        "total_relations": stats['total_relations'],
        "total_triples": stats['total_triples'],
        "nezha_relations": len(nezha_triples)
    },
    "entity_types": dict(type_stats),
    "relation_types": dict(rel_stats),
    "nezha_network": {
        rel_type: pairs for rel_type, pairs in nezha_by_type.items()
    },
    "key_findings": {
        "found": found_count,
        "total": len(key_knowledge),
        "rate": f"{found_count/len(key_knowledge)*100:.1f}%"
    }
}

with open('output/detailed_report.json', 'w', encoding='utf-8') as f:
    json.dump(report_data, f, ensure_ascii=False, indent=2)

print(f"\n📄 详细报告已保存到: output/detailed_report.json")