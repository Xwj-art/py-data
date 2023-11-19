import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/116.0.0.0 Safari/537.36 '
}

data = []


# 拿到数据
def crawler(url):
    # 判定本类小说受众群体性别
    gender = "man"
    page = requests.get(url, headers).text
    tree = etree.HTML(page)
    num = len(tree.xpath('/html/body/div[1]/div[2]/div[3]/div[2]/div[1]/ul')[0]) + 1
    string = '/html/body/div[1]/div[2]/div[3]/div[2]/div[1]/ul/li['

    # 拿到小说数据，制成二维数组
    for i in range(1, num):
        name = tree.xpath(string + str(i) + ']/div[2]/h3/a')[0].text
        category = tree.xpath(string + str(i) + ']/div[2]/p[1]/span[1]')[0].text
        status = tree.xpath(string + str(i) + ']/div[2]/p[1]/span[2]')[0].text
        tep = tree.xpath(string + str(i) + ']/div[2]/p[1]/span[3]')[0].text
        if len(category) != 2:
            gender = 'woman'
        if tep[-1] == '万':
            tep = tep[:-1]
            word_count = float(tep)
            word_count = round(word_count)
            data.append(list((name, category, status, int(word_count), gender, len(name))))
            continue
        word_count = float(tep)
        word_count /= 10000
        data.append(list((name, category, status, word_count, gender, len(name))))


# 获取url数组
def get_urls():
    url_list = []
    page1 = requests.get('https://www.readnovel.com/category/f1_f1_f1_f1_f1_f1_0_1', headers).text
    tree1 = etree.HTML(page1)
    ids1 = tree1.xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/ul/li/@data-id')[1:]
    ids2 = tree1.xpath('/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[3]/ul/li/@data-id')[1:]
    # 拿到所有分类的id
    ids = ids2 + ids1

    for j in range(len(ids)):
        tep = 'https://www.readnovel.com/category/' + str(ids[j]) + '_f1_f1_f1_f1_f1_0_'
        page = requests.get(tep + '1', headers).text
        tree = etree.HTML(page)
        # 某分类下从1-n拿到每一页的url
        n = int(tree.xpath('/html/body/div[1]/div[2]/div[3]/div[2]/div[2]/div/div/ul/li[10]/a')[0].text)
        for i in range(1, n + 1):
            url = tep + str(i)
            url_list.append(url)
    return url_list


def data_collect():
    with ThreadPoolExecutor(max_workers=15) as executor:
        executor.map(crawler, get_urls())

    df = pd.DataFrame(data, columns=['name', 'category', 'status', 'word_count', 'gender', 'name_length'])
    df = df.drop_duplicates()
    df = df.dropna()
    df = df[df['word_count'] != 0]
    df = df[df['word_count'] < 1000]
    df = df[df['category'] != '短篇']
    df = df.reset_index(drop=True)
    # 获取数据放入novel.csv，避免每次重新爬，直接从csv拿到数据
    df.to_csv('novel.csv', index=False)