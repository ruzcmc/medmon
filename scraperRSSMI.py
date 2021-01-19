import pandas as pd
import feedparser
import re
import datetime

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.rstrip()
	
feed = feedparser.parse('https://mediaindonesia.com/feed')
df = pd.DataFrame({'title':[],'content':[],'summary':[],'link':[],'published':[]})

for i in feed.entries:
    conclean = i.content[0].value
    conclean = cleanhtml(conclean)
    summa = cleanhtml(i.summary)
    df = df.append({'title':i.title,'content':conclean,'summary':summa,'link':i.link,'published':i.published}, ignore_index=True)
    

now = datetime.datetime.now()
file = now.strftime("%d%m%Y")

name = "mediaindo"+file+".csv"

df.to_csv(name)