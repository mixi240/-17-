import os
from snownlp import SnowNLP
from docx import Document
import pdfplumber
import jieba
from collections import Counter

# ======================
# 读取 Word
# ======================
def read_docx(path):
    doc = Document(path)
    text = []
    for p in doc.paragraphs:
        if p.text.strip():
            text.append(p.text.strip())
    return "\n".join(text)

# ======================
# 读取 PDF
# ======================
def read_pdf(path):
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text.append(t)
    return "\n".join(text)

# ======================
# 情感分析
# ======================
def sentiment_analysis(text):
    scores = []
    for line in text.split("\n"):
        line = line.strip()
        if len(line) > 5:
            scores.append(SnowNLP(line).sentiments)

    if not scores:
        return 0.5, "中性"

    avg = sum(scores) / len(scores)

    if avg > 0.6:
        label = "正向"
    elif avg < 0.4:
        label = "负向"
    else:
        label = "中性"

    return avg, label

# ======================
# 关键词提取
# ======================
def extract_keywords(text, top_n=10):
    words = jieba.lcut(text)
    words = [w for w in words if len(w) > 1]
    return Counter(words).most_common(top_n)

# ======================
# 主流程
# ======================
def main():
    base_dir = "data"
    results = []

    for root, _, files in os.walk(base_dir):
        for file in files:
            path = os.path.join(root, file)

            if file.endswith(".docx"):
                text = read_docx(path)
            elif file.endswith(".pdf"):
                text = read_pdf(path)
            else:
                continue

            score, label = sentiment_analysis(text)
            keywords = extract_keywords(text, 5)

            results.append((file, score, label, keywords))

    print("=" * 60)
    print("PDF / Word 情感分析结果")
    print("=" * 60)

    for r in results:
        print(f"\n文件名：{r[0]}")
        print(f"情感倾向：{r[2]}（得分 {r[1]:.3f}）")
        print("关键词：", ", ".join([k for k, _ in r[3]]))

if __name__ == "__main__":
    main()
