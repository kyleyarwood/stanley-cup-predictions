from requests import get
from sys import stderr
import sqlite3
import pandas
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split

from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamyearbyyearstats
from json import loads

SITE = "https://statsapi.web.nhl.com/api/v1"

acronyms = {"Anaheim Ducks": "ANA", "Arizona Coyotes": "ARZ", "Atlanta Thrashers": "ATL",
        "Boston Bruins": "BOS", "Buffalo Sabres": "BUF", "Calgary Flames": "CGY",
        "Carolina Hurricanes": "CAR", "Chicago Blackhawks": "CHI", "Colorado Avalanche": "COL",
        "Columbus Blue Jackets": "CBJ", "Dallas Stars": "DAL", "Detroit Red Wings": "DET",
        "Edmonton Oilers": "EDM", "Florida Panthers": "FLA", "Los Angeles Kings": "LAK",
        "Minnesota Wild": "MIN", "Montréal Canadiens": "MTL", "Nashville Predators": "NSH",
        "New Jersey Devils": "NJD", "New York Islanders": "NYI", "New York Rangers": "NYR",
        "Ottawa Senators": "OTT", "Philadelphia Flyers": "PHI", "Phoenix Coyotes": "PHX",
        "Pittsburgh Penguins": "PIT", "San Jose Sharks": "SJS", "St. Louis Blues": "STL",
        "Tampa Bay Lightning": "TBL", "Toronto Maple Leafs": "TOR", "Vancouver Canucks": "VAN",
        "Vegas Golden Knights": "VGK", "Washington Capitals": "WSH", "Winnipeg Jets": "WPG"}

nba_acronyms = {"Philadelphia 76ers": "PHI", "Brooklyn Nets": "BKN", "Milwaukee Bucks": "MIL",
        "New York Knicks": "NYK", "Atlanta Hawks": "ATL", "Boston Celtics": "BOS",
        "Miami Heat": "MIA", "Charlotte Hornets": "CHA", "Indiana Pacers": "IND",
        "Washington Wizards": "WSH", "Toronto Raptors": "TOR", "Chicago Bulls": "CHI",
        "Orlando Magic": "ORL", "Cleveland Cavaliers": "CLE", "Detroit Pistons": "DET",
        "Utah Jazz": "UTA", "Phoenix Suns": "PHX", "Denver Nuggets": "DEN",
        "LA Clippers": "LAC", "Los Angeles Clippers": "LAC", "Dallas Mavericks": "DAL", "LA Lakers": "LAL", "Los Angeles Lakers": "LAL",
        "Portland Trail Blazers": "POR", "Memphis Grizzlies": "MEM", "Golden State Warriors": "GSW",
        "San Antonio Spurs": "SAS", "New Orleans Pelicans": "NOP", "New Orleans Hornets": "NOH", "New Orleans/Oklahoma City Hornets": "NOH", "Sacramento Kings": "SAC",
        "Oklahoma City Thunder": "OKC", "Minnesota Timberwolves": "MIN", "Houston Rockets": "HOU", 
        "Seattle SuperSonics": "SEA", "New Jersey Nets": "NJN", "Vancouver Grizzlies": "VAN", "Charlotte Bobcats": "CHA"}

def get_season_data(info: str, season: str, options: str):
    """
    info: Information to be fetched (/teams?season= for team data)
    season: String containing season that the data is coming from
    (e.g. 20182019 for the 2018-19 season)
    options: Extra options for the request (e.g. expand=team.stats
    for team stats)

    Returns: pandas dataframe containing the data of each team from the season
    """
    data = get(SITE + info + season + options)
    teams = None
    try:
        teams = data.json()
        teams = teams["teams"]
    except:
        stderr.write("error getting data from NHL API")
        return None
    
    stats_columns = {"team": []}

    for team in teams:
        team_name = team["name"]
        print(team_name)
        #print(team)
        team_stats = team["teamStats"][0]["splits"]
        absolute_stats = team_stats[0]["stat"]
        ranking_stats = team_stats[1]["stat"]
        stats_columns["team"].append(acronyms[team_name])
        for stat in absolute_stats:
            if stat not in stats_columns:
                stats_columns[stat] = [absolute_stats[stat]]
            else:
                stats_columns[stat].append(absolute_stats[stat])

    df = pandas.DataFrame.from_dict(stats_columns)
    df["season"] = season
    return df

