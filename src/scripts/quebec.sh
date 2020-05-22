#!/bin/sh

cd src/scrapers/quebec/
scrapy crawl table_quebec
cd ../../..
python src/scripts/merge_new_quebec.py 'May 21st'
python src/scripts/make_graphs_quebec.py
mv data/quebec/age_cases* data/quebec/past
mv data/quebec/age_deaths* data/quebec/past
mv data/quebec/cases* data/quebec/past
mv data/quebec/deaths* data/quebec/past


