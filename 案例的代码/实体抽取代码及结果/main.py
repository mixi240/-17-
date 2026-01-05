# main.py - 哪吒知识图谱构建系统
import os
import sys
import json
import re
import csv

# 设置UTF-8编码（解决Windows显示问题）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_section(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)

def load_text():
    """加载文本文件"""
    print("正在加载文本文件...")
    
    file_path = "data/all_text.txt"
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 {file_path}")
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✓ 成功加载文件，长度: {len(content):,} 字符")
        return content
    except Exception as e:
        print(f"✗ 加载失败: {e}")
        return None

def extract_entities(text):
    """提取实体"""
    print_section("实体识别")
    
    # 哪吒相关实体词典
    entities_dict = {
        "神话人物": ["哪吒", "李靖", "殷夫人", "太乙真人", "敖丙", "申公豹",
                   "无量仙翁", "玉皇大帝", "龙王", "东海龙王"],
        
        "创作者": ["吴承恩", "许仲琳", "饺子", "乌尔善"],
        
        "学者": ["焦杰", "付方彦", "程国赋", "张茗", "李妙然"],
        
        "作品": ["《封神演义》", "《西游记》", "《哪吒之魔童降世》",
                "《哪吒之魔童闹海》", "《大闹天宫》", "《哪吒闹海》"],
        
        "概念": ["魔丸", "灵珠", "乾坤圈", "风火轮", "火尖枪", "混天绫",
                "我命由我不由天", "神化", "人化"],
        
        "时间": ["唐代", "宋代", "元代", "明代", "1961年", "1979年",
                "2019年", "2025年"],
    }
    
    entities = []
    entity_count = {}
    
    for entity_type, keywords in entities_dict.items():
        for keyword in keywords:
            count = text.count(keyword)
            if count > 0:
                entities.append({
                    "text": keyword,
                    "type": entity_type,
                    "count": count
                })
                entity_count[entity_type] = entity_count.get(entity_type, 0) + 1
    
    print(f"识别到 {len(entities)} 个实体")
    
    # 按类型统计
    print("\n实体类型分布:")
    for etype, count in sorted(entity_count.items()):
        print(f"  {etype}: {count}")
    
    # 按出现频率排序
    entities_sorted = sorted(entities, key=lambda x: x["count"], reverse=True)
    
    print("\n出现频率最高的实体:")
    for i, entity in enumerate(entities_sorted[:15], 1):
        print(f"  {i:2d}. {entity['text']}: {entity['count']} 次 ({entity['type']})")
    
    return entities_sorted

def extract_relations(text, entities):
    """提取关系"""
    print_section("关系抽取")
    
    # 简化关系模式（只找最关键的）
    relation_patterns = [
        # 创作关系
        (r'([^，。]+?)创作《([^》]+)》', '创作'),
        (r'([^，。]+?)编写《([^》]+)》', '创作'),
        
        # 父子关系
        (r'([^，。]+?)是([^，。]+?)的父亲', '父亲'),
        (r'([^，。]+?)是([^，。]+?)的母亲', '母亲'),
        
        # 师徒关系
        (r'([^，。]+?)是([^，。]+?)的师父', '师父'),
        
        # 改编关系
        (r'《([^》]+)》改编自《([^》]+)》', '改编自'),
        
        # 研究关系
        (r'([^，。]+?)研究([^，。]+?)', '研究'),
        (r'([^，。]+?)分析([^，。]+?)', '研究'),
        
        # 敌对关系
        (r'([^，。]+?)与([^，。]+?)是敌人', '敌人'),
        
        # 朋友关系
        (r'([^，。]+?)与([^，。]+?)是朋友', '朋友'),
    ]
    
    relations = []
    seen = set()
    
    # 从实体列表中提取实体文本
    entity_texts = [e["text"] for e in entities]
    
    for pattern, rel_type in relation_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            if len(match.groups()) >= 2:
                subject = match.group(1).strip()
                obj = match.group(2).strip()
                
                # 检查是否是我们关心的实体
                if subject in entity_texts and obj in entity_texts:
                    key = f"{subject}|{rel_type}|{obj}"
                    if key not in seen:
                        seen.add(key)
                        relations.append({
                            "subject": subject,
                            "predicate": rel_type,
                            "object": obj
                        })
    
    # 添加一些已知的重要关系
    known_relations = [
        ("哪吒", "父亲", "李靖"),
        ("哪吒", "师父", "太乙真人"),
        ("吴承恩", "创作", "《西游记》"),
        ("许仲琳", "创作", "《封神演义》"),
        ("饺子", "导演", "《哪吒之魔童降世》"),
        ("哪吒", "出现于", "《封神演义》"),
        ("《哪吒之魔童降世》", "改编自", "《封神演义》"),
    ]
    
    for subject, predicate, obj in known_relations:
        if subject in entity_texts and obj in entity_texts:
            key = f"{subject}|{predicate}|{obj}"
            if key not in seen:
                seen.add(key)
                relations.append({
                    "subject": subject,
                    "predicate": predicate,
                    "object": obj
                })
    
    print(f"抽取到 {len(relations)} 个关系")
    
    # 按关系类型统计
    rel_stats = {}
    for rel in relations:
        pred = rel["predicate"]
        rel_stats[pred] = rel_stats.get(pred, 0) + 1
    
    print("\n关系类型分布:")
    for pred, count in sorted(rel_stats.items()):
        print(f"  {pred}: {count}")
    
    print("\n关系示例:")
    for i, rel in enumerate(relations[:20], 1):
        print(f"  {i:2d}. {rel['subject']} --[{rel['predicate']}]--> {rel['object']}")
    
    return relations

