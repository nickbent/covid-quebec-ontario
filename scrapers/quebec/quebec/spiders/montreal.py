import scrapy
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
from datetime import datetime as dt  


class TableSpider(scrapy.Spider):
    name = "table_montreal"
    start_urls = ['https://santemontreal.qc.ca/en/public/coronavirus-covid-19/']

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install()) 

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)

        self.driver.find_element_by_xpath('//*[@id="exampleHeadingDefault36390"]').click() 
        table = driver.find_element_by_xpath('//*[@id="c36390"]/table[3]/tbody')
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        region = {}
        for row in rows:
            elements = row.find_elements(By.TAG_NAME, "td")
            region[elements[0].text] = elements[1].text 

        date = dt.now().strftime('%Y-%m-%dT%H:%M:%S')
        path = '../../data/quebec/montreal' +date+ '.json'
        with open(path, 'w') as outfile:
            json.dump(region, outfile)
