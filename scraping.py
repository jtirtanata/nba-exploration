from bs4 import BeautifulSoup
import pandas as pd
import re
import constants

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
    return int(m.group('weight'))

def get_draft_year_urls(soup, start, end=None):
	"""
	Get the links that lists the nba players drafted for each year

	Args:
		soup: The soup object
		start: The earliest year that you want to fetch the url for.
		end: The last year that you want to fetch the url for.

	Returns:
    	List of urls.
	"""
	table = soup.find(id='first_overall')
	if end is None:
		end = int(table.find_all('tr')[1].find("th",\
		 {"data-stat" : 'year_id'}).text)
	urls = []
	for i in range(start, end + 1):
	    urls.append(table.find('th', text=str(i)).a['href'])
	return ['http://www.basketball-reference.com' + url for url in urls]

def get_all_player_data(soup):
	"""
	Get the links of all of the nba players of that year and a dataframe that
	contains the player's name, college_id, and draft_year.
	e.g. links, df = get_all_player_data(soup)

	Args:
		soup: The soup object.

	Returns:
    	List of nba player's links and a dataframe of all of the player's
			information.
	"""
	draft_year = soup.find("h1", {"itemprop" : 'name'}).span.text
	body = soup.find(id='stats').tbody
	df = pd.DataFrame(columns = ['name', 'college', 'draft_rank', 'draft_year'])
	links = []
	for row in body.find_all('tr'):
		college = row.find('td', {'data-stat': 'college_name'})
		player = row.find('td', {'data-stat': 'player'})
		# no stats for player that doesn't have an anchor tag
		# no college stats when college name is not displayed
		if college and player and college.text and player.a:
			draft_rank = row.find('td', {'data-stat': 'pick_overall'})
			fields = {'name': player.text, 'college': college.text,\
			 'draft_rank': draft_rank.text, 'draft_year': draft_year }
			df = df.append(fields, ignore_index=True)
			links.append(player.a['href'])
	links = ['http://www.basketball-reference.com' + url for url in links]
	return df, links

def get_player_data(soup):
	"""
	Get player data from soup object.

	Args:
    	soup: The soup object containing the player's info.

	Returns:
    	Series that can be appended to the dataframe.
	"""
	table = soup.find(id='all_college_stats')
	if not table or not table.tbody:
		return
	table_rows = table.tbody.find_all('tr')
	name = soup.find("h1", {"itemprop" : 'name'}).text
	print(name)
	per = soup.find('h4', text='PER').find_next_sibling().text
	no_of_seasons = len(table_rows)
	start_age = table_rows[0].find("td", {"data-stat" : 'age'}).text
	end_age = table_rows[-1].find("td", {"data-stat" : 'age'}).text
	career_data = [table.tfoot.find("td", {"data-stat" : stat}).text for stat in constants.CAREER_COLUMNS]
	print(career_data)
	weight = soup.find('span', {'itemprop':'weight'}).text
	weight = fetch_weight(weight)
	height = convert_to_inches(soup.find('span', {'itemprop':'height'}).text)
	print(weight, height)
	all_data = [name, per, no_of_seasons, start_age, end_age, weight, height] + career_data
	columns = ['name', 'per', 'no_of_seasons', 'start_age', 'end_age', 'weight_lb', 'height_in'] +\
		constants.CAREER_COLUMNS
	return pd.Series(all_data, index=columns)
