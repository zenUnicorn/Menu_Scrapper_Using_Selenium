import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def menu_scrapper():
    path = 'C:/Program Files/chromedriver.exe'
    browser=webdriver.Chrome(path)

    browser.get("https://www.just-eat.co.uk/restaurants-chasingdragon-willesdennw10/menu")
    menus_list = []
    try:
        element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, 'skipToMain'))
        )
        #print(element.text)
        categories = element.find_elements_by_css_selector("section.c-menuItems-category.c-card.c-card--noBgColor.c-card--noPad.c-menuItems-category--collapsed")

        for category in categories:
            category_name = category.find_element_by_tag_name('button').find_element_by_tag_name('h3').text
            #print("Category:", category_name)

            all_items = category.find_elements_by_tag_name('div')
            for item in all_items:
                item_name = item.find_element_by_tag_name('header').find_element_by_tag_name('h4').text.strip()
                #print("Item name:", item_name)
                try:
                    unknown_feature = item.find_elements_by_tag_name('p')[0].text.strip().replace("£", '').replace("from", '')
                    item_price = float(unknown_feature)
                    item_desc = ''
                except:
                    item_desc = item.find_elements_by_tag_name('p')[0].text.strip()
                    item_price = item.find_elements_by_tag_name('p')[1].text.strip()
                
                
                #print("description:", item_desc)
                #print("Price:", item_price)

                menu_item = {
                'Category': category_name,
                'Name': item_name,
                'description': item_desc,
                'Price': item_price  
                }
                menus_list.append(menu_item)
                df = pd.DataFrame(menus_list)
                df.to_excel('menu-excel.xls', sheet_name='Sheet1')
                print('inserting done!')


    finally:
        browser.quit()
    

menu_scrapper()
