# phase2_complete.py
import json
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Patch
import matplotlib

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

def phase2_main():
    print("=" * 60)
    print("阶段二：命名实体识别与关系抽取")
    print("=" * 60)
    
    # ==================== 1. 实体识别 ====================
    print("\n1. 📋 实体识别")
    print("-" * 40)
    
    entities = {
        '人物': ['哪吒', '李靖', '殷夫人', '太乙真人', '敖丙', '龙王', '申公豹',
                '石矶娘娘', '杨戬', '雷震子', '姜子牙', '金吒', '木吒', '殷郊', '殷洪'],
        '法宝': ['混天绫', '乾坤圈', '风火轮', '火尖枪', '九龙神火罩'],
        '地点': ['陈塘关', '东海', '金光洞', '乾元山', '天庭'],
        '事件': ['哪吒降生', '大闹东海', '削骨还父', '莲花化身', '助周伐纣', '封神归位'],
        '组织': ['商朝', '周朝', '天庭', '截教', '阐教']
    }
    
    print(f"识别到 {len(entities)} 类实体：")
    total_entities = 0
    for category, items in entities.items():
        print(f"  ✅ {category}: {len(items)}个")
        total_entities += len(items)
        if category == '人物':
            print(f"      {', '.join(items)}")
    
    print(f"\n📊 实体总数: {total_entities}个")
    
    # ==================== 2. 关系抽取 ====================
    print("\n2. 🔗 关系抽取")
    print("-" * 40)
    
    relations = [
        # 家庭关系
        ('哪吒', '父亲', '李靖'),
        ('哪吒', '母亲', '殷夫人'),
        ('哪吒', '兄长', '金吒'),
        ('哪吒', '兄长', '木吒'),
        ('李靖', '妻子', '殷夫人'),
        
        # 师徒关系
        ('哪吒', '师父', '太乙真人'),
        ('太乙真人', '徒弟', '哪吒'),
        ('申公豹', '同门', '太乙真人'),
        
        # 朋友/战友关系
        ('哪吒', '朋友', '敖丙'),
        ('哪吒', '战友', '杨戬'),
        ('哪吒', '战友', '雷震子'),
        ('杨戬', '战友', '雷震子'),
        
        # 敌对关系
        ('哪吒', '敌人', '龙王'),
        ('哪吒', '敌人', '申公豹'),
        ('哪吒', '敌人', '石矶娘娘'),
        ('太乙真人', '敌人', '申公豹'),
        
        # 对抗击杀关系
        ('哪吒', '对抗', '龙王三太子'),
        ('哪吒', '击杀', '龙王三太子'),
        ('哪吒', '对抗', '石矶娘娘'),
        
        # 救赎复活关系
        ('哪吒', '救赎', '敖丙'),
        ('太乙真人', '复活', '哪吒'),
        
        # 身份转变关系
        ('哪吒', '身份转变', '从魔童到英雄'),
        ('敖丙', '关系转变', '从敌人到朋友'),
        
        # 拥有关系（人物-法宝）
        ('哪吒', '拥有法宝', '混天绫'),
        ('哪吒', '拥有法宝', '乾坤圈'),
        ('哪吒', '拥有法宝', '风火轮'),
        ('哪吒', '拥有法宝', '火尖枪'),
        ('太乙真人', '赐予法宝', '乾坤圈'),
        ('太乙真人', '赐予法宝', '混天绫'),
        
        # 地理位置关系
        ('李靖', '镇守', '陈塘关'),
        ('龙王', '统治', '东海'),
        ('太乙真人', '居住', '金光洞'),
        ('太乙真人', '修行地', '乾元山'),
        
        # 组织归属
        ('哪吒', '归属', '阐教'),
        ('太乙真人', '归属', '阐教'),
        ('申公豹', '归属', '截教'),
        ('石矶娘娘', '归属', '截教'),
        ('李靖', '效忠', '商朝'),
        ('哪吒', '助战', '周朝'),
    ]
    
    # 统计关系类型
    relation_types = set([r[1] for r in relations])
    print(f"抽取到 {len(relations)} 条关系，共 {len(relation_types)} 种关系类型：")
    print(f"  关系类型: {', '.join(sorted(relation_types))}")
    
    # ==================== 3. 事件节点建立 ====================
    print("\n3. 📅 事件节点建立")
    print("-" * 40)
    
    events = {
        '哪吒降生': {
            '时间': '商朝末年',
            '地点': '陈塘关',
            '参与者': ['哪吒', '李靖', '殷夫人', '太乙真人'],
            '结果': '灵珠子转世，出生即不凡',
            '关键物品': ['灵珠子']
        },
        '大闹东海': {
            '时间': '七岁时',
            '地点': '东海',
            '参与者': ['哪吒', '龙王三太子', '龙王'],
            '结果': '打死龙王三太子，抽龙筋',
            '关键物品': ['混天绫', '乾坤圈']
        },
        '削骨还父': {
            '时间': '七岁时（大闹东海后）',
            '地点': '陈塘关',
            '参与者': ['哪吒', '李靖', '殷夫人', '龙王'],
            '结果': '为不连累父母，自刎谢罪，肉身毁灭',
            '关键物品': ['宝剑']
        },
        '莲花化身': {
            '时间': '死后三日',
            '地点': '金光洞',
            '参与者': ['哪吒', '太乙真人'],
            '结果': '太乙真人用莲花莲藕重塑肉身，获得新生',
            '关键物品': ['莲花', '莲藕', '金丹']
        },
        '助周伐纣': {
            '时间': '商周交替时期',
            '地点': '各处战场',
            '参与者': ['哪吒', '姜子牙', '杨戬', '雷震子', '太乙真人'],
            '结果': '立下赫赫战功，成为伐纣先锋',
            '关键物品': ['风火轮', '火尖枪', '九龙神火罩']
        },
        '封神归位': {
            '时间': '封神大战后',
            '地点': '天庭',
            '参与者': ['哪吒', '姜子牙', '玉帝'],
            '结果': '被封为"三坛海会大神"，位列仙班',
            '关键物品': ['封神榜']
        }
    }
    
    print(f"建立 {len(events)} 个关键事件节点：")
    for event_name in events.keys():
        print(f"  ✅ {event_name}")
    
    # ==================== 4. 形成三元组结构 ====================
    print("\n4. 🔼 形成三元组结构")
    print("-" * 40)
    
    # 基础三元组
    triplets = relations.copy()
    
    # 添加事件相关三元组
    for event_name, event_info in events.items():
        triplets.append((event_name, '事件类型', '关键事件'))
        triplets.append((event_name, '发生时间', event_info['时间']))
        triplets.append((event_name, '发生地点', event_info['地点']))
        triplets.append((event_name, '事件结果', event_info['结果']))
        
        for participant in event_info['参与者']:
            triplets.append((participant, '参与事件', event_name))
            triplets.append((event_name, '涉及人物', participant))
        
        for item in event_info['关键物品']:
            triplets.append((event_name, '涉及物品', item))
    
    # 添加其他三元组
    additional_triplets = [
        # 人物属性
        ('哪吒', '称号', '三坛海会大神'),
        ('哪吒', '身份', '灵珠子转世'),
        ('哪吒', '前世', '灵珠子'),
        ('李靖', '称号', '托塔天王'),
        ('太乙真人', '称号', '乾元山金光洞太乙真人'),
        ('敖丙', '身份', '东海龙王三太子'),
        
        # 法宝属性
        ('混天绫', '类型', '法宝'),
        ('混天绫', '功能', '束缚敌人'),
        ('乾坤圈', '类型', '法宝'),
        ('乾坤圈', '功能', '攻击武器'),
        ('风火轮', '类型', '法宝'),
        ('风火轮', '功能', '飞行工具'),
        ('火尖枪', '类型', '法宝'),
        ('火尖枪', '功能', '近战武器'),
        
        # 事件关系
        ('大闹东海', '前因', '哪吒洗澡搅动东海'),
        ('大闹东海', '后果', '削骨还父'),
        ('削骨还父', '前因', '大闹东海'),
        ('削骨还父', '后果', '莲花化身'),
        ('莲花化身', '前因', '削骨还父'),
        ('莲花化身', '后果', '助周伐纣'),
    ]
    
    triplets.extend(additional_triplets)
    
    print(f"生成三元组总数: {len(triplets)} 个")
    print("\n示例三元组:")
    for i in range(10):  # 显示前10个示例
        print(f"  {triplets[i][0]} -- {triplets[i][1]} --> {triplets[i][2]}")
    
    # ==================== 5. 保存结果 ====================
    print("\n5. 💾 保存结果")
    print("-" * 40)
    
    result = {
        '项目': '哪吒知识图谱构建',
        '阶段': '阶段二：命名实体识别与关系抽取',
        '实体识别': entities,
        '关系抽取': relations,
        '事件节点': events,
        '三元组数据': triplets,
        '统计信息': {
            '实体类别数': len(entities),
            '实体总数': total_entities,
            '关系数量': len(relations),
            '关系类型数': len(relation_types),
            '事件节点数': len(events),
            '三元组总数': len(triplets)
        }
    }
    
    # 保存为JSON文件
    with open('nezha_knowledge_graph_phase2.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 保存三元组为CSV（便于导入图数据库）
    with open('nezha_triplets.csv', 'w', encoding='utf-8') as f:
        f.write('头实体,关系,尾实体\n')
        for triplet in triplets:
            f.write(f'{triplet[0]},{triplet[1]},{triplet[2]}\n')
    
    print(f"✅ JSON文件已保存: nezha_knowledge_graph_phase2.json")
    print(f"✅ CSV文件已保存: nezha_triplets.csv")
    
    # ==================== 6. 可视化 ====================
    print("\n6. 📊 生成可视化图谱")
    print("-" * 40)
    
    # 创建知识图谱可视化
    create_visualization(entities, relations, events, triplets)
    
    print("\n" + "=" * 60)
    print("阶段二完成！")
    print("=" * 60)
    print("\n📈 最终统计:")
    for key, value in result['统计信息'].items():
        print(f"  {key}: {value}")
    
    return result

def create_visualization(entities, relations, events, triplets):
    """创建可视化图谱"""
    
    # 创建一个图形
    plt.figure(figsize=(16, 12))
    G = nx.MultiDiGraph()
    
    # 添加节点（按类别）
    node_categories = {}
    for category, items in entities.items():
        for item in items:
            G.add_node(item, category=category)
            node_categories[item] = category
    
    # 添加事件节点
    for event_name in events.keys():
        G.add_node(event_name, category='事件')
        node_categories[event_name] = '事件'
    
    # 添加边（关系）
    for rel in relations:
        G.add_edge(rel[0], rel[2], relationship=rel[1])
    
    # 添加事件关系边
    for event_name in events.keys():
        for participant in events[event_name]['参与者']:
            if participant in G.nodes():
                G.add_edge(participant, event_name, relationship='参与事件')
                G.add_edge(event_name, participant, relationship='涉及人物')
    
    # 定义颜色映射
    category_colors = {
        '人物': '#4d96ff',    # 蓝色
        '法宝': '#6bcf7f',    # 绿色
        '地点': '#ffd166',    # 黄色
        '事件': '#a29bfe',    # 紫色
        '组织': '#ff9a76',    # 橙色
    }
    
    # 设置节点颜色
    node_colors = []
    for node in G.nodes():
        category = node_categories.get(node, '其他')
        node_colors.append(category_colors.get(category, '#cccccc'))
    
    # 手动布局 - 将不同类别的节点放在不同区域
    pos = {}
    
    # 人物节点放在中间
    people_nodes = [n for n in G.nodes() if node_categories.get(n) == '人物']
    for i, node in enumerate(people_nodes):
        angle = 2 * 3.14159 * i / len(people_nodes)
        radius = 2
        pos[node] = (radius * 3 * (i%3), radius * 2 * (i//3))
    
    # 哪吒放在中心
    if '哪吒' in pos:
        pos['哪吒'] = (0, 0)
    
    # 事件节点放在下方
    event_nodes = [n for n in G.nodes() if node_categories.get(n) == '事件']
    for i, node in enumerate(event_nodes):
        pos[node] = (-5 + i * 3, -3)
    
    # 其他节点放在周围
    other_nodes = [n for n in G.nodes() if n not in pos]
    for i, node in enumerate(other_nodes):
        row = i // 4
        col = i % 4
        pos[node] = (-8 + col * 5, 4 - row * 2)
    
    # 绘制图形
    plt.figure(figsize=(16, 12))
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, 
                          node_color=node_colors,
                          node_size=1500,
                          edgecolors='white',
                          linewidths=2)
    
    # 绘制边
    nx.draw_networkx_edges(G, pos,
                          edge_color='gray',
                          width=1.5,
                          alpha=0.6,
                          arrowsize=15)
    
    # 绘制节点标签
    labels = {}
    for node in G.nodes():
        labels[node] = node
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')
    
    # 添加图例
    legend_elements = []
    for category, color in category_colors.items():
        legend_elements.append(Patch(facecolor=color, edgecolor='white', label=category))
    
    plt.legend(handles=legend_elements, 
              loc='upper left',
              bbox_to_anchor=(1.02, 1),
              fontsize=11,
              title='实体类别',
              title_fontsize=12)
    
    # 添加标题和统计信息
    plt.title('哪吒知识图谱 - 阶段二：实体与关系可视化', 
              fontsize=20, fontweight='bold', pad=20)
    
    stats_text = f"""基于文本分析结果：
• 识别实体：{sum(len(v) for v in entities.values())}个
• 发现关系：{len(set([r[1] for r in relations]))}种
• 建立事件：{len(events)}个
• 生成三元组：{len(triplets)}个"""
    
    plt.text(-9, -5, stats_text, 
             fontsize=11, 
             ha='left', 
             va='center',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#ddd'))
    
    plt.xlim(-10, 10)
    plt.ylim(-6, 6)
    plt.axis('off')
    plt.tight_layout()
    
    # 保存图片
    plt.savefig('nezha_phase2_visualization.png', dpi=300, bbox_inches='tight')
    print("✅ 可视化图谱已保存: nezha_phase2_visualization.png")
    
    # 显示图片
    plt.show()

def export_for_neo4j():
    """为Neo4j图数据库导出数据"""
    print("\n7. 🗃️ 为图数据库准备数据")
    print("-" * 40)
    
    # 读取之前保存的数据
    with open('nezha_knowledge_graph_phase2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 创建节点CSV
    nodes_data = []
    node_id = 1
    
    # 添加实体节点
    for category, items in data['实体识别'].items():
        for item in items:
            nodes_data.append({
                'nodeId': f'n{node_id}',
                'name': item,
                'type': category,
                'label': category
            })
            node_id += 1
    
    # 添加事件节点
    for event_name in data['事件节点'].keys():
        nodes_data.append({
            'nodeId': f'n{node_id}',
            'name': event_name,
            'type': '事件',
            'label': '事件'
        })
        node_id += 1
    
    # 保存节点数据
    with open('neo4j_nodes.csv', 'w', encoding='utf-8') as f:
        f.write('nodeId:ID,name,:LABEL,type\n')
        for node in nodes_data:
            f.write(f'{node["nodeId"]},{node["name"]},{node["label"]},{node["type"]}\n')
    
    # 创建关系CSV
    relations_data = []
    rel_id = 1
    
    # 创建节点名称到ID的映射
    node_map = {node['name']: node['nodeId'] for node in nodes_data}
    
    # 添加关系
    for triplet in data['三元组数据']:
        if triplet[0] in node_map and triplet[2] in node_map:
            relations_data.append({
                ':START_ID': node_map[triplet[0]],
                ':END_ID': node_map[triplet[2]],
                ':TYPE': triplet[1].replace(' ', '_').upper(),
                'name': triplet[1]
            })
    
    # 保存关系数据
    with open('neo4j_relationships.csv', 'w', encoding='utf-8') as f:
        f.write(':START_ID,:END_ID,:TYPE,name\n')
        for rel in relations_data:
            f.write(f'{rel[":START_ID"]},{rel[":END_ID"]},{rel[":TYPE"]},{rel["name"]}\n')
    
    print("✅ Neo4j节点文件: neo4j_nodes.csv")
    print("✅ Neo4j关系文件: neo4j_relationships.csv")
    
    # 创建导入脚本
    import_script = """
// Neo4j 数据导入脚本
// 1. 首先导入节点
LOAD CSV WITH HEADERS FROM 'file:///neo4j_nodes.csv' AS row
CREATE (n:KnowledgeNode {id: row.nodeId, name: row.name, type: row.type})
SET n:row.label;

// 2. 然后导入关系
LOAD CSV WITH HEADERS FROM 'file:///neo4j_relationships.csv' AS row
MATCH (start:KnowledgeNode {id: row.START_ID})
MATCH (end:KnowledgeNode {id: row.END_ID})
CALL apoc.create.relationship(start, row.TYPE, {name: row.name}, end) YIELD rel
RETURN count(rel);

// 3. 创建索引（提高查询性能）
CREATE INDEX ON :KnowledgeNode(name);
CREATE INDEX ON :KnowledgeNode(type);
"""
    
    with open('neo4j_import.cypher', 'w', encoding='utf-8') as f:
        f.write(import_script)
    
    print("✅ Neo4j导入脚本: neo4j_import.cypher")
    print("\n📝 使用说明:")
    print("  1. 将CSV文件复制到Neo4j的import目录")
    print("  2. 在Neo4j Browser中运行导入脚本")
    print("  3. 或者使用: CALL apoc.import.csv(...)")

if __name__ == "__main__":
    # 运行主程序
    result = phase2_main()
    
    # 询问是否导出为图数据库格式
    export = input("\n是否导出为图数据库格式(Neo4j)? (y/n): ")
    if export.lower() == 'y':
        export_for_neo4j()
    
    print("\n🎉 阶段二全部任务完成！")
    print("下一步建议:")
    print("  1. 查看生成的JSON文件: nezha_knowledge_graph_phase2.json")
    print("  2. 查看可视化图片: nezha_phase2_visualization.png")
    print("  3. 进入阶段三: 知识图谱存储与查询")