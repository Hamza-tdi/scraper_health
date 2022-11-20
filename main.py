from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import json
import argparse


# VARIABLES
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
parser = argparse.ArgumentParser(description='Scrap Data from Site')
parser.add_argument('type', type=str, help='Type of  scraping method')
parser.add_argument('input', type=str, help='Value of Input, State Name if you want to scrap a site data, provider url if you want to scrap one provider')
args = parser.parse_args()
state_path = "https://turquoise.health/providers?state={ST}&page=1&letter="


def retract_providers():
    _list = []
    while True:
        try:
            elements = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, '//ul[@class="three-columns"]/li/a')))
            for elm in elements:
                href = elm.get_attribute('href')
                _list.insert(len(_list), href)
        except TimeoutException as e:
            print(e)
        try:
            current_page = int(WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//div[@class="alphabet-pagination"]/ul/li/a[@class="current-pagination"]'))).text)
            next_page = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, f'//div[@class="alphabet-pagination"]/ul/li/a[contains(text(), "{current_page + 1}")]')))
            driver.get(next_page.get_attribute('href'))
        except TimeoutException as e:
            break
    return _list


def retract_all_services():
    services_list = []
    try:
        services_elm = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="browse-services"]/ul/li/a')))
        services = []
        for item in services_elm:
            services.insert(len(services), item.get_attribute('href'))
        for elm in services:
            print(elm)
            driver.get(elm)
            services_list.extend(retract_all_services())
    except TimeoutException as e:
        for item in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@class="rate-button"]'))):
            services_list.insert(len(services_list), item.get_attribute('href'))
    return services_list


def state_extractor():
    global provider_address
    providers = retract_providers()
    data = []
    for provider in providers:
        driver.get(provider)
        provider_name = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//div[@class="page-title"]/h1'))).text
        elm_eddress = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="sidebar-location"]/p')))
        provider_address = ''
        for i in elm_eddress:
            provider_address += i.text
        services = retract_all_services()
        print(f'Total Services : {len(services)}')
        data_service = []
        for i in services:
            driver.get(i)
            service_name = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
                (By.XPATH, '//div[@class="cost-estimate-info"]/h1'))).text
            try:
                cash_price = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.ID, 'cashPriceAmount'))).text
            except TimeoutException as e:
                cash_price = 'N/A'
            try:
                list_insurances = []
                elm = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located(
                    (By.XPATH, '//label[@class="payment-select-button"]')))[-1]
                elm.click()
                inssurance_plans = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located(
                    (By.XPATH, '//select[@id="insurance-plan-selection"]/option')))
                for ins in range(1, len(inssurance_plans)-1):
                    inssurance_plans[ins].click()
                    ins_name = inssurance_plans[ins].text
                    ins_cash = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, '//div/ul/li/span[@class="estimate-amount"]')))[-2].text
                    _dict_ins = {'ins_name': ins_name, 'ins_cash': ins_cash}
                    list_insurances.append(_dict_ins)
                _dict = {'service_name': service_name, 'cash_price': cash_price, 'insurrance_plans': list_insurances}
                data_service.append(_dict)
            except TimeoutException as e:
                _dict = {'service_name': service_name, 'cash_price': cash_price, 'insurrance_plans': []}
                data_service.append(_dict)
        data_providers = {'provider_name': provider_name, 'provider_address': provider_address, 'services': data_service}
        data.append(data_providers)
    return data


def save_data_json(data, name):
    with open(f'data_{name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def provider_extractor(url):
    driver.get(url)
    provider_name = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="page-title"]/h1'))).text
    elm_eddress = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.XPATH, '//div[@class="sidebar-location"]/p')))
    provider_address = ''
    for i in elm_eddress:
        provider_address += i.text
    services = retract_all_services()
    print(f'Total Services : {len(services)}')
    data_service = []
    for i in services:
        driver.get(i)
        service_name = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
            (By.XPATH, '//div[@class="cost-estimate-info"]/h1'))).text
        try:
            cash_price = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, 'cashPriceAmount'))).text
        except TimeoutException as e:
            cash_price = 'N/A'
        try:
            list_insurances = []
            elm = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//label[@class="payment-select-button"]')))[-1]
            elm.click()
            inssurance_plans = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//select[@id="insurance-plan-selection"]/option')))
            for ins in range(1, len(inssurance_plans) - 1):
                inssurance_plans[ins].click()
                ins_name = inssurance_plans[ins].text
                ins_cash = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//div/ul/li/span[@class="estimate-amount"]')))[-2].text
                _dict_ins = {'ins_name': ins_name, 'ins_cash': ins_cash}
                list_insurances.append(_dict_ins)
            _dict = {'service_name': service_name, 'cash_price': cash_price, 'insurrance_plans': list_insurances}
            data_service.append(_dict)
        except TimeoutException as e:
            _dict = {'service_name': service_name, 'cash_price': cash_price, 'insurrance_plans': []}
            data_service.append(_dict)
    data_providers = {'provider_name': provider_name, 'provider_address': provider_address, 'services': data_service}
    return data_providers


if __name__ == '__main__':
    if args.type == 'S':
        driver.get(state_path.replace("{ST}", args.input))
        state = state_extractor()
        save_data_json(state, args.type)
    elif args.type == 'P':
        provider = provider_extractor(args.input)
        save_data_json(provider, args.input.split('/')[-1])
    else:
        print("Please Insert a valid command")
        exit()
