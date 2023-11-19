import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud


def draw_chart(title, xlabel, ylabel, chart_name):
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("image/" + chart_name)
    plt.show()


def other_df(df1):
    df1.reset_index(drop=False)
    tep_df1 = df1.groupby('category')['word_count'].sum().reset_index().sort_values('category')
    tep_df2 = df1['category'].value_counts().reset_index().sort_values('category')
    df2 = tep_df1.merge(tep_df2, how='inner').reset_index(drop=True)
    df2['average'] = round(df2['word_count'] / df2['count'])
    return df2


def word_cloud(image_name, text, title):
    wordcloud = WordCloud(width=800, height=400, background_color='white',
                          font_path='/System/Library/Fonts/STHeiti Light.ttc').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show()
    wordcloud.to_file("image/" + image_name)


# data_collect()

df1 = pd.read_csv('novel.csv')
df2 = other_df(df1)
df2 = df2.sort_values(by='average').reset_index(drop=True)
sns.set(style="darkgrid")

# 1. 绘制柱状图，展示各类小说总字数
# 将Series转换为DataFrame
plt.figure(figsize=(8, 4))  # 设置图形大小
sns.barplot(x='category', y='word_count', data=df2, hue='category', palette='hls')
draw_chart('各类小说总字数', 'category', 'word_count(单位：万字)', 'total_number.png')

plt.figure(figsize=(8, 4))  # 设置图形大小
sns.barplot(x='category', y='count', data=df2, hue='category', palette='hls')
draw_chart('各类小说总字数', 'category', 'count(单位：本)', 'total_count.png')

# 2. 绘制直方图，展示小说字数分布
plt.figure(figsize=(8, 4))  # 设置图形大小
sns.histplot(df1['word_count'], bins=100, kde=True, color='blue', edgecolor='black')
draw_chart('小说字数分布', 'word_count(单位：万字)', 'novel_count(单位：本)', 'word_distribution.png')

# 3. 绘制饼状图，分别展示男女受众各个类别书籍所占比例
df_man = df2[df2['category'].str.len() == 2].reset_index(drop=True).sort_values(by='average', ascending=False)
df_woman = df2[df2['category'].str.len() != 2].reset_index(drop=True).sort_values(by='average', ascending=False)

plt.figure(figsize=(8, 8))  # 设置图形大小
colors = cm.rainbow(
    np.arange(len(df_man['category'].value_counts().tolist())) / len(df_man['category'].value_counts().tolist()))
exp = [0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
plt.pie(df_man['average'], labels=df_man['category'], pctdistance=0.9, explode=exp, startangle=90, autopct='%2.1f%%',
        shadow=True, labeldistance=1.1, colors=colors)
plt.legend(bbox_to_anchor=(1.3, 0.5), loc="center right")
draw_chart('男性受众群体的各类小说平均字数占比', '图一', '', 'novels_distribution_man')

plt.figure(figsize=(8, 8))
colors = cm.rainbow(
    np.arange(len(df_man['category'].value_counts().tolist())) / len(df_man['category'].value_counts().tolist()))
exp = [0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
plt.pie(df_woman['average'], labels=df_woman['category'], pctdistance=0.9, explode=exp, startangle=90,
        autopct='%2.1f%%', shadow=True, labeldistance=1.1, colors=colors)
plt.legend(bbox_to_anchor=(1.3, 0.5), loc="center right")
draw_chart('女性受众群体的各类小说平均字数占比', '图二', '', 'novels_distribution_woman')

# 4. 绘制折线图，对比连载与完结作品的字数
df_serialization = other_df(df1[df1['status'] == '连载中']).sort_values(by='average').reset_index(drop=True)
df_end = other_df(df1[df1['status'] == '已完结']).sort_values(by='average').reset_index(drop=True)
plt.figure(figsize=(8, 4))  # 设置图形大小
sns.lineplot(x='category', y='average', data=df_serialization, label='连载中', marker='o')  # 绘制第一个连载中的折线
sns.lineplot(x='category', y='average', data=df_end, label='已完结', marker='o')  # 绘制第二个已完结的折线
sns.lineplot(x='category', y='average', data=df2, label='不分类', marker='o')  # 绘制第三个DataFrame的折线
draw_chart('完结与连载书籍与未分类下每个分类的平均字数', 'category', 'word_count(单位：万字)', 'average_comparison.png')

# 5. 绘制散点图，展示各类小说平均字数
# 因为原先数据太多了，就挑了男女性别中单个种类中小说本数最多的进行分析，分别是玄幻和二次元
df3 = df1[df1['category'] == '玄幻'].reset_index(drop=True)
plt.figure(figsize=(8, 4))  # 设置图形大小
colors = np.arange(50)  # 用于表示渐变颜色的
scatter = sns.scatterplot(x='name_length', y='word_count', data=df3, c=np.arange(len(df3)), cmap='viridis')
colorbar = plt.colorbar(scatter.get_children()[0])
colorbar.set_label('Index')
draw_chart('玄幻小说字数与小说名长度关系', 'name_length', 'word_count(单位：万字)', 'word_name_man.png')

df4 = df1[df1['category'] == '二次元'].reset_index(drop=True)
plt.figure(figsize=(8, 4))  # 设置图形大小
scatter = sns.scatterplot(x='name_length', y='word_count', data=df4, c=np.arange(len(df4)), cmap='viridis')
colorbar = plt.colorbar(scatter.get_children()[0])
colorbar.set_label('Index')
draw_chart('二次元类小说字数与小说名长度关系', 'name_length', 'word_count(单位：万字)', 'word_name_woman.png')

# 6. 绘制小提琴图展示不同性别受众群体的各类小说字数分布
df_man = df1[df1['gender'] == 'man'].reset_index(drop=True)
plt.figure(figsize=(8, 4))  # 设置图形大小
sns.violinplot(x='category', y='word_count', data=df_man)
draw_chart('男性受众群体所看各类小说的字数分布', 'category', 'word_count(单位：万字)', 'violin_man.png')

df_woman = df1[df1['gender'] == 'woman'].reset_index(drop=True)
plt.figure(figsize=(8, 4))  # 设置图形大小
sns.violinplot(x='category', y='word_count', data=df_woman)
draw_chart('女性受众群体所看各类小说的字数分布', 'category', 'word_count(单位：万字)', 'violin_woman.png')

# 7. 绘制回归曲线
df3 = df1['name_length'].value_counts().reset_index(drop=False).sort_values('name_length').reset_index(drop=True)
df3 = df3[df3['count'] > 10]
plt.figure(figsize=(8, 4))  # 设置图形大小
sns.regplot(x='name_length', y='count', data=df3, order=1)
draw_chart('书本数与书名长度关系', 'name_length', 'count', 'relation1.png')
plt.figure(figsize=(8, 4))  # 设置图形大小
sns.regplot(x='name_length', y='count', data=df3, order=2)
draw_chart('书本数与书名长度关系', 'name_length', 'count', 'relation2.png')

# 8. 不同性别受众书名词云
df_cloud1 = df1[df1['gender'] == 'man']
text1 = ' '.join(df_cloud1['name'])
word_cloud("book_name_man.png", text1, '男生群体书名词云')
df_cloud2 = df1[df1['gender'] == 'woman']
text2 = ' '.join(df_cloud2['name'])
word_cloud("book_name_woman.png", text2, '女生群体书名词云')