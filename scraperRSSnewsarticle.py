import pandas as pd
import feedparser
from datetime import datetime
from time import mktime
from newspaper import Article as art
from tqdm import tqdm

import re

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.rstrip()
	
	
urlnocont = ["https://www.antaranews.com/rss/terkini.xml","https://www.antaranews.com/rss/top-news.xml","https://www.suara.com/rss/news","https://www.cnnindonesia.com/nasional/rss","https://www.cnbcindonesia.com/news/rss",]

feed=[]
for url in urlnocont:
    feeds = feedparser.parse(url)
    feed.append(feeds)
	
df = pd.DataFrame({'title':[],'content':[],'summary':[],'link':[],'published':[],'source':[]})

def extractcontent(link):
    page = art(link)
    page.download()
    page.parse()
    content = cleanhtml(page.text)
    content = content.rstrip()
    
    
    return content

for u in feed:
    source = u.feed.title
    for i in tqdm(u.entries):
        conclean = extractcontent(i.link)
        summa = cleanhtml(i.summary)
        stru = i.published_parsed
        dt = datetime.fromtimestamp(mktime(stru))
        df = df.append({'title':i.title,'content':conclean,'summary':summa,'link':i.link,'published':dt,'source':source}, ignore_index=True)
    


now = datetime.now()
file = now.strftime("%d%m%Y")

name = "brss"+file+".csv"

df.to_csv(name)