def get_nba_team_data_for_years_from_file(start_year, end_year):
    years = {'{}-{}'.format(yr, str(yr+1)[-2:]) for yr in range(start_year, end_year+1)}
    with open('nbaresponses.txt', 'r') as f:
        teams = f.readlines()
    hdrs = []
    print(len(teams))
    stats_columns = {"team": [], "playoffRoundWins": []}
    for team in teams:
        stats = loads(team)
        stats = stats['resultSets'][0]
        if not hdrs:
            hdrs = stats['headers']
        seasons = stats['rowSet']
        for season in seasons:
            if season[3] not in years:
                continue
            name = ' '.join(season[1:3])
            stats_columns["team"].append(nba_acronyms[name] if name in nba_acronyms else None)
            for stat,value in zip(hdrs,season):
                if stat not in stats_columns:
                    stats_columns[stat] = [value]
                else:
                    stats_columns[stat].append(value)
            if stats_columns["PO_LOSSES"][-1] == 0:
                stats_columns["playoffRoundWins"].append(None)
            else:
                stats_columns["playoffRoundWins"].append(stats_columns["PO_WINS"][-1]//4)
    df = pandas.DataFrame.from_dict(stats_columns)
    print(df)
    return df

def get_nba_team_data_for_years(start_year, end_year):
    years = {'{}-{}'.format(yr, str(yr+1)[-2:]) for yr in range(start_year, end_year+1)}
    tms = teams.get_teams()
    hdrs = []
    stats_columns = {"team": []}
    for tm in tms:
        print(tm)
        try:
            x = teamyearbyyearstats.TeamYearByYearStats(tm['id']).nba_response._response
            with open('nbaresponses.txt', 'r') as f:
                x = f.read
            stats = loads(x)
        except:
            break
        print(stats)
        stats = stats['resultSets'][0]
        if not hdrs:
            hdrs = stats['headers']
        seasons = stats['rowSet']
        for season in seasons:
            if season[3] not in years:
                continue
            name = ' '.join(season[1:3])
            stats_columns["team"].append(nba_acronyms[name] if name in nba_acronyms else None)
            for stat,value in zip(hdrs,season):
                if stat not in stats_columns:
                    stats_columns[stat] = [value]
                else:
                    stats_columns[stat].append(value)
    df = pandas.DataFrame.from_dict(stats_columns)
    print(df)
    return df

def main():
    """
    TODO: analyze season_tables to determine which team will win
    the Stanley Cup
    """
    #print("Starting...")
    info = "/teams?season="
    season = "20182019"
    options = "&expand=team.stats"
    df = None
    conn = sqlite3.connect("scpreds.db")
    cur = conn.cursor()
    query = "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
    query += " AND name='stanley-cup-predictions'"
    result = cur.execute(query)
    for row in result:
        db_exists = row[0]
    
    print(db_exists)

    if not db_exists:
        start_year = 2005
        end_year = 2021
        df_created = False
        for i in range(end_year, start_year - 1, -1):
            season = str(i) + str(i + 1)
            new_df = get_season_data(info, season, options)
            if df_created:
                df = df.append(new_df, ignore_index = True)
            else:
                df_created = True
                df = new_df
        df.to_sql("stanley-cup-predictions", conn)
        f = open("playoff_results.sql", "r")
        content = f.read()
        queries = content.split(";")
        for query in queries:
            cur.execute(query)
            conn.commit()
    df = pandas.read_sql("SELECT * FROM 'stanley-cup-predictions'", conn)
    df.drop(['index'], axis = 1, inplace = True)
    df = df[df['playoffRoundWins'].notnull()]

    #_2021_df = get_season_data(info, '20202021', options)
    _2020_df = get_season_data(info, '20202021', options)
    print(_2020_df)
    #print(_2021_df)

    model = Ridge()
    df = df[df['season'] != '20202021']
    useful_stats = df.drop(['team', 'season'], axis = 1)
    Xs = useful_stats.drop(['playoffRoundWins'], axis = 1)
    y = useful_stats['playoffRoundWins']
    Xs_train, Xs_test, y_train, y_test = train_test_split(Xs, y, test_size = 0.33)
    print(Xs, y)
    model.fit(Xs, y)
    #pred_values = model.predict(Xs_test)
    #print(pred_values)
    #print(df)

    _2020_df.drop(['team', 'season'], axis=1, inplace=True)
    _2020_pred_values = model.predict(_2020_df)
    print(_2020_pred_values)

def nba_main():

    '''
    df = get_nba_team_data_for_years_from_file(1980, 2020)
    print(df)
    '''
    conn = sqlite3.connect("scpreds.db")
    cur = conn.cursor()
    '''
    df.to_sql("nba_predictions", conn)

    f = open("nba_playoff_results.sql", "r")
    content = f.read()
    queries = content.split(";")
    for query in queries:
        cur.execute(query)
        conn.commit()
    '''
    df = pandas.read_sql("SELECT * FROM 'nba_predictions'", conn)
    df = df[('2010-11' <= df['YEAR']) & (df['YEAR'] <= '2020-21')]
    df.drop(['index'], axis = 1, inplace = True)
    _2020_df = df[df['YEAR'] == '2020-21']
    df = df[df['playoffRoundWins'].notnull()]
    #_2020_df = _2020_df[_2020_df['playoffRoundWins'].notnull()]

    print(_2020_df)
    _2020_wins = _2020_df['PO_WINS']
    _2020_df.drop(['team', 'TEAM_ID', 'TEAM_CITY', 'TEAM_NAME', 'YEAR', 'NBA_FINALS_APPEARANCE', 'PO_WINS', 'PO_LOSSES', 'playoffRoundWins'], axis = 1, inplace=True)
    df = df[df['YEAR'] != '2019-20']
    model = Ridge()
    useful_stats = df.drop(['team', 'TEAM_ID', 'TEAM_CITY', 'TEAM_NAME', 'YEAR', 'NBA_FINALS_APPEARANCE', 'playoffRoundWins', 'PO_LOSSES'], axis = 1)
    Xs = useful_stats.drop(['PO_WINS'], axis = 1)
    y = useful_stats['PO_WINS']
    Xs_train, Xs_test, y_train, y_test = train_test_split(Xs, y, test_size = 0.33)
    print(Xs, y)
    model.fit(Xs, y)
    #pred_values = model.predict(Xs_test)
    pred_values = model.predict(_2020_df)
    print(pred_values)
    print(model.score(_2020_df, _2020_wins))
    #print(Xs_test)

if __name__ == "__main__":
    main()
    #nba_main()

