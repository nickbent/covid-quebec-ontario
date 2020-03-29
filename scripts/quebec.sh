#!/bin/sh

jupyter nbconvert --to notebook --inplace --execute notebooks/Graphing\ Quebec.ipynb
git add plotly/*
git commit -m "Updated Quebec"
git push origin master
