import pandas as pd
import feedparser
from datetime import datetime
from time import mktime
from newspaper import Article as art
from tqdm import tqdm
import re
import mysql.connector
from sqlalchemy import create_engine
import pymysql

def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
	cleantext = re.sub(cleanr, '', raw_html)
	cleantext = cleantext.rstrip("\n")
	return cleantext

urls = ["https://mediaindonesia.com/feed","https://www.jawapos.com/nasional/feed/","https://www.republika.co.id/rss","https://feed.liputan6.com/rss"]
urlnocont = ["https://www.antaranews.com/rss/terkini.xml","https://www.antaranews.com/rss/top-news.xml","https://www.suara.com/rss/news","https://www.cnnindonesia.com/nasional/rss","https://www.cnbcindonesia.com/news/rss",]

	
feed=[]
for url in urls:
    feeds = feedparser.parse(url)
    feed.append(feeds)
	
feedi = []	
for url in urlnocont:
    feeds = feedparser.parse(url)
    feedi.append(feeds)	

df = pd.DataFrame({'title':[],'content':[],'summary':[],'link':[],'published':[],'source':[]})

def extractcontent(link):
    page = art(link)
    page.download()
    page.parse()
    content = cleanhtml(page.text)
    content = content.rstrip("\n")
    
    
    return content

for u in feed:
    source = u.feed.title
    for i in tqdm(u.entries):
        conclean = i.content[0].value
        conclean = cleanhtml(conclean)
        #conclean = conclean[13:]
        summa = cleanhtml(i.summary)
        stru = i.published_parsed
        dt = datetime.fromtimestamp(mktime(stru))
        df = df.append({'title':i.title,'content':conclean,'summary':summa,'link':i.link,'published':dt,'source':source}, ignore_index=True)
 
for u in feedi:
    source = u.feed.title
    for i in tqdm(u.entries):
        conclean = extractcontent(i.link)
        summa = cleanhtml(i.summary)
        stru = i.published_parsed
        dt = datetime.fromtimestamp(mktime(stru))
        df = df.append({'title':i.title,'content':conclean,'summary':summa,'link':i.link,'published':dt,'source':source}, ignore_index=True)
     

#import datetime save file
#now = datetime.datetime.now()
#file = now.strftime("%d%m%Y")

#name = "allrss"+file+".csv"

#df.to_csv(name)

#sql connector
tableName = "beritaonline"
sqlEngine = create_engine('mysql+pymysql://user:pass@127.0.0.1/medmon', pool_recycle=3600)
dbConnection = sqlEngine.connect()
try:
	df.reset_index(drop=True, inplace=True)
	frame = df.to_sql(tableName, con=dbConnection, if_exists='append', index=False)

except ValueError as vx:

    print(vx)

except Exception as ex:   

    print(ex)

else:

    print("Table %s inserted successfully."%tableName);   

finally:

    dbConnection.close()