def build_triples(entities, relations):
    """构建三元组"""
    print_section("构建三元组")
    
    triples = []
    
    # 从关系构建
    for rel in relations:
        triples.append({
            "subject": rel["subject"],
            "predicate": rel["predicate"],
            "object": rel["object"],
            "type": "relation"
        })
    
    # 从实体构建类型信息
    for entity in entities[:100]:  # 只取前100个，避免太多
        triples.append({
            "subject": entity["text"],
            "predicate": "类型",
            "object": entity["type"],
            "type": "entity_type"
        })
    
    print(f"构建了 {len(triples)} 个三元组")
    
    # 哪吒相关的三元组
    nezha_triples = [t for t in triples if "哪吒" in t["subject"] or "哪吒" in t["object"]]
    print(f"其中与哪吒相关的: {len(nezha_triples)} 个")
    
    if nezha_triples:
        print("\n哪吒核心关系:")
        for i, triple in enumerate(nezha_triples[:15], 1):
            print(f"  {i:2d}. ({triple['subject']}, {triple['predicate']}, {triple['object']})")
    
    return triples, nezha_triples

def save_results(entities, relations, triples, nezha_triples):
    """保存结果"""
    print_section("保存结果")
    
    # 创建输出目录
    os.makedirs("output", exist_ok=True)
    
    # 1. 保存为JSON
    print("正在保存JSON文件...")
    with open("output/entities.json", "w", encoding="utf-8") as f:
        json.dump(entities, f, ensure_ascii=False, indent=2)
    
    with open("output/relations.json", "w", encoding="utf-8") as f:
        json.dump(relations, f, ensure_ascii=False, indent=2)
    
    with open("output/triples.json", "w", encoding="utf-8") as f:
        json.dump(triples, f, ensure_ascii=False, indent=2)
    
    with open("output/nezha_triples.json", "w", encoding="utf-8") as f:
        json.dump(nezha_triples, f, ensure_ascii=False, indent=2)
    
    # 2. 保存为CSV
    print("正在保存CSV文件...")
    
    # 三元组CSV
    with open("output/triples.csv", "w", encoding="utf-8-sig", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["subject", "predicate", "object", "type"])
        for triple in triples:
            writer.writerow([triple["subject"], triple["predicate"], triple["object"], triple["type"]])
    
    # 哪吒相关三元组CSV
    with open("output/nezha_triples.csv", "w", encoding="utf-8-sig", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["subject", "predicate", "object", "type"])
        for triple in nezha_triples:
            writer.writerow([triple["subject"], triple["predicate"], triple["object"], triple["type"]])
    
    # 3. 保存统计信息
    stats = {
        "total_entities": len(entities),
        "entity_types": {},
        "total_relations": len(relations),
        "relation_types": {},
        "total_triples": len(triples),
        "nezha_triples": len(nezha_triples)
    }
    
    # 实体类型统计
    for entity in entities:
        etype = entity["type"]
        stats["entity_types"][etype] = stats["entity_types"].get(etype, 0) + 1
    
    # 关系类型统计
    for rel in relations:
        pred = rel["predicate"]
        stats["relation_types"][pred] = stats["relation_types"].get(pred, 0) + 1
    
    with open("output/statistics.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    # 4. 生成文本报告
    with open("output/report.txt", "w", encoding="utf-8") as f:
        f.write("哪吒知识图谱构建报告\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"文本长度: {len(text) if 'text' in locals() else 'N/A'} 字符\n")
        f.write(f"识别实体: {len(entities)} 个\n")
        f.write(f"抽取关系: {len(relations)} 个\n")
        f.write(f"构建三元组: {len(triples)} 个\n")
        f.write(f"哪吒相关三元组: {len(nezha_triples)} 个\n\n")
        
        f.write("重要发现:\n")
        for rel in relations:
            if "哪吒" in rel["subject"]:
                f.write(f"  • {rel['subject']} 的 {rel['predicate']} 是 {rel['object']}\n")
    
    print("✓ 结果已保存到 output/ 目录")
    print("\n生成的文件:")
    print("  output/triples.csv        - 所有三元组 (Excel可打开)")
    print("  output/nezha_triples.csv  - 哪吒相关三元组")
    print("  output/entities.json      - 所有实体")
    print("  output/relations.json     - 所有关系")
    print("  output/statistics.json    - 统计信息")
    print("  output/report.txt         - 文本报告")

def main():
    """主函数"""
    print("哪吒知识图谱构建系统")
    print("=" * 60)
    
    # 1. 加载文本
    text = load_text()
    if not text:
        return
    
    # 2. 提取实体
    entities = extract_entities(text)
    
    # 3. 提取关系
    relations = extract_relations(text, entities)
    
    # 4. 构建三元组
    triples, nezha_triples = build_triples(entities, relations)
    
    # 5. 保存结果
    save_results(entities, relations, triples, nezha_triples)
    
    # 6. 完成提示
    print_section("处理完成")
    print("恭喜！哪吒知识图谱构建成功！")
    print("\n下一步操作:")
    print("1. 用 Excel 打开 output/triples.csv 查看所有三元组")
    print("2. 查看 output/nezha_triples.csv 了解哪吒的核心关系")
    print("3. 查看 output/report.txt 获取分析报告")

if __name__ == "__main__":
    try:
        main()
        input("\n按 Enter 键退出...")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        input("按 Enter 键退出...")