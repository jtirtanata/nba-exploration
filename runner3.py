# Fetching in the null heights and weights
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

player_ref_link = 'http://www.basketball-reference.com/players/{}/'

df_measurement = pd.read_csv('data/player_measurement.csv', index_col=0)
df_draft = pd.read_csv('data/draft_info.csv', index_col=0)
df = pd.merge(df_measurement, df_draft, on='name')
null_height = list(df[df.height_in.isnull()]['name'])

def get_last_initial(s):
    last_name = s.split()[-1]
    return last_name[0].lower()
def get_player_link(soup, name):
    name = soup.find('a', text=name)
    if name:
        return name['href']
    else:
        return None
def convert_to_inches(s):
    if s == '':
        return ''
    m = re.match(r"(?P<feet>\d+)\-(?P<inches>\d+\.?\d*)", s)
    if not m:
        return np.nan
    feet = int(m.group('feet'))
    inches = float(m.group('inches'))
    return feet * 12 + inches
def fetch_weight(s):
    if s == '':
        return ''
    m = re.match(r"(?P<weight>\d+)lbs*", s)
    if not m:
        return np.nan
    return m.group('weight')

for name in null_height:
    result = requests.get(player_ref_link.format(get_last_initial(name)))
    assert (result.status_code == 200),"Can't fetch main draft page"
    soup = BeautifulSoup(result.text, 'html.parser')
    player_link = get_player_link(soup, name)
    if player_link:
        player_result = requests.get('http://www.basketball-reference.com' + player_link)
        soup = BeautifulSoup(player_result.text, 'html.parser')
        weight = fetch_weight(soup.find('span', {'itemprop':'weight'}).text)
        height = convert_to_inches(soup.find('span', {'itemprop':'height'}).text)
        df.ix[df.name==name, 'weight_lb'] = weight
        df.ix[df.name==name, 'height_in'] = height


df.to_csv('data/data.csv')
