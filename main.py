from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time


# name, price, hometown, town, photo_url, url


class Parser:
    def __init__(self, search: str, hometown, avito_delivery=False):
        self.url = f'https://www.avito.ru/{hometown}?q={search.replace(" ", "+")}'
        self.avito_delivery = avito_delivery
        self.max = None
        self.min = None
        self.filter_flag = False
        self.list_of_items = []

    def filter(self, minimum, maximum):
        self.max = maximum
        self.min = minimum
        self.filter_flag = True

    def parser(self):
        options_chrome = webdriver.ChromeOptions()
        options_chrome.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                    'like Gecko) Chrome/116.0.0.0 Safari/537.36')
        options_chrome.add_argument('--disable-blink-features=AutomationControlled')
        options_chrome.add_argument('--headless=new')

        with webdriver.Chrome(options=options_chrome) as browser:
            browser.get(self.url)
            time.sleep(5)
            if self.filter_flag:
                minimum = browser.find_element(By.CLASS_NAME, 'input-layout-stick-after-fLNbQ').find_element(By.TAG_NAME, 'input')
                minimum.send_keys(self.min)

                maximum = browser.find_element(By.CLASS_NAME, 'input-layout-stick-both-horizontal-Jx38b').find_element(By.TAG_NAME, 'input')
                maximum.send_keys(self.max)

            if self.avito_delivery:
                checkbox = browser.find_element(By.CLASS_NAME, 'checkbox-input-uPrBY')
                checkbox.click()

            browser.find_element(By.CLASS_NAME, 'button-primary-x_x8w').click()

            count_pagination = int(browser.find_element(By.CLASS_NAME, 'styles-module-item_last-vIJIa').find_element(By.TAG_NAME, 'span').text)

            for _ in range(count_pagination):
                divs_items = browser.find_elements(By.CLASS_NAME, 'items-items-kAJAg')
                hometown = '-'
                for div in divs_items:
                    if div.get_attribute('data-marker'):
                        hometown = '+'

                    for item in div.find_elements(By.CLASS_NAME, 'iva-item-root-_lk9K'):

                        name = item.find_element(By.CLASS_NAME, 'styles-module-root-TWVKW').text
                        price = item.find_element(By.CLASS_NAME, 'styles-module-root-LIAav').find_element(By.TAG_NAME, 'span').text
                        town = item.find_element(By.CLASS_NAME, 'geo-root-zPwRk').find_element(By.TAG_NAME, 'span').text

                        url = item.find_element(By.CLASS_NAME, 'iva-item-sliderLink-uLz1v').get_attribute('href')

                        json_data = {'name': name, 'price': price, 'hometown': hometown, 'town': town, 'url': url}

                        self.list_of_items.append(json_data)

                browser.find_element(By.CLASS_NAME, 'styles-module-listItem_arrow_next-AdI_R').find_element(By.TAG_NAME, 'a').click()

    def create_json_file(self, name):
        with open(f'{name}.json', 'w', encoding='utf-8') as file:
            json.dump(self.list_of_items, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    obj = Parser('Nike Air Force 1', 'murmansk')
    obj.filter(n, m)
    try:
        obj.parser()
    except Exception as err:
        print(err)
    obj.create_json_file('test')
    print('Finished')
