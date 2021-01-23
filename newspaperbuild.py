import newspaper
import pandas as pd
from tqdm.auto import tqdm
from datetime import datetime
from time import mktime
import re
from newspaper import news_pool, Config

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.rstrip()
	
	
#BUILD SOURCES 
config = Config()
config.memoize_articles = False


antara = newspaper.build("https://www.antaranews.com/")
jawapos = newspaper.build("https://www.jawapos.com/")
mediaindo = newspaper.build("https://www.mediaindonesia.com/")
suara = newspaper.build("https://www.suara.com/")
liputan = newspaper.build("https://www.liputan6.com/")
republika = newspaper.build("https://www.republika.co.id/")
cnnindo = newspaper.build("https://www.cnnindonesia.com/")
cnbcindo = newspaper.build("https://www.cnbcindonesia.com/")
#kumparan = newspaper.build("https://www.kumparan.com/")
#ngopibareng = newspaper.build("https://www.ngopibareng.id/")
#detik = newspaper.build("https://www.detik.com/")
kompas = newspaper.build("https://www.kompas.com/") 
#tirto = newspaper.build("https://www.tirto.id/")

df = pd.DataFrame({'title':[],'content':[],'summary':[],'link':[],'published':[],'source':[]})

#POOLING

kolamikan = [antara,jawapos,mediaindo,suara,liputan,republika,cnnindo,cnbcindo,kumparan,ngopibareng,detik,kompas,tirto]
news_pool.set(kolamikan, threads_per_source=3)
news_pool.join()


#INSERTING TO HOUSES

for u in tqdm(kolamikan):
    for a in u.articles:
        df = df.append({'title':a.title,'content':cleanhtml(a.text),'summary':a.summary,'link':a.url,'published':a.publish_date,'source':u.brand}, ignore_index=True)
    
    
#SAVE TO CSV

import datetime
now = datetime.datetime.now()
file = now.strftime("%d%m%Y")

name = "newspaper"+file+".csv"

df.to_csv(name)
