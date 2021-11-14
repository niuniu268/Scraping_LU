import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

df = pd.DataFrame()


def get_html(url):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebLit/537.36 (KHTML, like Gecko)'}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        resp.encoding = 'utf-8'
        return resp.text
    except resp.exceptions.RequestException:
        return ''


def get_nodes(html):
    '''# apply the module, which is named as BeautifulSoup, 
    # to analyze and extract main information from the website, "lunduniversity.se"'''
    soup = BeautifulSoup(html, 'html.parser')
    nodes = soup.find_all('li', class_='views-row')
    return nodes


def get_each_node_data(df, nodes):
    '''# extracting the information and writing into the database, df
    database, df, consists of 5 columns: articles' title, the url of articles, 
    the summary of articles, the time to start scraping, and the time to end up'''

    now = int(time.time())
    for node in nodes:
        title = node.find('h2').text.strip()
        url = node.find('a')['href']
        publish = node.find('span').text.strip
        data = {
            'title': [title],
            'url': [url],
            'publish': [publish], 
            'start_time': [now], 
            'end_time': [now]
        }
        item = pd.DataFrame(data)
        df = pd.concat([df, item], ignore_index=True)
    return df


for i in range(2):
    url = 'https://lunduniversity.lu.se/news/archive?start={}'.format(i+1)
    html = get_html(url)
    nodes = get_nodes(html)
    df = get_each_node_data(df, nodes)

df.shape

# convert the format of data_time
df['start_time'] = pd.to_datetime(df['start_time'], unit='s')
df['end_time'] = pd.to_datetime(df['end_time'], unit='s')

# preparying for the wordcloud
text = ' '.join(name for name in df.title)

# remove redundent words from wordcloud
stopwords = set(STOPWORDS)
stopwords.update(['picture', 'can', 'is', 'in', 'the', 'an', 
                  'a', 'of', 'from', 'are', 'has', 'have', 'pictures', 'sweden', 'swedish', 'need', 'will'])

# establishing the wordcloud
wordcloud = WordCloud(stopwords=stopwords, background_color='white').generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('local.jpg', format='jpg')
plt.show()

# Output the database as a CSV file

df.to_csv('lu_article.csv', index=False, sep=',', encoding='utf-8')

df = pd.read_csv('lu_article.csv', sep=',')
