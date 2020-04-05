#!/bin/sh

cd scrapers/ontario
scrapy crawl table_ontario
cd ../..
python scripts/merge_new_total.py
mv data/ontario/total_* data/ontario/past
#jupyter nbconvert --to notebook --inplace --execute notebooks/Graphing\ Ontario.ipynb

