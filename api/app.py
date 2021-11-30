from flask import Flask
from flask_restful import Resource, Api, reqparse


import time
import math
import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pandas.core.common import flatten
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, StaleElementReferenceException

options = Options()
options.page_load_strategy = 'eager'
options.headless = True
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort

app = Flask(__name__)
api = Api(app)

class IEEE(Resource):

    #hello_args = {"search_word": fields.Str(required=True)}

    #@use_args(hello_args)

    def get(self):

        
        browser = Firefox(options = options)

        URL = "https://www.ieee.org/searchresults/index.html?q={}".format("biology")

        browser.get(URL)
        browser.implicitly_wait(5)

        path = "//div[@id='___gcse_0']/.//div[@class='gsc-resultsbox-visible']/div[1]/div/.//div[contains(@class, 'gsc-webResult gsc-result')]"

        elems = browser.find_elements_by_xpath(path)

        title = []
        link = []

        flist = []
        for i in elems:
                
            try: 
                link_tx = i.find_element_by_xpath(".//a[@class='gs-title']").get_attribute("href")
                link.append(link_tx)
            except:
                link_tx = ""
                link.append(link_tx)

            try: 
                title_tx = i.find_element_by_xpath(".//a[@class='gs-title']").text
                title.append(title_tx)
            except:
                title_tx = ""
                title.append(title_tx)

            pdict = {
                "title": title_tx,
                "link": link_tx
            }
            flist.append(pdict)
        browser.close()
        browser.quit()
        

        return(flist)

@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    abort(error_status_code, errors=err.messages)

api.add_resource(IEEE, '/', '/ieee')

if __name__ == '__main__':
    app.run(debug=True)