import scrapy
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
from datetime import datetime as dt  




class TableSpider(scrapy.Spider):
    name = "table_quebec"
    start_urls = ['https://www.quebec.ca/sante/problemes-de-sante/a-z/coronavirus-2019/situation-coronavirus-quebec/']

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install()) 

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)

        table = self.driver.find_element_by_xpath('//*[@id="c47903"]/div/div/div/table/tbody')
        rows = table.find_elements(By.TAG_NAME, "tr")
        region = {}
        for row in rows:
            elements = row.find_elements(By.TAG_NAME, "td")
            region[elements[0].text] = elements[1].text

        path = '../../data/quebec/region_quebec_' +str(dt.now())+ '.json'
        with open(path, 'w') as outfile:
            json.dump(region, outfile)

        #self.driver.close()