# nezha_graph.py - 哪吒关系图谱完整代码
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Patch

# 创建图形
plt.figure(figsize=(14, 10))
G = nx.Graph()

# 定义节点和关系
nodes = {
    '哪吒': {'type': 'core', 'pos': (0, 0)},
    '李靖': {'type': 'family', 'pos': (-2, 1.5)},
    '殷夫人': {'type': 'family', 'pos': (2, 1.5)},
    '太乙真人': {'type': 'master', 'pos': (-2, 0)},
    '敖丙': {'type': 'friend', 'pos': (2, 0)},
    '龙王': {'type': 'enemy', 'pos': (-2, -1.5)},
    '申公豹': {'type': 'enemy', 'pos': (2, -1.5)},
}

# 添加节点
for node, info in nodes.items():
    G.add_node(node, node_type=info['type'])

# 添加边（关系）
edges = [
    ('哪吒', '李靖', '父子'),
    ('哪吒', '殷夫人', '母子'),
    ('哪吒', '太乙真人', '师徒'),
    ('哪吒', '敖丙', '朋友'),
    ('哪吒', '龙王', '敌对'),
    ('哪吒', '申公豹', '敌对'),
    ('申公豹', '龙王', '联盟'),
]

for edge in edges:
    G.add_edge(edge[0], edge[1], relationship=edge[2])

# 设置节点颜色和大小
node_colors = {
    'core': '#ff6b6b',      # 红色 - 核心人物
    'family': '#4d96ff',    # 蓝色 - 家庭
    'master': '#6bcf7f',    # 绿色 - 师徒
    'friend': '#ffd166',    # 黄色 - 朋友
    'enemy': '#ff9a76',     # 橙色 - 敌对
}

node_sizes = {
    'core': 3500,
    'family': 2000,
    'master': 2000,
    'friend': 2000,
    'enemy': 2000,
}

# 获取节点颜色和大小
node_color_list = [node_colors[G.nodes[node]['node_type']] for node in G.nodes()]
node_size_list = [node_sizes[G.nodes[node]['node_type']] for node in G.nodes()]

# 获取位置
pos = {node: nodes[node]['pos'] for node in nodes.keys()}

# 绘制图形
plt.figure(figsize=(14, 12))

# 1. 绘制节点
nx.draw_networkx_nodes(G, pos, 
                       node_color=node_color_list,
                       node_size=node_size_list,
                       edgecolors='white',
                       linewidths=2)

# 2. 绘制边 - 实线
solid_edges = [edge for edge in edges if edge[2] != '联盟']
edge_labels = {(edge[0], edge[1]): edge[2] for edge in solid_edges}
nx.draw_networkx_edges(G, pos, 
                       edgelist=[(edge[0], edge[1]) for edge in solid_edges],
                       width=2, 
                       alpha=0.7,
                       edge_color='gray')

# 3. 绘制边 - 虚线（联盟关系）
dashed_edges = [edge for edge in edges if edge[2] == '联盟']
nx.draw_networkx_edges(G, pos, 
                       edgelist=[(edge[0], edge[1]) for edge in dashed_edges],
                       width=2, 
                       alpha=0.5,
                       edge_color='gray',
                       style='dashed')

# 4. 绘制节点标签（带关系说明）
for node, (x, y) in pos.items():
    node_type = G.nodes[node]['node_type']
    if node_type == 'core':
        label = f'{node}\n(核心人物)'
    elif node_type == 'family':
        if node == '李靖':
            label = f'{node}\n(父亲)'
        else:
            label = f'{node}\n(母亲)'
    elif node_type == 'master':
        label = f'{node}\n(师父)'
    elif node_type == 'friend':
        label = f'{node}\n(朋友)'
    elif node_type == 'enemy':
        label = f'{node}\n(敌人)'
    
    plt.text(x, y, label, 
             fontsize=12, 
             fontweight='bold',
             ha='center', 
             va='center',
             color='white' if node_type in ['core', 'family', 'master'] else 'black')

# 5. 绘制边标签
nx.draw_networkx_edge_labels(G, pos, 
                             edge_labels=edge_labels,
                             font_size=10,
                             font_weight='bold')

# 6. 添加相关作品模块
works = ['《封神演义》', '《西游记》', '《哪吒闹海》', 
         '《魔童降世》', '《魔童闹海》', '《哪吒传奇》']

works_y = -2.5
for i, work in enumerate(works):
    x = -2.5 + i * 1.0
    plt.gca().add_patch(plt.Rectangle((x-0.4, works_y-0.15), 0.8, 0.3, 
                                      color='#a29bfe', alpha=0.8, ec='#6c5ce7', lw=2))
    plt.text(x, works_y, work, fontsize=10, ha='center', va='center', color='white', fontweight='bold')

plt.text(0, works_y-0.5, '主要作品', fontsize=12, ha='center', va='center', fontweight='bold')

# 7. 添加连接线（从哪吒到作品）
plt.plot([0, 0], [-1.8, works_y+0.15], 'k--', alpha=0.3, linewidth=1)

# 8. 添加图例
legend_elements = [
    Patch(facecolor='#ff6b6b', edgecolor='white', label='核心人物'),
    Patch(facecolor='#4d96ff', edgecolor='white', label='家庭关系'),
    Patch(facecolor='#6bcf7f', edgecolor='white', label='师徒关系'),
    Patch(facecolor='#ffd166', edgecolor='white', label='朋友关系'),
    Patch(facecolor='#ff9a76', edgecolor='white', label='敌对关系'),
    Patch(facecolor='#a29bfe', edgecolor='white', label='相关作品'),
]

plt.legend(handles=legend_elements, 
           loc='upper right', 
           bbox_to_anchor=(1.15, 1),
           fontsize=11,
           title='图例说明',
           title_fontsize=12)

# 9. 添加数据统计
stats_text = '基于文本分析结果\n识别实体：18个 | 发现关系：13种 | 相关作品：7部'
plt.text(0, -3.2, stats_text, 
         fontsize=11, 
         ha='center', 
         va='center',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#ddd'))

# 设置图形属性
plt.title('哪吒关系图谱', fontsize=20, fontweight='bold', pad=20)
plt.xlim(-3.5, 3.5)
plt.ylim(-3.5, 2.5)
plt.axis('off')
plt.tight_layout()

# 保存图片
plt.savefig('nezha_relationship_graph.png', dpi=300, bbox_inches='tight')
plt.show()

print("关系图谱已生成并保存为 'nezha_relationship_graph.png'")