# Getting links to players from 1980 - 1996
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re

import scraping
import constants
import runner1
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import scraping
import constants
import time
import pickle
chromedriver = "/Applications/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

result = requests.get(constants.MAIN_URL)
assert (result.status_code == 200),"Can't fetch main draft page"
soup = BeautifulSoup(result.text, 'html.parser')

links = scraping.get_draft_year_urls(soup, 1980, 1997)

# with open ('data/player_links.pkl', 'rb') as fp:
#     player_links = pickle.load(fp)

df = pd.DataFrame(columns=constants.OTHER_COLUMNS)
player_df = pd.DataFrame(columns = constants.DRAFT_COLUMNS)
player_links = []
for link in links:
    result = requests.get(link)
    assert (result.status_code == 200),"Can't fetch main draft page"
    soup = BeautifulSoup(result.text, 'html.parser')
    temp_df, p_links = scraping.get_all_player_data(soup)
    player_links.extend(p_links)

with open('data/extra_player_links.pkl','wb') as f:
    pickle.dump(player_links,f)
# for link in player_links:
#     try:
#         driver.get(link)
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         player_series = scraping.get_player_data(soup)
#         player_df = player_df.append(player_series, ignore_index=True, verify_integrity=True)
#         time.sleep(0.2)
#     except Exception:
#         pass

# Fetch pre draft measurements and add that to the dataframe
# df.to_csv('data/additional_data.csv')
# player_df.to_csv('data/additional_draft_data.csv')
