import matplotlib.pyplot as plt
import os

# ==================== 关键设置：解决中文显示问题 ====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

print("=" * 60)
print("哪吒关系图生成器 - 中文版")
print("=" * 60)

# 创建图形
fig, ax = plt.subplots(figsize=(12, 9))

# ==================== 1. 标题 ====================
ax.text(0.5, 0.95, '哪吒关系图谱', 
        fontsize=28, ha='center', va='center',
        fontweight='bold', color='darkred')

# ==================== 2. 中心节点 ====================
ax.text(0.5, 0.7, '哪吒', 
        fontsize=36, ha='center', va='center',
        fontweight='bold',
        bbox=dict(boxstyle='circle,pad=2', 
                 facecolor='#FF5252', 
                 edgecolor='#D32F2F', 
                 linewidth=4,
                 alpha=0.9))

# ==================== 3. 关系节点 ====================
# 定义所有关系
relationships = [
    # (文本, x位置, y位置, 颜色, 关系类型)
    ('李靖\n（父亲）', 0.25, 0.88, '#42A5F5', '家庭关系'),
    ('殷夫人\n（母亲）', 0.75, 0.88, '#EC407A', '家庭关系'),
    ('太乙真人\n（师父）', 0.15, 0.65, '#66BB6A', '师徒关系'),
    ('敖丙\n（朋友）', 0.85, 0.65, '#FFCA28', '朋友关系'),
    ('龙王\n（敌人）', 0.1, 0.42, '#EF5350', '敌对关系'),
    ('申公豹\n（敌人）', 0.9, 0.42, '#EF5350', '敌对关系')
]

# 绘制关系节点
for text, x, y, color, rel_type in relationships:
    # 绘制节点
    ax.text(x, y, text, 
            fontsize=18, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=1', 
                     facecolor=color + 'CC',  # CC是透明度
                     edgecolor=color,
                     linewidth=3,
                     alpha=0.8))
    
    # 绘制连接线
    ax.annotate('', xy=(x, y - 0.05), xytext=(0.5, 0.76),
                arrowprops=dict(arrowstyle='->',
                               color='#666666',
                               linewidth=2.5,
                               alpha=0.7,
                               connectionstyle="arc3,rad=0.2"))

# ==================== 4. 作品信息 ====================
works_box = ax.text(0.5, 0.25, 
                   '主要作品\n《封神演义》 《西游记》 《哪吒闹海》\n《魔童降世》 《魔童闹海》 《哪吒传奇》',
                   fontsize=14, ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=1',
                            facecolor='#E3F2FD',
                            edgecolor='#2196F3',
                            linewidth=2))

# ==================== 5. 统计信息 ====================
stats_text = ax.text(0.5, 0.1, 
                    '基于文本分析结果\n识别实体: 18个 | 发现关系: 13种 | 相关作品: 7部',
                    fontsize=12, ha='center', va='center',
                    style='italic',
                    color='#666666')

# ==================== 6. 图例 ====================
legend_text = '''
图例说明：
● 红色：核心人物
● 蓝色：家庭关系  
● 绿色：师徒关系
● 黄色：朋友关系
● 红色：敌对关系
● 浅蓝：相关作品
'''
ax.text(0.02, 0.02, legend_text,
        fontsize=10, va='bottom',
        bbox=dict(boxstyle='round,pad=0.5',
                 facecolor='#F5F5F5',
                 edgecolor='#BDBDBD',
                 alpha=0.7))

# ==================== 7. 设置图形属性 ====================
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')  # 关闭坐标轴

# ==================== 8. 保存图片 ====================
# 确保results文件夹存在
os.makedirs('results', exist_ok=True)

# 保存为PNG
save_path_png = 'results/nezha_chinese_fixed.png'
plt.savefig(save_path_png, 
           dpi=300, 
           bbox_inches='tight',
           facecolor='white',
           transparent=False)

# 保存为PDF（矢量格式，更清晰）
save_path_pdf = 'results/nezha_chinese_fixed.pdf'
plt.savefig(save_path_pdf, 
           format='pdf',
           bbox_inches='tight',
           facecolor='white')

# ==================== 9. 显示图片 ====================
plt.tight_layout()
plt.show()

# ==================== 10. 输出结果信息 ====================
print("\n" + "=" * 60)
print("✓ 生成完成！")
print("=" * 60)
print(f"图片已保存到:")
print(f"1. {os.path.abspath(save_path_png)}")
print(f"2. {os.path.abspath(save_path_pdf)}")
print("\n文件信息:")
import datetime
file_size_png = os.path.getsize(save_path_png) if os.path.exists(save_path_png) else 0
file_size_pdf = os.path.getsize(save_path_pdf) if os.path.exists(save_path_pdf) else 0
print(f"• PNG文件大小: {file_size_png:,} 字节 ({file_size_png/1024:.1f} KB)")
print(f"• PDF文件大小: {file_size_pdf:,} 字节 ({file_size_pdf/1024:.1f} KB)")
print(f"• 生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n下一步:")
print("1. 打开 results/ 文件夹")
print("2. 双击 nezha_chinese_fixed.png 查看图片")
print("3. 如果PNG不清晰，可以打开PDF版本")
print("=" * 60)