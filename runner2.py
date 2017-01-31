# Open each of the player's links and scrapes through the information.

import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import scraping
import constants
import time

chromedriver = "/Applications/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

player_df = pd.DataFrame(columns = constants.DRAFT_COLUMNS)
player_links = []

with open ('data/player_links.pkl', 'rb') as fp:
    player_links = pickle.load(fp)

for link in player_links:
    try:
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        player_series = scraping.get_player_data(soup)
            player_df = player_df.append(player_series, ignore_index=True, verify_integrity=True)
        time.sleep(0.2)
    except Exception:
        pass

player_df.to_csv('data/draft_info.csv')
