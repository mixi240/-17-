# fix_main.py - 自动修复main.py的编码问题
import os

print("正在修复 main.py 文件的编码设置...")

# 读取main.py内容
with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# 替换编码设置
old_csv_line1 = 'with open("output/triples.csv", "w", encoding="utf-8", newline=\'\') as f:'
new_csv_line1 = 'with open("output/triples.csv", "w", encoding="utf-8-sig", newline=\'\') as f:'

old_csv_line2 = 'with open("output/nezha_triples.csv", "w", encoding="utf-8", newline=\'\') as f:'
new_csv_line2 = 'with open("output/nezha_triples.csv", "w", encoding="utf-8-sig", newline=\'\') as f:'

# 进行替换
content = content.replace(old_csv_line1, new_csv_line1)
content = content.replace(old_csv_line2, new_csv_line2)

# 保存修复后的文件
with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✓ main.py 修复完成")
print("现在重新运行程序...")

# 重新运行
os.system("python main.py")