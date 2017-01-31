CAREER_COLUMNS = ['g', 'mp', 'fg', 'fga', 'fg3', 'fg3a', 'ft', 'fta', 'orb',\
    'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'fg_pct', 'fg3_pct', 'ft_pct', \
    'mp_per_g', 'pts_per_g', 'trb_per_g', 'ast_per_g']
COLUMNS = ['name', 'per','no_of_seasons', 'start_age', 'end_age', 'college',\
    'draft_year', 'draft_rank'] + CAREER_COLUMNS
MAIN_URL = 'http://www.basketball-reference.com/draft/'
DRAFT_COLUMNS = ['name', 'per','no_of_seasons', 'start_age', 'end_age'] + CAREER_COLUMNS
OTHER_COLUMNS = ['name', 'draft_year', 'draft_rank', 'college', 'wingspan_in', 'height_in', 'reach_in', 'weight_lb']
ALL_COLUMNS = DRAFT_COLUMNS + OTHER_COLUMNS[1:]

MEASUREMENTS_URL = 'http://www.draftexpress.com/nba-pre-draft-measurements/?page=&year={}&source=All&sort2=DESC&draft=0&pos=0&sort='
