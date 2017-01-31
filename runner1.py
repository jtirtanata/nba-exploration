from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re

import scraping
import constants

def convert_to_inches(s):
    if s == '':
        return ''
    m = re.match(r"(?P<feet>\d+)\' (?P<inches>\d+\.?\d*)\"", s)
    if not m:
        return np.nan
    feet = int(m.group('feet'))
    inches = float(m.group('inches'))
    return feet * 12 + inches

def get_value(row, td_name):
    td = row.find("td", {"data-title": td_name})
    if td:
        return td.text
    else:
        return ''

def insert_measurement(value, df, index, column_name):
    if value != '':
        df.ix[index, column_name] = value


result = requests.get(constants.MAIN_URL)
assert (result.status_code == 200),"Can't fetch main draft page"
soup = BeautifulSoup(result.text, 'html.parser')

links = scraping.get_draft_year_urls(soup, 1997)

df = pd.DataFrame(columns=constants.OTHER_COLUMNS)
player_links = []
for link in links:
    result = requests.get(link)
    assert (result.status_code == 200),"Can't fetch main draft page"
    soup = BeautifulSoup(result.text, 'html.parser')
    temp_df, p_links = scraping.get_all_player_data(soup)
    player_links.extend(p_links)
    df = df.append(temp_df, ignore_index=True)

# Fetch pre draft measurements and add that to the dataframe
for year in range(1997, 2017):
    result = requests.get(constants.MEASUREMENTS_URL.format(year))
    soup = BeautifulSoup(result.text, 'html.parser')
    player_rows = soup.table.find_all('tr')[1:]
    for row in player_rows:
        name = row.a.text.strip()
        i = df[df.name == name].index.values
        if len(i) > 1:
            # name is not unique
            rank = get_value(row, 'Drafted')
            if rank.isdigit():
                i = df[(df.name == name) & (df.draft_rank == int(rank))].index.values
            else:
                i = None
        if i:
            wingspan = convert_to_inches(get_value(row,'Wingspan'))
            insert_measurement(wingspan, df, i, 'wingspan_in')
            reach = convert_to_inches(get_value(row,'Reach'))
            insert_measurement(reach, df, i, 'reach_in')
            height = convert_to_inches(get_value(row,'Height'))
            insert_measurement(height, df, i, 'height_in')
            weight = get_value(row, 'Weight')
            insert_measurement(weight, df, i, 'weight_lb')

df.to_csv('data/player_measurement.csv')
