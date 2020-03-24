# CORONA VIRUS SCRAPER AND VISUALIZER FOR QUEBEC AND ONTARIO

I was super impressed by https://covid19stats.alberta.ca/ so I decided to create something similar for the provinces of Ontario and Quebec. I have scraped data and made visualizations and put them in :  
https://canadian-covid-visualizations.netlify.com/?fbclid=IwAR17oeIrlenhQTyC0mRvsivrLVDHaw27O2UGbCbXMjHsG_72w85EQr1Ou-w

## Getting Started 

To Scrape the latest Quebec information from https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/

`cd scrapers/quebec`

`scrapy crawl table_quebec`

`data/quebec/Quebec.csv` contains all information from previous days which I got manually from the Way Back Machine. I will be updating this manually since I am getting data from the above link and Sante quebec twitter daily. 


For the latest data from 'https://www.ontario.ca/page/2019-novel-coronavirus'

`cd scrapers/ontario`

`scrapy crawl table_ontario`


Past data was taken from
https://github.com/Russell-Pollari/ontario-covid19/blob/master/data/processed/all_cases.json

The scraped data will go into `data/PROVINCE` with a timestamped file

To update the ontario data files

`python scripts/merge_new_cases.py`
`python scripts/merge_new_total.py`

and then move the files that were just scraped in to `data/PROVINCE/past/`


The visualizations are made in `notebooks/Graphing Ontario` and `notebooks/Graphing Quebec`

#TODO

Change the visualizations from notebooks to scripts

Scrape sante quebec twitter to get updates 


