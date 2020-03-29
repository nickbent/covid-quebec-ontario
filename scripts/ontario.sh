cd scrapers/ontario
scrapy crawl table_ontario
cd ../..
python scripts/merge_new_total.py
python scripts/merge_new_cases.py
jupyter nbconvert --to notebook --inplace --execute notebookts/Graphing\ Ontario.ipynb
git add plotly/*
git commit -m "Updated Ontario"
git push origin master
