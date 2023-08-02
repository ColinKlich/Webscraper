from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time

web = "https://www.audible.com/adblbestsellers?ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=1bb99d4d-8ec8-42a3-bb35-704e849c2bc6&pf_rd_r=TZ3K2M1E0BHX4WW4B0Y1&pageLoadId=ppBWnjwnLfDJnHnc&creativeId=1642b4d1-12f3-4375-98fa-4938afc1cedc"

options = Options()
options.page_load_strategy = 'normal'
options.headless = True
options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome(options=options)
driver.get(web)
# driver.maximize_window()

#pagination
pagination = driver.find_element(By.XPATH, ".//ul[contains(@class, 'pagingElements')]")
pages = pagination.find_elements(By.TAG_NAME, "li")
last_page = int(pages[-2].text)

curr_pg = 1

book_title = []
book_author = []
book_runtime = []

while curr_pg <= last_page:
    time.sleep(2)
    # container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container')))
    container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')
    # products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './li')))
    products = container.find_elements(By.XPATH, ".//li[contains(@class, 'productListItem')]")

    for product in products:
        title = product.find_element(By.XPATH, ".//h3[contains(@class, 'bc-heading')]").text
        book_title.append(title)
        book_author.append(product.find_element(By.XPATH, ".//li[contains(@class, 'authorLabel')]").text)
        book_runtime.append(product.find_element(By.XPATH, ".//li[contains(@class, 'runtimeLabel')]").text)
        print("Loaded data from: ", title)
    
    next_page = driver.find_element(By.XPATH, "//span[contains(@class, 'nextButton')]")
    next_page.click()
    curr_pg += 1

driver.quit()

df_books = pd.DataFrame({'Title': book_title, 'Author': book_author, 'Run Time': book_runtime})
df_books.to_csv('books.csv', index=False)