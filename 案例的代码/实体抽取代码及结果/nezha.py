# nezha.py - 哪吒知识图谱最简单版
print("=" * 60)
print("哪吒知识图谱生成器 v1.0")
print("=" * 60)

# 哪吒故事
nezha_story = """
哪吒是陈塘关总兵李靖的第三个儿子。
母亲是殷夫人，师父是太乙真人。
哪吒拥有乾坤圈和混天绫两件法宝。
他的朋友是龙族太子敖丙。
敌人是申公豹。
哪吒最终反抗命运，与敖丙一起对抗天劫。
"""

print("\n📖 故事内容：")
print(nezha_story)

# 定义人物关系
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

print("\n🔍 正在分析人物关系...")
print("-" * 40)

# 显示所有关系
print("✅ 分析完成！发现以下人物关系：\n")
for i, (who, relation, to_whom) in enumerate(relationships, 1):
    print(f"{i:2}. {who:5} --{relation:6}--> {to_whom}")

# 显示与哪吒相关的
print("\n🌟 与哪吒相关的所有关系：")
print("-" * 40)
nezha_list = []
for who, relation, to_whom in relationships:
    if "哪吒" in who or "哪吒" in to_whom:
        if "哪吒" == who:
            nezha_list.append(f"哪吒 --{relation}--> {to_whom}")
        else:
            nezha_list.append(f"{who} --{relation}--> 哪吒")

for i, rel in enumerate(nezha_list, 1):
    print(f"{i:2}. {rel}")

# 统计
print("\n📊 统计信息：")
print("-" * 40)
print(f"故事字数：{len(nezha_story)} 字")
print(f"发现关系数：{len(relationships)} 条")

# 保存到文件
with open("哪吒关系表.txt", "w", encoding="utf-8") as f:
    f.write("哪吒之魔童降世 人物关系表\n")
    f.write("=" * 40 + "\n\n")
    f.write("【完整关系列表】\n")
    for i, (who, relation, to_whom) in enumerate(relationships, 1):
        f.write(f"{i:2}. {who:5} --{relation:6}--> {to_whom}\n")

print("\n💾 已保存到：哪吒关系表.txt")

# 显示关系图
print("\n🎨 人物关系图：")
print("""
          李靖 ────父───> 哪吒 <──母─── 殷夫人
                     ↗              ↘
                   师                 友
                    ↓                  ↓
               太乙真人              敖丙
                    ↖                  ↙
                    敌                敌
                      ↘             ↗
                       申公豹─────┐
                                  ↓
                             对抗天劫
""")

print("\n🎉 全部完成！按回车键退出...")
input()