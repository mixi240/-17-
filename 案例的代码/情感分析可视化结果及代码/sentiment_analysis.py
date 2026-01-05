import json

# 读取哪吒
with open("nezha_processed.json", encoding="utf-8") as f:
    nezha_data = json.load(f)

# 读取封神
with open("fengshen_processed.json", encoding="utf-8") as f:
    fengshen_data = json.load(f)

print("哪吒字幕条数：", len(nezha_data["cleaned"]))
print("封神字幕条数：", len(fengshen_data["cleaned"]))
from snownlp import SnowNLP

def sentiment_scores(texts):
    scores = []
    for t in texts:
        if t.strip():
            s = SnowNLP(t)
            scores.append(s.sentiments)
    return scores

nezha_scores = sentiment_scores(nezha_data["cleaned"])
fengshen_scores = sentiment_scores(fengshen_data["cleaned"])

print("哪吒情感样例：", nezha_scores[:5])
print("封神情感样例：", fengshen_scores[:5])
def classify(scores):
    pos = sum(1 for s in scores if s > 0.6)
    neu = sum(1 for s in scores if 0.4 <= s <= 0.6)
    neg = sum(1 for s in scores if s < 0.4)
    return pos, neu, neg

nezha_dist = classify(nezha_scores)
fengshen_dist = classify(fengshen_scores)

print("哪吒 情感分布（正 中 负）：", nezha_dist)
print("封神 情感分布（正 中 负）：", fengshen_dist)
