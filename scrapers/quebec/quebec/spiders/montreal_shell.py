import argparse
import scrapy
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
from datetime import datetime as dt 


def main(response):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(response.url)

    driver.find_element_by_xpath('//*[@id="exampleAccordionDefault"]').click() 
    table = driver.find_element_by_xpath('//*[@id="c36505"]/div/table[1]/tbody')
    rows = table.find_elements(By.TAG_NAME, "tr")
    
    region = {}
    for row in rows:
        elements = row.find_elements(By.TAG_NAME, "td")
        region[elements[0].text] = (elements[1].text, elements[3].text)

    date = dt.now().strftime('%Y-%m-%dT%H:%M:%S')
    path = 'data/quebec/montreal_ciuss' +date+ '.json'
    with open(path, 'w') as outfile:
        json.dump(region, outfile)

    table = driver.find_element_by_xpath('//*[@id="c36505"]/div/table[2]/tbody')
    rows = table.find_elements(By.TAG_NAME, "tr")
    
    region = {}
    for row in rows:
        elements = row.find_elements(By.TAG_NAME, "td")
        region[elements[0].text] = (elements[1].text, elements[3].text)

    date = dt.now().strftime('%Y-%m-%dT%H:%M:%S')
    path = 'data/quebec/montreal_nhood' +date+ '.json'
    with open(path, 'w') as outfile:
        json.dump(region, outfile)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "response", help="response object from scrapy shell"
    )
    args = parser.parse_args()
    main(**vars(args))