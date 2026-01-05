# -*- coding: utf-8 -*-
"""
文献情感差异分析工具
可以直接运行生成所有分析图片
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import jieba
from collections import Counter
import os
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 1. 创建数据（直接使用你提供的数据）
def create_data():
    """创建示例数据"""
    data = {
        '文件名': [
            '哪吒形象研究源流述略_张茗.pdf',
            '三重视角下哪吒形象的立体建构 —— 以电影《哪吒之魔童闹海》为例_李妙然.pdf',
            '从"神化"到"人化"_哪吒动画的形象变迁、叙事演进与文化表达_王莉.pdf',
            '从《哪吒之魔童闹海》看中国传统文化的现代转译_颜畅.pdf',
            '从《哪吒闹海》到《魔童降世》：角色设计的解构与重构_李欠欠.pdf',
            '从视觉建构到认知重构：《哪吒之魔童闹海》的视觉修辞路径研究_刘浩然.pdf',
            '叛逆英雄的祛魅与再神圣化：哪吒形象的叙事话语变迁与身份政治转型_刘秀梅.pdf',
            '国产动画电影中经典神话人物形象演变与文化意蕴探赜_徐锦博.pdf',
            '数字媒介下古典神话的当代重构 —— 以《哪吒》魔童系列电影为例_刘欣.pdf',
            '专访｜《封神第一部》导演乌尔善："先从人间开始".docx',
            '相关解读.docx',
            '饺子看法.docx'
        ],
        '情感倾向': [
            '正向（得分 0.959）', '正向（得分 0.918）', '正向（得分 0.791）',
            '正向（得分 0.953）', '正向（得分 0.848）', '正向（得分 0.953）',
            '正向（得分 0.799）', '正向（得分 0.894）', '正向（得分 0.906）',
            '正向（得分 0.949）', '正向（得分 0.973）', '正向（得分 0.871）'
        ],
        '关键词': [
            '哪吒，形象，研究，文化，相关',
            '哪吒，形象，凝视，自我，主体',
            '哪吒，动画，叙事，文化，形象',
            '哪吒，文化，叙事，传统，影片',
            '角色，哪吒，设计，敖丙，形象',
            '视觉，哪吒，修辞，认知，通过',
            '哪吒，文化，传统，叙事，技术',
            '神话，文化，传统，人物，神性',
            '哪吒，神话，古典，电影，文化',
            '电影，一个，我们，封神，中国',
            '哪吒，这个，李靖，就是，故事',
            '一个，那个，哪吒，其实，时代'
        ]
    }
    return pd.DataFrame(data)

# 2. 数据预处理函数
def preprocess_data(df):
    """预处理数据：提取情感得分、分类文献类型"""
    
    # 提取情感得分
    df['情感得分'] = df['情感倾向'].str.extract(r'(\d+\.\d+)').astype(float)
    
    # 定义文献类型分类函数
    def classify_document(filename):
        filename_lower = filename.lower()
        
        # 首先判断文件格式
        if filename.endswith('.docx'):
            if '专访' in filename or '访谈' in filename:
                return '访谈类'
            elif '解读' in filename or '看法' in filename:
                return '评论类'
            else:
                return '普通文档'
        
        # PDF文献的分类逻辑
        if any(word in filename_lower for word in ['研究', '述略', '探赜', '分析']):
            return '学术研究'
        elif any(word in filename_lower for word in ['视角', '建构', '路径', '理论']):
            return '理论分析'
        elif any(word in filename_lower for word in ['变迁', '演变', '重构', '转型']):
            return '演变分析'
        elif any(word in filename_lower for word in ['转译', '表达', '意蕴', '文化']):
            return '文化分析'
        elif any(word in filename_lower for word in ['设计', '视觉', '修辞', '技术']):
            return '技术分析'
        elif any(word in filename_lower for word in ['电影', '动画', '影片']):
            return '影视分析'
        else:
            return '其他文献'
    
    # 应用分类
    df['文献类型'] = df['文件名'].apply(classify_document)
    
    # 提取关键词列表
    df['关键词列表'] = df['关键词'].str.split('，')
    
    return df

# 3. 生成关键词词云
def create_keyword_wordcloud(df, save_path='wordcloud.png'):
    """生成关键词词云图"""
    
    # 合并所有关键词
    all_keywords = []
    for keywords in df['关键词列表']:
        all_keywords.extend(keywords)
    
    # 统计词频
    keyword_freq = Counter(all_keywords)
    
    # 创建词云
    plt.figure(figsize=(12, 8))
    
    # 简单的词云（不需要jieba分词，因为已经是关键词）
    text = ' '.join(all_keywords)
    
    wordcloud = WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf',  # Windows系统
        # font_path='/System/Library/Fonts/PingFang.ttc',  # Mac系统
        width=800,
        height=600,
        background_color='white',
        max_words=50,
        contour_width=1,
        contour_color='steelblue'
    ).generate(text)
    
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('文献关键词词云图', fontsize=16, fontweight='bold')
    
    # 保存图片
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"词云图已保存到: {save_path}")
    return keyword_freq

# 4. 生成文献类型情感对比图
def create_sentiment_comparison_charts(df, save_dir='output'):
    """生成文献类型情感对比的多张图表"""
    
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    # 统计各类型文献数量
    type_counts = df['文献类型'].value_counts()
    
    # 按文献类型分组统计情感得分
    type_stats = df.groupby('文献类型').agg({
        '情感得分': ['count', 'mean', 'std', 'min', 'max']
    }).round(3)
    
    # 重命名列
    type_stats.columns = ['数量', '平均分', '标准差', '最低分', '最高分']
    type_stats = type_stats.sort_values('平均分', ascending=False)
    
    print("=" * 60)
    print("各文献类型情感得分统计:")
    print("=" * 60)
    print(type_stats)
    print("\n" + "=" * 60)
    
    # 创建多子图展示
    fig = plt.figure(figsize=(18, 12))
    
    # 1. 箱线图（展示分布）
    ax1 = plt.subplot(2, 3, 1)
    sns.boxplot(x='文献类型', y='情感得分', data=df, 
                order=type_stats.index.tolist(),
                palette='Set2')
    plt.title('文献类型情感得分分布（箱线图）', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.ylim(0.75, 1.0)
    plt.grid(True, alpha=0.3)
    
    # 添加数据点
    for i, doc_type in enumerate(type_stats.index):
        type_data = df[df['文献类型'] == doc_type]['情感得分']
        x_pos = np.random.normal(i, 0.08, size=len(type_data))
        plt.scatter(x_pos, type_data, alpha=0.6, s=50, edgecolor='black', linewidth=0.5)
    
    # 2. 平均分柱状图
    ax2 = plt.subplot(2, 3, 2)
    bars = plt.bar(range(len(type_stats)), type_stats['平均分'], 
                   color=plt.cm.Set2(np.linspace(0, 1, len(type_stats))))
    plt.title('各文献类型平均情感得分', fontsize=14, fontweight='bold')
    plt.xticks(range(len(type_stats)), type_stats.index, rotation=45)
    plt.ylabel('平均情感得分')
    plt.ylim(0.7, 1.0)
    plt.grid(True, axis='y', alpha=0.3)
    
    # 在柱子上添加数值
    for i, (bar, value) in enumerate(zip(bars, type_stats['平均分'])):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height()+0.005, 
                f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # 3. 文献数量饼图
    ax3 = plt.subplot(2, 3, 3)
    colors = plt.cm.Paired(np.linspace(0, 1, len(type_counts)))
    wedges, texts, autotexts = plt.pie(type_counts.values, 
                                       labels=type_counts.index,
                                       autopct='%1.1f%%',
                                       startangle=90,
                                       colors=colors)
    plt.title('各文献类型数量占比', fontsize=14, fontweight='bold')
    
    # 4. 小提琴图（展示密度分布）
    ax4 = plt.subplot(2, 3, 4)
    sns.violinplot(x='文献类型', y='情感得分', data=df,
                   order=type_stats.index.tolist(),
                   palette='Set3', inner='quartile')
    plt.title('文献类型情感得分密度分布（小提琴图）', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.ylim(0.75, 1.0)
    plt.grid(True, alpha=0.3)
    
    # 5. 雷达图（多维对比）
    ax5 = plt.subplot(2, 3, 5, projection='polar')
    categories = type_stats.index.tolist()
    N = len(categories)
    
    # 标准化数据用于雷达图
    values = type_stats['平均分'].values
    values_normalized = (values - values.min()) / (values.max() - values.min())
    
    # 重复第一个值以闭合雷达图
    values_normalized = np.concatenate((values_normalized, [values_normalized[0]]))
    
    # 计算角度
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # 闭合
    
    # 绘制雷达图
    ax5.plot(angles, values_normalized, 'o-', linewidth=2)
    ax5.fill(angles, values_normalized, alpha=0.25)
    ax5.set_xticks(angles[:-1])
    ax5.set_xticklabels(categories, fontsize=10)
    ax5.set_title('文献类型情感得分对比（雷达图）', fontsize=14, fontweight='bold', pad=20)
    
    # 6. 散点图：情感得分分布
    ax6 = plt.subplot(2, 3, 6)
    for i, doc_type in enumerate(type_stats.index):
        type_data = df[df['文献类型'] == doc_type]
        plt.scatter(type_data['情感得分'], [i]*len(type_data), 
                   label=doc_type, s=100, alpha=0.7)
    
    plt.title('各文献情感得分散点分布', fontsize=14, fontweight='bold')
    plt.xlabel('情感得分')
    plt.yticks(range(len(type_stats)), type_stats.index)
    plt.grid(True, alpha=0.3)
    plt.xlim(0.75, 1.0)
    
    plt.tight_layout()
    
    # 保存图片
    comparison_path = os.path.join(save_dir, 'sentiment_comparison.png')
    plt.savefig(comparison_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"对比图表已保存到: {comparison_path}")
    
    return type_stats

# 5. 生成详细统计报告图
def create_detailed_statistics(df, type_stats, save_dir='output'):
    """生成详细的统计分析图表"""
    
    # 创建热力图：文献类型 vs 关键词频率
    fig = plt.figure(figsize=(16, 10))
    
    # 1. 热力图：文献类型与关键词的关系
    ax1 = plt.subplot(2, 2, 1)
    
    # 获取所有关键词
    all_keywords = []
    for keywords in df['关键词列表']:
        all_keywords.extend(keywords)
    top_keywords = [word for word, count in Counter(all_keywords).most_common(10)]
    
    # 创建热力图数据
    heatmap_data = pd.DataFrame(0, index=type_stats.index, columns=top_keywords)
    for doc_type in type_stats.index:
        type_df = df[df['文献类型'] == doc_type]
        for keywords in type_df['关键词列表']:
            for keyword in keywords:
                if keyword in top_keywords:
                    heatmap_data.loc[doc_type, keyword] += 1
    
    sns.heatmap(heatmap_data, annot=True, cmap='YlOrRd', linewidths=0.5,
                cbar_kws={'label': '出现次数'})
    plt.title('文献类型与高频关键词关联热力图', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    
    # 2. 情感得分分布直方图
    ax2 = plt.subplot(2, 2, 2)
    plt.hist(df['情感得分'], bins=10, alpha=0.7, color='skyblue', edgecolor='black')
    plt.xlabel('情感得分')
    plt.ylabel('文献数量')
    plt.title('所有文献情感得分分布', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # 添加均值和标准差线
    mean_score = df['情感得分'].mean()
    std_score = df['情感得分'].std()
    plt.axvline(mean_score, color='red', linestyle='--', linewidth=2, label=f'均值: {mean_score:.3f}')
    plt.axvline(mean_score + std_score, color='orange', linestyle=':', linewidth=1.5, label=f'±1标准差')
    plt.axvline(mean_score - std_score, color='orange', linestyle=':', linewidth=1.5)
    plt.legend()
    
    # 3. 累计分布图
    ax3 = plt.subplot(2, 2, 3)
    sorted_scores = np.sort(df['情感得分'])
    y_vals = np.arange(1, len(sorted_scores)+1) / len(sorted_scores)
    plt.plot(sorted_scores, y_vals, marker='o', linestyle='-', linewidth=2)
    plt.xlabel('情感得分')
    plt.ylabel('累积比例')
    plt.title('情感得分累积分布函数', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # 4. 文献类型得分对比（条形图+误差线）
    ax4 = plt.subplot(2, 2, 4)
    x_pos = range(len(type_stats))
    plt.bar(x_pos, type_stats['平均分'], 
            yerr=type_stats['标准差'],
            capsize=5,
            color=plt.cm.Set3(np.linspace(0, 1, len(type_stats))),
            edgecolor='black',
            linewidth=1)
    
    plt.xticks(x_pos, type_stats.index, rotation=45)
    plt.ylabel('平均情感得分')
    plt.title('各文献类型平均分±标准差', fontsize=14, fontweight='bold')
    plt.grid(True, axis='y', alpha=0.3)
    
    # 添加具体数值
    for i, (mean, std) in enumerate(zip(type_stats['平均分'], type_stats['标准差'])):
        plt.text(i, mean + 0.01, f'{mean:.3f}±{std:.3f}', 
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    
    # 保存图片
    stats_path = os.path.join(save_dir, 'detailed_statistics.png')
    plt.savefig(stats_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"详细统计图已保存到: {stats_path}")
    
    return heatmap_data

# 6. 生成统计摘要表格图片
def create_summary_table(df, type_stats, save_dir='output'):
    """生成统计摘要的表格图片"""
    
    # 创建摘要统计
    summary_data = {
        '指标': [
            '总文献数量',
            '平均情感得分',
            '情感得分标准差',
            '最高情感得分',
            '最低情感得分',
            '得分范围',
            '文献类型数量',
            '正向情感比例'
        ],
        '数值': [
            len(df),
            f"{df['情感得分'].mean():.3f}",
            f"{df['情感得分'].std():.3f}",
            f"{df['情感得分'].max():.3f}",
            f"{df['情感得分'].min():.3f}",
            f"{df['情感得分'].min():.3f}-{df['情感得分'].max():.3f}",
            len(type_stats),
            f"{(len(df)/len(df)*100):.1f}%"  # 所有都是正向，所以是100%
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    
    # 创建表格图
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    
    # 创建表格
    table = ax.table(cellText=summary_df.values,
                     colLabels=summary_df.columns,
                     cellLoc='center',
                     loc='center',
                     colColours=['#f2f2f2', '#f2f2f2'])
    
    # 调整表格样式
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)
    
    # 设置标题单元格样式
    for i in range(len(summary_df.columns)):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    # 交替行颜色
    for i in range(1, len(summary_df) + 1):
        if i % 2 == 0:
            for j in range(len(summary_df.columns)):
                table[(i, j)].set_facecolor('#f9f9f9')
    
    plt.title('文献情感分析统计摘要', fontsize=16, fontweight='bold', pad=20)
    
    # 保存表格图片
    table_path = os.path.join(save_dir, 'summary_table.png')
    plt.savefig(table_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"统计摘要表格已保存到: {table_path}")
    
    return summary_df

# 7. 主函数：运行所有分析
def main():
    """主函数：运行完整的分析流程"""
    
    print("=" * 60)
    print("文献情感差异分析工具")
    print("=" * 60)
    
    # 创建输出目录
    save_dir = 'sentiment_analysis_output'
    os.makedirs(save_dir, exist_ok=True)
    
    # 1. 创建并预处理数据
    print("\n1. 加载和预处理数据...")
    df = create_data()
    df = preprocess_data(df)
    
    print(f"数据加载完成，共 {len(df)} 篇文献")
    print(f"文献类型分布: {dict(df['文献类型'].value_counts())}")
    
    # 2. 生成关键词词云
    print("\n2. 生成关键词词云图...")
    keyword_freq = create_keyword_wordcloud(df, os.path.join(save_dir, 'keyword_wordcloud.png'))
    
    print(f"\n前10个高频关键词:")
    for word, count in keyword_freq.most_common(10):
        print(f"  {word}: {count}次")
    
    # 3. 生成文献类型情感对比
    print("\n3. 生成文献类型情感对比图...")
    type_stats = create_sentiment_comparison_charts(df, save_dir)
    
    # 4. 生成详细统计
    print("\n4. 生成详细统计分析图...")
    heatmap_data = create_detailed_statistics(df, type_stats, save_dir)
    
    # 5. 生成统计摘要
    print("\n5. 生成统计摘要表格...")
    summary_df = create_summary_table(df, type_stats, save_dir)
    
    # 6. 打印分析结论
    print("\n" + "=" * 60)
    print("分析结论摘要:")
    print("=" * 60)
    
    # 找出情感得分最高的文献类型
    highest_type = type_stats.loc[type_stats['平均分'].idxmax()]
    lowest_type = type_stats.loc[type_stats['平均分'].idxmin()]
    
    print(f"1. 整体分析: {len(df)}篇文献全部为正向情感，平均得分{df['情感得分'].mean():.3f}")
    print(f"2. 文献类型差异: 共识别出{len(type_stats)}种文献类型")
    print(f"3. 情感最强类型: {highest_type.name} (平均分: {highest_type['平均分']:.3f})")
    print(f"4. 情感最弱类型: {lowest_type.name} (平均分: {lowest_type['平均分']:.3f})")
    print(f"5. 稳定性最好: {type_stats.loc[type_stats['标准差'].idxmin()].name}")
    print(f"6. 最高分文献: {df.loc[df['情感得分'].idxmax(), '文件名']} ({df['情感得分'].max():.3f})")
    print(f"7. 最低分文献: {df.loc[df['情感得分'].idxmin(), '文件名']} ({df['情感得分'].min():.3f})")
    
    print(f"\n所有分析结果已保存到 '{save_dir}' 目录中!")
    print("=" * 60)

# 运行主函数
if __name__ == "__main__":
    main()