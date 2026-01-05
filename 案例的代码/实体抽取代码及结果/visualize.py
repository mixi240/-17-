# visualize.py - 哪吒关系可视化
print("正在生成哪吒人物关系图...")

# 导入库
try:
    import matplotlib.pyplot as plt
    import networkx as nx
    print("✓ 库导入成功")
except ImportError as e:
    print(f"✗ 导入失败: {e}")
    print("请运行: pip install matplotlib networkx")
    input("按回车退出...")
    exit()

# 关系数据
relationships = [
    ("李靖", "父亲", "哪吒"),
    ("殷夫人", "母亲", "哪吒"),
    ("太乙真人", "师父", "哪吒"),
    ("哪吒", "朋友", "敖丙"),
    ("申公豹", "敌人", "哪吒"),
    ("哪吒", "拥有", "乾坤圈"),
    ("哪吒", "拥有", "混天绫"),
    ("哪吒", "居住地", "陈塘关"),
    ("敖丙", "身份", "龙族太子"),
    ("哪吒", "核心行动", "反抗命运"),
    ("哪吒", "参与", "对抗天劫"),
    ("敖丙", "参与", "对抗天劫"),
]

print(f"✓ 加载了 {len(relationships)} 条关系")

# 创建图
G = nx.DiGraph()

# 添加边
for source, relation, target in relationships:
    G.add_edge(source, target, label=relation)

print("✓ 创建了关系图")

# 设置图形
plt.figure(figsize=(12, 8))

# 计算布局
print("正在计算布局...")
pos = nx.spring_layout(G, seed=42)

# 设置节点颜色
node_colors = []
for node in G.nodes():
    if node == "哪吒":
        node_colors.append('red')
    elif node in ["李靖", "殷夫人", "太乙真人", "申公豹", "敖丙"]:
        node_colors.append('skyblue')
    else:
        node_colors.append('lightgreen')

# 绘制
print("正在绘制图形...")

# 绘制节点
nx.draw_networkx_nodes(G, pos, 
                      node_color=node_colors,
                      node_size=2000,
                      alpha=0.8)

# 绘制边
nx.draw_networkx_edges(G, pos,
                      edge_color='gray',
                      arrows=True,
                      arrowsize=20,
                      width=2)

# 绘制节点标签
nx.draw_networkx_labels(G, pos,
                       font_size=10,
                       font_weight='bold')

# 绘制边标签
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos,
                           edge_labels=edge_labels,
                           font_size=9)

# 标题
plt.title("哪吒人物关系知识图谱", fontsize=16, fontweight='bold', pad=20)
plt.axis('off')

# 图例
legend_text = """图例：
• 红色: 核心人物(哪吒)
• 蓝色: 主要人物
• 绿色: 物品/地点/概念"""
plt.figtext(0.02, 0.02, legend_text,
           bbox=dict(boxstyle="round,pad=0.5",
                    facecolor="white",
                    alpha=0.8))

plt.tight_layout()

# 保存图片
output_file = '哪吒关系图谱.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✅ 图片已保存为: {output_file}")

# 显示
print("✅ 正在显示关系图，关闭图片窗口继续...")
plt.show()

# 统计信息
print("\n" + "="*50)
print("📊 图谱统计信息：")
print(f"• 节点数量：{G.number_of_nodes()}")
print(f"• 边数量：{G.number_of_edges()}")

print("\n👥 所有节点：")
for i, node in enumerate(G.nodes(), 1):
    print(f"  {i:2}. {node}")

print("\n🔄 所有关系：")
for i, (source, relation, target) in enumerate(relationships, 1):
    print(f"  {i:2}. {source:5} → {relation:6} → {target}")

print("\n" + "="*50)
print("🎉 可视化完成！")
input("按回车键退出...")