# Demmonitrix
A media monitoring research project. Topped with various automated text analysis pipelines, iced with beautiful dashboard. 

### Development Plan
- Scraper / News Aggregator to run daily on 8 or more Indonesian online news outlet
- Scraper / Listener for Indonesian Tweets with custom filter
- Model for Sentiment Analysis
- Model for Topic Classification
- NER to classify Academic Institution-related news
- Interactive Dashboard to Monitor custom keywords


## Usage Guide
[ScraperSQL.py](https://github.com/ruzcmc/medmon/blob/main/scraperSQL.py) is an rss feed scraper, I used [newspaper3k]() as the content scraper and combined it with pandas and sqlalchemy to save the data. Change the news source urls as you wish and modify the tables accordingly.
Before usage, you may want to 
```
pip install -r requirements.txt
```
first inside your desired environment. (note: if you use Linux, pywin might cause pip to stop, remove accordingly).
To run daily, insert it to your cron. Don't forget to change the permissions and create the db first.

## Disclaimer
This is a research project. You are free to use any of the code for non commercial purposes. Research articles concerning this project will be released accordingly, please cite if you decide to use this project.
