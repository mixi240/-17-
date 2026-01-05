"""
哪吒实体关系抽取系统 - 极简版本
"""

import re
import json
import os

class NeZhaExtractor:
    def __init__(self):
        # 哪吒相关的人物列表
        self.characters = [
            '哪吒', '李靖', '殷夫人', '太乙真人', '敖丙', '申公豹',
            '元始天尊', '纣王', '姬发', '姜子牙', '孙悟空', '龙王',
            '无量仙翁', '石矶娘娘', '伯邑考', '周文王', '杨戬', '妲己'
        ]
        
        # 相关作品
        self.works = [
            '封神演义', '西游记', '哪吒闹海', '哪吒之魔童降世',
            '哪吒之魔童闹海', '哪吒传奇', '大闹天宫'
        ]
    
    def load_text(self, file_path):
        """读取文本文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def find_entities(self, text):
        """找出文本中的人物和作品"""
        found_chars = []
        found_works = []
        
        for char in self.characters:
            if char in text:
                found_chars.append(char)
        
        for work in self.works:
            if work in text:
                found_works.append(work)
        
        return found_chars, found_works
    
    def extract_relations(self, text):
        """提取哪吒的关系"""
        relations = []
        
        # 1. 父子关系
        if '李靖' in text and ('父亲' in text or '父子' in text):
            relations.append(['哪吒', '父亲', '李靖'])
        
        # 2. 母子关系
        if '殷夫人' in text and ('母亲' in text or '母子' in text):
            relations.append(['哪吒', '母亲', '殷夫人'])
        
        # 3. 师徒关系
        if '太乙真人' in text and ('师父' in text or '师傅' in text):
            relations.append(['哪吒', '师父', '太乙真人'])
        
        # 4. 朋友关系
        if '敖丙' in text and '朋友' in text:
            relations.append(['哪吒', '朋友', '敖丙'])
        
        # 5. 敌人关系
        if '龙王' in text and ('敌人' in text or '对抗' in text):
            relations.append(['哪吒', '敌人', '龙王'])
        
        if '申公豹' in text and ('敌人' in text or '对抗' in text):
            relations.append(['哪吒', '敌人', '申公豹'])
        
        # 6. 作品关系
        for work in self.works:
            if work in text:
                relations.append(['哪吒', '出现在', work])
        
        return relations
    
    def run(self, input_file):
        """运行抽取程序"""
        print("哪吒实体关系抽取开始...")
        print("=" * 40)
        
        # 1. 读取文件
        text = self.load_text(input_file)
        print(f"读取文件: {os.path.basename(input_file)}")
        print(f"文本长度: {len(text)} 字符")
        
        # 2. 抽取实体
        characters, works = self.find_entities(text)
        print(f"\n找到 {len(characters)} 个人物:")
        print(", ".join(characters))
        print(f"\n找到 {len(works)} 部作品:")
        print(", ".join(works))
        
        # 3. 抽取关系
        relations = self.extract_relations(text)
        print(f"\n找到 {len(relations)} 条关系:")
        
        # 4. 显示结果
        for i, rel in enumerate(relations, 1):
            print(f"{i:2d}. {rel[0]} -- {rel[1]} -- {rel[2]}")
        
        # 5. 保存结果
        self.save_results(characters, works, relations)
        
        return characters, works, relations
    
    def save_results(self, characters, works, relations):
        """保存结果到文件"""
        # 创建 results 文件夹（如果不存在）
        if not os.path.exists('results'):
            os.makedirs('results')
        
        # 保存为文本文件
        with open('results/nezha_results.txt', 'w', encoding='utf-8') as f:
            f.write("哪吒实体关系抽取结果\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("一、人物实体:\n")
            for char in characters:
                f.write(f"  • {char}\n")
            
            f.write("\n二、相关作品:\n")
            for work in works:
                f.write(f"  • {work}\n")
            
            f.write("\n三、关系三元组:\n")
            for rel in relations:
                f.write(f"  ({rel[0]}, {rel[1]}, {rel[2]})\n")
        
        print(f"\n结果已保存到: results/nezha_results.txt")
        
        # 保存为JSON
        result_data = {
            'characters': characters,
            'works': works,
            'relations': [
                {'subject': r[0], 'relation': r[1], 'object': r[2]}
                for r in relations
            ]
        }
        
        with open('results/nezha_results.json', 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        print(f"JSON格式已保存到: results/nezha_results.json")

def main():
    """主程序"""
    print("=" * 50)
    print("哪吒实体关系抽取系统 v1.0")
    print("=" * 50)
    
    # 检查文件是否存在
    text_file = "data/all_text.txt"
    
    if not os.path.exists(text_file):
        print(f"错误：找不到文件 {text_file}")
        print("\n请确保：")
        print("1. 项目结构正确：")
        print("   nezha_entity_extraction/")
        print("   ├── data/all_text.txt  ← 文件应该在这里")
        print("   ├── src/extractor.py")
        print("   └── results/")
        print("\n2. all_text.txt 文件在 data/ 文件夹中")
        return
    
    # 创建提取器并运行
    extractor = NeZhaExtractor()
    extractor.run(text_file)
    
    print("\n" + "=" * 50)
    print("抽取完成！")
    print("请打开 results/ 文件夹查看结果文件")
    print("=" * 50)

if __name__ == "__main__":
    main()