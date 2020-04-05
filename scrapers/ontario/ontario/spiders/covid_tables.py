import scrapy
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json  
from datetime import datetime as dt  




class TableSpider(scrapy.Spider):
    name = "table_ontario"
    #allowed_domains = ['ontario.ca']
    start_urls = ['https://www.ontario.ca/page/2019-novel-coronavirus']

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install()) 

    def parse_table(self, table):
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            row_dict = {}
            for ix, element in enumerate(row.find_elements(By.TAG_NAME, "td")):
                row_dict[self.headers[ix]] = element.text
            self.data.append(row_dict)


    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)

        self.data = []
        #self.headers = ["case number", "patient", "public health unit", "transmission", "status"] 

        #Might need these css locators for tables in past
        #//*[@id="pagebody"]/table[2]/tbody
        #//*[@id="pagebody"]/table[3]/tbody
        table = driver.find_element_by_xpath('//*[@id="pagebody"]/table/tbody')
        rows = table.find_elements(By.TAG_NAME, "tr")

        total = {}
        for row in rows:
            elements = row.find_elements(By.TAG_NAME, "td")
            total[elements[0].text] = elements[1].text


        date = dt.now().strftime('%Y-%m-%dT%H:%M:%S')

        path = '../../data/ontario/total_ontario_' +date+'.json'
        with open(path, 'w') as outfile:
            json.dump(total, outfile)

        #self.driver.close()