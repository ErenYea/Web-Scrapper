from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os, sys
import time,requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from concurrent import futures

# driver = webdriver.Chrome(options=options)
# it is use to run webdriver without opening actual browser

with open("./jsonfiles/website.json", 'r') as js:
    data = json.load(js)

results = []


def mainscrapper(email):
    global data,results
    results =[]
    email = email
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    # print(key)

    # window_before = driver.window_handles[0]
    def scrapper(props):
        global results, data
        key,email = props
        driver = webdriver.Chrome(ChromeDriverManager().install())
        # window_after = driver.window_handles[0]
        driver.get(data[key]['url'])
        driver.implicitly_wait(30)
        myelement = driver.find_element_by_xpath(data[key]["inputpath"])
        myelement.send_keys(email)
        button = driver.find_element_by_xpath(data[key]["buttonpath"])
        button.click()
        try:
            t = driver.find_element_by_xpath(data[key]["errormessagepath"])
            if t.text == data[key]['successmessage']:
                result = "not registered"
            else:
                result = "registered"
        except Exception as e:
            print(e)
        driver.close()
        results.append([key, result])

    with futures.ThreadPoolExecutor() as executor:
        # store the url for each thread as a dict, so we can know which thread fails
        future_results = {key: executor.submit(scrapper, [key,email]) for key in data}
        # print(future_results)
        for key, future in future_results.items():
            try:
                # print(key,future)
                future.result()  # can use `timeout` to wait max seconds for each thread
            except Exception as exc:  # can give a exception in some thread
                print('url {:0} generated an exception: {:1}'.format(key, exc))
    return results