from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time
import os

web = "https://twitter.com/i/flow/login"

options = Options()
options.page_load_strategy = 'normal'
# options.headless = True
options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome(options=options)
driver.get(web)
driver.maximize_window()

time.sleep(2)

def login():
    username = driver.find_element(By.XPATH, '//input[@autocomplete ="username"]')
    username.send_keys(os.environ.get("TWITTER_USER"))

    next_button = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Next"]')
    next_button.click()
    time.sleep(2)

    password = driver.find_element(By.XPATH, '//input[@autocomplete ="current-password"]')
    username.send_keys(os.environ.get("TWITTER_PASSWORD"))

    login_button = driver.find_element(By.XPATH, '//div[@role="button"]//span[text()="Log in"]')
    login_button.click()


def get_tweet(element):
    try:
        user = element.find_element(By.XPATH, ".//span[contains(text(), '@')]").text
        text = element.find_element(By.XPATH, ".//div[@lang]").text
        tweet_data = [user, text]
    except:
        tweet_data = ['user', 'text']
    return tweet_data

login()
user_data = []
text_data = []
tweet_ids = set()
scrolling = True
while scrolling:
    time.sleep(2)
    tweets = driver.find_elements(By.XPATH, "//article[@role='article']")
    print(len(tweets))
    for tweet in tweets[-15:]:  # you can change this number with the number of tweets in a website || NOTE: ONLY THOSE LOADED IN THE last page will be considered while those from previous page will be forgotten (example: scroll all the way down and then try to find an @username that it's on top --> it won't find it)
        tweet_list = get_tweet(tweet)
        tweet_id = ''.join(tweet_list)
        if tweet_id not in tweet_ids:
            tweet_ids.add(tweet_id)
            user_data.append(tweet_list[0])
            text_data.append(" ".join(tweet_list[1].split()))

    # Get the initial scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(2)
        # Calculate new scroll height and compare it with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        # condition 1
        if new_height == last_height:  # if the new and last height are equal, it means that there isn't any new page to load, so we stop scrolling
            scrolling = False
            break
        # condition 2
        # if len(data) > 60:
        #     scrolling = False
        #     break
        else:
            last_height = new_height
            break


driver.quit()

df_tweets = pd.DataFrame({'user': user_data, 'text': text_data})
df_tweets.to_csv('tweets_pagination.csv', index=False)
print(df_tweets)
