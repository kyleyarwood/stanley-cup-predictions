from requests import get
from sys import stderr
import pandas

SITE = "https://statsapi.web.nhl.com/api/v1"
index_to_stat = []
constructed = False #only construct index_to_stat once

def get_season_data(info: str, season: str, options: str):
    """
    info: Information to be fetched (/teams?season= for team data)
    season: String containing season that the data is coming from
    (e.g. 20182019 for the 2018-19 season)
    options: Extra options for the request (e.g. expand=team.stats
    for team stats)

    Returns: pandas dataframe containing the data of each team from the season

    Modifies index_to_stat to be a list of the stats in each row
    (index_to_stat[i] is the stat represented by row i in the dataframe)
    """
    data = get(SITE + info + season + options)
    teams = None
    global index_to_stat
    global constructed

    try:
        teams = data.json()
        teams = teams["teams"]
    except:
        stderr.write("error getting data from NHL API")
        return None
    
    team_columns = {}

    for team in teams:
        team_name = team["name"]
        #print(team_name)
        #print(team)
        team_stats = team["teamStats"][0]["splits"]
        absolute_stats = team_stats[0]["stat"]
        ranking_stats = team_stats[1]["stat"]
        team_columns[team_name] = list(absolute_stats.values())
        if not constructed:
            constructed = True
            index_to_stat = list(absolute_stats.keys())

    df = pandas.DataFrame.from_dict(team_columns)            
    #print(df)
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

    season_tables = {}
    start_year = 2018
    end_year = 2018
    for i in range(start_year, end_year + 1):
        season = str(i) + str(i + 1)
        season_tables[i] = get_season_data(info, season, options)

if __name__ == "__main__":
    main()

