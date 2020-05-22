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
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(executable_path='/Users/chocholatethunder/.wdm/drivers/chromedriver/mac64/chromedriver' )

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)

        cases = []
        text = self.driver.find_element_by_xpath('//*[@id="c50212"]/div/div').text
        # lines = text.find_elements(By.TAG_NAME, "li")
        # for li in lines:
        #     cases.append(lines.text)

        text += '\n'+self.driver.find_element_by_xpath('//*[@id="c50210"]/div/div').text 
        # lines = text.find_elements(By.TAG_NAME, "li")
        # for li in lines:
        #     cases.append(lines.text) 

        path = '../../../data/quebec/cases_total' +str(dt.now())+ '.txt'
        with open(path, 'w') as outfile:
            outfile.write(text)

        table = self.driver.find_element_by_xpath('//*[@id="c50214"]/div/div/div/table/tbody')
        rows = table.find_elements(By.TAG_NAME, "tr")
        age = {}
        for row in rows:
            elements = row.find_elements(By.TAG_NAME, "td")
            age[elements[0].text] = elements[1].text

        path = '../../../data/quebec/cases_region' +str(dt.now())+ '.json'
        with open(path, 'w') as outfile:
            json.dump(age, outfile)

        table = self.driver.find_element_by_xpath('//*[@id="c51880"]/div/div/div/table/tbody')
        rows = table.find_elements(By.TAG_NAME, "tr")
        age = {}
        for row in rows:
            elements = row.find_elements(By.TAG_NAME, "td")
            age[elements[0].text] = elements[1].text

        path = '../../../data/quebec/deaths_region' +str(dt.now())+ '.json'
        with open(path, 'w') as outfile:
            json.dump(age, outfile)

        table = self.driver.find_element_by_xpath('//*[@id="c50213"]/div/div/div/table/tbody')
        rows = table.find_elements(By.TAG_NAME, "tr")
        age = {}
        for row in rows:
            elements = row.find_elements(By.TAG_NAME, "td")
            age[elements[0].text] = elements[1].text

        path = '../../../data/quebec/age_cases' +str(dt.now())+ '.json'
        with open(path, 'w') as outfile:
            json.dump(age, outfile)


        table = self.driver.find_element_by_xpath('//*[@id="c51881"]/div/div/div/table/tbody')
        rows = table.find_elements(By.TAG_NAME, "tr")
        deaths = {}
        for row in rows:
            elements = row.find_elements(By.TAG_NAME, "td")
            deaths[elements[0].text] = elements[1].text

        path = '../../../data/quebec/age_death' +str(dt.now())+ '.json'
        with open(path, 'w') as outfile:
            json.dump(deaths, outfile)

        #self.driver.close()