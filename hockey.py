from requests import get
from sys import stderr
import sqlite3
import pandas
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split

SITE = "https://statsapi.web.nhl.com/api/v1"

index_to_team = {}

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

def predict_stanley_cup_winner_in_season(df, season):
        model = Ridge()
        train = df[df['season'] != season]
        test = df[df['season'] == season]
        train = train.drop(['team', 'season'], axis = 1)
        test = test.drop(['team', 'season'], axis = 1)

        Xs_train = train.drop(['playoffRoundWins'], axis = 1)
        y_train = train['playoffRoundWins']
        Xs_test = test.drop(['playoffRoundWins'], axis = 1)
        y_test = test['playoffRoundWins']

        model.fit(Xs_train, y_train)
        pred_values = model.predict(Xs_test)
        print(list(pred_values), list(y_test))

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
        end_year = 2018
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

    global index_to_team
    index_to_team = df[['team']].to_dict()['team']

    df.drop(['index'], axis = 1, inplace = True)
    df = df[df['playoffRoundWins'].notnull()]

    """for i in range(start_year, end_year + 1):
        predict_stanley_cup_winner_in_season(df, str(i) + str(i + 1))"""
    predict_stanley_cup_winner_in_season(df, '20132014')
    #print(df)

if __name__ == "__main__":
    main()

