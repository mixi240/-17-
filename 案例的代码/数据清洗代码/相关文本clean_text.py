import pdfplumber
import os

pdf_folder = "data/pdf"
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(pdf_folder):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, file)
        text_all = ""

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_all += text + "\n"

        out_path = os.path.join(output_folder, file.replace(".pdf", ".txt"))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text_all)

        print(f"{file} 提取完成")
from docx import Document

word_folder = "data/word"

for file in os.listdir(word_folder):
    if file.endswith(".docx"):
        doc_path = os.path.join(word_folder, file)
        doc = Document(doc_path)

        text_all = ""
        for para in doc.paragraphs:
            text_all += para.text + "\n"

        out_path = os.path.join("output", file.replace(".docx", ".txt"))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text_all)

        print(f"{file} 提取完成")
import pandas as pd

data = []

for file in os.listdir("output"):
    if file.endswith(".txt"):
        with open(os.path.join("output", file), encoding="utf-8") as f:
            content = f.read()
            data.append({
                "文件名": file,
                "文本内容": content
            })

df = pd.DataFrame(data)
df.to_csv("output/clean_data.csv", index=False, encoding="utf-8-sig")
import pandas as pd

data = []

for file in os.listdir("output"):
    if file.endswith(".txt"):
        with open(os.path.join("output", file), encoding="utf-8") as f:
            content = f.read()
            data.append({
                "文件名": file,
                "文本内容": content
            })

df = pd.DataFrame(data)
df.to_csv("output/clean_data.csv", index=False, encoding="utf-8-sig")
with open("all_text.txt", "w", encoding="utf-8") as out:
    for file in os.listdir("output"):
        with open("output/" + file, encoding="utf-8") as f:
            out.write(f.read() + "\n\n")
