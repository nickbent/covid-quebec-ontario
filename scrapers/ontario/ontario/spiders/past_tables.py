import scrapy
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json  
from datetime import datetime as dt  




class TableSpider(scrapy.Spider):
    name = "past_ontario"
    #allowed_domains = ['ontario.ca']
    #start_urls = ['https://www.ontario.ca/page/2019-novel-coronavirus']

    # def __init__(self):
    #      self.driver = webdriver.Chrome(ChromeDriverManager().install()) 

    def start_requests(self):
        yield scrapy.Request('https://www.ontario.ca/page/2019-novel-coronavirus')

    def parse(self, response):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(response.url)
        time.sleep(5)

        data = []
        headers = ["case number", "patient", "public health unit", "transmission", "status"] 

        page = self.driver.find_element_by_xpath('//*[@id="pagebody"]') 
        divisions = page.find_elements(By.TAG_NAME, "div")
        for div in divisions : 
            table = div.find_elements(By.TAG_NAME, "tbody")
            if len(table) == 0 : 
                continue

            rows = table[0].find_elements(By.TAG_NAME, "tr")
            for row in rows:
                row_dict = {}
                for ix, element in enumerate(row.find_elements(By.TAG_NAME, "td")):
                    row_dict[headers[ix]] = element.text
                data.append(row_dict)


            

        total_table = self.driver.find_element_by_xpath('//*[@id="pagebody"]/table/tbody')
        rows = total_table.find_elements(By.TAG_NAME, "tr")
        total = {}
        for row in rows:
            elements = row.find_elements(By.TAG_NAME, "td")
            total[elements[0].text] = elements[1].text



        timestamp = response.meta['wayback_machine_time'].timestamp()
        path = '../../data/ontario/table_person_ontario_' +timestamp+'.jsonl'
        with open(path, 'w') as outfile:
            for entry in data:
                json.dump(entry, outfile)
                outfile.write('\n')

        path = '../../data/ontario/total_ontario_' +timestamp+'.json'
        with open(path, 'w') as outfile:
            json.dump(total, outfile)

        #self.driver.close()