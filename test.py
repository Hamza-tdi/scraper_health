import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import  ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import os


# VARIABLES
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# driver.get('https://turquoise.health/providers/providence-hospital-4/services/providence-35621273-cardiac-arrhythmia-i/')

# elm = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//label[@class="payment-select-button"]')))[-1]
# elm.click()
# time.sleep(1)
# inssurance_plans = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//select[@id="insurance-plan-selection"]/option')))
# print(len(inssurance_plans))
# for ins in range(1, len(inssurance_plans)):
#     print(ins)
#     # driver.find_elements_by_xpath(f'//select[@id="insurance-plan-selection"]/option[text()="{inssurance_plans[ins].text}"]')[ins].click()
#     inssurance_plans[ins].click()
#     time.sleep(2)
#     ins_cash = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div/ul/li/span[@class="estimate-amount"]')))[-2].text
#     print(ins_cash)
# data = []
# list_insurances = []
# provider_name = ''
# service_name = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//div[@class="cost-estimate-info"]/h1'))).text
# try:
#     cash_price = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'cashPriceAmount'))).text
# except TimeoutException as e:
#     cash_price = 'N/A'
# provider_address = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
#     (By.XPATH, '//div[@class="hospital-all-detail"]/ul/li/span'))).text
# # provider_address = "Address"
# try:
#     list_insurances = []
#     elm = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, '//label[@class="payment-select-button"]')))[-1]
#     elm.click()
#     inssurance_plans = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, '//select[@id="insurance-plan-selection"]/option')))
#     for ins in range(1, len(inssurance_plans)-1):
#         inssurance_plans[ins].click()
#         ins_name = inssurance_plans[ins].text
#         ins_cash = WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.XPATH, '//div/ul/li/span[@class="estimate-amount"]')))[-2].text
#         _dict_ins = {'ins_name': ins_name, 'ins_cash': ins_cash}
#         list_insurances.append(_dict_ins)
#     _dict = {'provider_name': provider_name, 'provider_address': provider_address, 'service_name': service_name, 'cash_price': cash_price, 'insurrance_plans': list_insurances}
#     data.append(_dict)
# except TimeoutException as e:
#     _dict = {'provider_name': provider_name, 'provider_address': provider_address, 'service_name': service_name, 'cash_price': cash_price, 'insurrance_plans': []}
#     data.append(_dict)
# print(_dict)
print("a".upper())