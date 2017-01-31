# Scraping info from additional links
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
player_links = []
player_df = pd.DataFrame(columns = constants.DRAFT_COLUMNS)
with open ('data/extra_player_links.pkl', 'rb') as fp:
    player_links = pickle.load(fp)

for link in player_links:
    try:
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        player_series = scraping.get_player_data(soup)
        player_df = player_df.append(player_series, ignore_index=True, verify_integrity=True)
    except Exception:
        pass

# Fetch pre draft measurements and add that to the dataframe
player_df.to_csv('data/additional_draft_data.csv')
