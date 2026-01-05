import json
import networkx as nx
from pyvis.network import Network

# -------------------------------
# 1️⃣ 数据加载函数
# -------------------------------
def load_clean_text(json_path):
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    return data["cleaned"]

# -------------------------------
# 2️⃣ 构建图函数
# -------------------------------
def build_graph(texts):
    G = nx.Graph()
    for words in texts:
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                if G.has_edge(words[i], words[j]):
                    G[words[i]][words[j]]['weight'] += 1
                else:
                    G.add_edge(words[i], words[j], weight=1)
    return G

# -------------------------------
# 3️⃣ 可视化函数
# -------------------------------
def visualize_graph(G, html_name):
    net = Network(height="750px", width="100%", notebook=False)
    net.force_atlas_2based()  # 力导向布局

    # 添加节点
    for node, data in G.nodes(data=True):
        size = data.get('size', 1)  # 如果没有 size 字段默认 1
        net.add_node(node, label=node, size=size*3, color="red")

    # 添加边
    for source, target, data in G.edges(data=True):
        net.add_edge(source, target, value=data['weight'])

    # 输出 HTML
    net.show(html_name)
    print(f"知识图谱生成完成：{html_name}")

# -------------------------------
# 4️⃣ 主程序
# -------------------------------
if __name__ == "__main__":
    # 哪吒
    nezha_texts = load_clean_text("nezha_processed.json")
    G_nezha = build_graph(nezha_texts)
    visualize_graph(G_nezha, "nezha_knowledge_graph.html")

    # 封神
    fengshen_texts = load_clean_text("fengshen_processed.json")
    G_fengshen = build_graph(fengshen_texts)
    visualize_graph(G_fengshen, "fengshen_knowledge_graph.html")
