import pandas as pd
import feedparser
import re
import datetime
from time import mktime
from tqdm import tqdm
#from newspaper import Article as art

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.rstrip()

urls = ["https://mediaindonesia.com/feed","https://www.jawapos.com/nasional/feed/","https://www.republika.co.id/rss","https://feed.liputan6.com/rss"]

	
feed=[]
for url in urls:
    feeds = feedparser.parse(url)
    feed.append(feeds)
	
df = pd.DataFrame({'title':[],'content':[],'summary':[],'link':[],'published':[],'source':[]})

for u in feed:
    source = u.feed.title
    for i in tqdm(u.entries):
        conclean = i.content[0].value
        conclean = cleanhtml(conclean)
        #conclean = conclean[13:]
        summa = cleanhtml(i.summary)
        stru = i.published_parsed
        dt = datetime.datetime.fromtimestamp(mktime(stru))
        df = df.append({'title':i.title,'content':conclean,'summary':summa,'link':i.link,'published':dt,'source':source}, ignore_index=True)
    

#import datetime
now = datetime.datetime.now()
file = now.strftime("%d%m%Y")

name = "arss"+file+".csv"

df.to_csv(name)
