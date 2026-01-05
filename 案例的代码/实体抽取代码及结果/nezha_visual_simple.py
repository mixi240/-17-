"""
哪吒知识图谱可视化 - 简化保证版
这个版本一定能运行！
"""

print("=" * 60)
print("哪吒知识图谱可视化程序 v1.0")
print("=" * 60)

# 1. 先检查并安装必要的库
print("\n🔧 检查运行环境...")
import sys
import subprocess

# 需要安装的库
required_libraries = ['matplotlib', 'networkx']

for lib in required_libraries:
    try:
        __import__(lib)
        print(f"✓ {lib} 已安装")
    except ImportError:
        print(f"✗ {lib} 未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])
            print(f"  ✓ {lib} 安装成功")
        except:
            print(f"  ✗ {lib} 安装失败，请手动安装: pip install {lib}")
            input("按回车继续尝试...")

# 2. 导入库（强制使用Tkinter显示）
try:
    import matplotlib
    matplotlib.use('TkAgg')  # 强制使用Tkinter，确保能弹出窗口
    import matplotlib.pyplot as plt
    import networkx as nx
    print("✓ 所有库导入成功")
except Exception as e:
    print(f"✗ 导入失败: {e}")
    input("按回车退出...")
    exit()

# 3. 哪吒关系数据
print("\n📊 加载关系数据...")
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

print(f"✓ 共加载 {len(relationships)} 条关系")

# 4. 创建关系图
print("\n🎨 创建关系图谱...")

# 创建有向图
G = nx.DiGraph()

# 添加所有关系
for source, relation, target in relationships:
    G.add_edge(source, target, label=relation)

# 5. 设置图形参数
plt.figure(figsize=(14, 10))
plt.title("哪吒人物关系知识图谱", fontsize=18, fontweight='bold', pad=20)

# 使用更好的布局
print("正在计算节点布局...")
pos = nx.spring_layout(G, seed=42, k=1.5)

# 6. 设置节点颜色和大小
node_colors = []
node_sizes = []

for node in G.nodes():
    if node == "哪吒":
        node_colors.append('#FF6B6B')  # 红色 - 主角
        node_sizes.append(3500)
    elif node in ["李靖", "殷夫人", "太乙真人", "申公豹", "敖丙"]:
        node_colors.append('#4ECDC4')  # 青色 - 人物
        node_sizes.append(2500)
    else:
        node_colors.append('#FFD166')  # 黄色 - 物品/概念
        node_sizes.append(2000)

# 7. 绘制节点
nx.draw_networkx_nodes(G, pos,
                      node_color=node_colors,
                      node_size=node_sizes,
                      alpha=0.9,
                      edgecolors='black',
                      linewidths=2)

# 8. 绘制边（关系线）
nx.draw_networkx_edges(G, pos,
                      edge_color='gray',
                      arrows=True,
                      arrowsize=25,
                      width=2,
                      alpha=0.7)

# 9. 绘制节点标签
nx.draw_networkx_labels(G, pos,
                       font_size=11,
                       font_weight='bold',
                       font_family='Microsoft YaHei')

# 10. 绘制边标签（关系类型）
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos,
                           edge_labels=edge_labels,
                           font_size=9,
                           font_family='Microsoft YaHei')

# 11. 添加图例
legend_text = """
图例说明：
🔴 红色：核心人物（哪吒）
🔵 青色：主要人物
🟡 黄色：物品/地点/概念
"""
plt.figtext(0.02, 0.02, legend_text,
           bbox=dict(boxstyle="round,pad=0.5",
                    facecolor="white",
                    edgecolor="gray",
                    alpha=0.9),
           fontsize=10)

plt.axis('off')
plt.tight_layout()

# 12. 保存图片
output_file = '哪吒关系图谱_最终版.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✅ 图片已保存：{output_file}")

# 13. 显示图片
print("\n📺 正在显示关系图...")
print("提示：会弹出一个新窗口显示图片，关闭窗口后程序继续")
plt.show()

# 14. 显示统计信息
print("\n" + "=" * 60)
print("📈 图谱统计信息")
print("=" * 60)

print(f"\n👥 节点信息（共 {G.number_of_nodes()} 个）：")
for i, node in enumerate(G.nodes(), 1):
    degree = G.degree(node)
    print(f"  {i:2}. {node:8} - 连接数：{degree}")

print(f"\n🔄 边信息（共 {G.number_of_edges()} 条）：")
for i, (source, relation, target) in enumerate(relationships, 1):
    print(f"  {i:2}. {source:5} → {relation:6} → {target}")

print(f"\n📊 关系类型统计：")
from collections import Counter
rel_counts = Counter([rel for _, rel, _ in relationships])
for rel_type, count in rel_counts.items():
    print(f"  • {rel_type:8}：{count:2} 条")

# 15. 生成文本报告
print(f"\n💾 生成报告文件...")
with open('可视化报告.txt', 'w', encoding='utf-8') as f:
    f.write("哪吒知识图谱可视化报告\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"生成时间：2024年\n")
    f.write(f"总节点数：{G.number_of_nodes()}\n")
    f.write(f"总边数：{G.number_of_edges()}\n\n")
    
    f.write("节点列表：\n")
    for node in sorted(G.nodes()):
        f.write(f"  • {node}\n")
    
    f.write("\n关系列表：\n")
    for source, relation, target in relationships:
        f.write(f"  • {source} --{relation}--> {target}\n")

print("✅ 报告已保存：可视化报告.txt")

print("\n" + "=" * 60)
print("🎉 所有任务完成！")
print("=" * 60)
print("\n已生成的文件：")
print("  1. 哪吒关系图谱_最终版.png - 关系图图片")
print("  2. 可视化报告.txt - 统计报告")
print("\n提示：如果图片窗口没弹出，请检查文件夹中的图片文件")
input("按回车键退出程序...")