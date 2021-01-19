import pandas as pd
import feedparser
import re
import datetime as dti
#from datetime import datetime
from time import mktime

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.rstrip()
	
feed = feedparser.parse('https://www.jawapos.com/nasional/feed/')
df = pd.DataFrame({'title':[],'content':[],'summary':[],'link':[],'published':[]})

for i in feed.entries:
    conclean = i.content[0].value
    conclean = cleanhtml(conclean)
    conclean = conclean[13:]
    summa = cleanhtml(i.summary)
    stru = i.published_parsed
    dt = dti.datetime.fromtimestamp(mktime(stru))
    df = df.append({'title':i.title,'content':conclean,'summary':summa,'link':i.link,'published':dt}, ignore_index=True)
    

now = dti.datetime.now()
file = now.strftime("%d%m%Y")

name = "jp"+file+".csv"

df.to_csv(name)