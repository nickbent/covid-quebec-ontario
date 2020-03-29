#!/bin/sh

cd scrapers/ontario
scrapy crawl table_ontario
cd ../..
python scripts/merge_new_total.py
python scripts/merge_new_cases.py
mv data/ontario/total_* data/ontario/past
mv data/ontario/table_* data/ontario/past
jupyter nbconvert --to notebook --inplace --execute notebooks/Graphing\ Ontario.ipynb
git add plotly/*
git add data/ontario/all_updates.json
git add data/ontario/cases.jsonl
git commit -m "Updated Ontario"
git push origin master
