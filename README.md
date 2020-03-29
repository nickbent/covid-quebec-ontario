# CORONA VIRUS SCRAPER AND VISUALIZER FOR QUEBEC AND ONTARIO

I was super impressed by https://covid19stats.alberta.ca/ so I decided to create something similar for the provinces of Ontario and Quebec. I have scraped data and made visualizations and put them in :  
https://canadian-covid-visualizations.netlify.com/?fbclid=IwAR17oeIrlenhQTyC0mRvsivrLVDHaw27O2UGbCbXMjHsG_72w85EQr1Ou-w

## Getting Started 

`bash scripts/quebec.sh`

Updates the latest from https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/

 and updates the plotly graphs in plotly/

`bash scripts/ontario.sh`

does the same thing for Ontario 'https://www.ontario.ca/page/2019-novel-coronavirus'


The visualizations are made in `notebooks/Graphing Ontario` and `notebooks/Graphing Quebec`

#TODO

Scrape sante quebec twitter to get updates 


