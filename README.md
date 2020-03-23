# CORONA VIRUS SCRAPER AND VISUALIZER FOR QUEBEC AND ONTARIO

I was super impressed by 'https://covid19stats.alberta.ca/' so I decided to create something similar for the provinces of Ontario and Quebec. I have scraped data and made visualizations and put them in :  
https://canadian-covid-visualizations.netlify.com/?fbclid=IwAR17oeIrlenhQTyC0mRvsivrLVDHaw27O2UGbCbXMjHsG_72w85EQr1Ou-w

## Getting Started 

To Scrape the latest Quebec information from 'https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/'

`cd scrapers/quebec`
`scrapy crawl table_quebec`

For the latest data from 'https://www.ontario.ca/page/2019-novel-coronavirus'

`cd scrapers/ontario`
`scrapy crawl table_ontario`

The scraped data will go into `data/PROVINCE` with a timestamped file

`data/Quebec/quebec.csv` contains all information from previous days which I got manually from the Way Back Machine.


The visualizations are made in `notebooks/Graphing Ontario` and `notebooks/Graphing Quebec`

#TODO

Change the visualizations from notebooks to scripts

Have not figured out how to scrape the way back machine yet. Currently using https://github.com/sangaline/scrapy-wayback-machine but have not got it to work. The spider is currently in `scrapers/ontario/ontario/spiders/past_tables.py`. I have added the required changes to `scrapers/ontario/ontario/settings.py` but still not working. 


