ALTER TABLE "nba_predictions" ADD playoffRoundWins INT NULL;
UPDATE "nba_predictions"
    SET playoffRoundWins = 0
    WHERE (YEAR = '2014-15'
        AND team IN ('BKN', 'MIL', 'BOS', 'TOR', 'NOP', 'DAL', 'SAS', 'POR'))
    OR (YEAR = '2015-16'
        AND team IN ('BOS', 'DET', 'CHA', 'IND', 'HOU', 'DAL', 'LAC', 'MEM'))
    OR (YEAR = '2016-17'
        AND team IN ('CHI', 'IND', 'MIL', 'ATL', 'POR', 'OKC', 'MEM', 'LAC'))
    OR (YEAR = '2017-18'
        AND TEAM IN ('MIL', 'IND', 'MIA', 'WSH', 'SAS', 'MIN', 'POR', 'OKC'))
    OR (YEAR = '2018-19'
        AND team IN ('IND', 'DET', 'BKN', 'ORL', 'SAS', 'LAC', 'UTA', 'OKC'))
    OR (YEAR = '2019-20'
        AND team IN ('PHI', 'IND', 'ORL', 'BKN', 'UTA', 'OKC', 'DAL', 'POR'));
UPDATE "nba_predictions"
    SET playoffRoundWins = 1
    WHERE (YEAR = '2014-15'
        AND team IN ('WSH', 'CHI', 'MEM', 'LAC'))
    OR (YEAR = '2015-16'
        AND team IN ('ATL', 'MIA', 'POR', 'SAS'))
    OR (YEAR = '2016-17'
        AND team IN ('WSH', 'TOR', 'UTA', 'HOU'))
    OR (YEAR = '2017-18'
        AND team IN ('PHI', 'TOR', 'NOP', 'UTA'))
    OR (YEAR = '2018-19'
        AND team IN ('BOS', 'PHI', 'HOU', 'DEN'))
    OR (YEAR = '2019-20'
        AND team IN ('TOR', 'MIL', 'LAC', 'HOU'));
UPDATE "nba_predictions"
    SET playoffRoundWins = 2
    WHERE (YEAR = '2014-15'
        AND team IN ('ATL', 'HOU'))
    OR (YEAR = '2015-16'
        AND team IN ('TOR', 'OKC'))
    OR (YEAR = '2016-17'
        AND team IN ('BOS', 'SAS'))
    OR (YEAR = '2017-18'
        AND team IN ('BOS', 'HOU'))
    OR (YEAR = '2018-19'
        AND team IN ('MIL', 'POR'))
    OR (YEAR = '2019-20'
        AND team IN ('BOS', 'DEN'));
UPDATE "nba_predictions"
    SET playoffRoundWins = 3
    WHERE (YEAR = '2014-15'
        AND team = 'CLE')
    OR (YEAR = '2015-16'
        AND team = 'GSW')
    OR (YEAR = '2016-17'
        AND team = 'CLE')
    OR (YEAR = '2017-18'
        AND team = 'CLE')
    OR (YEAR = '2018-19'
        AND team = 'GSW')
    OR (YEAR = '2019-20'
        AND team = 'MIA');
UPDATE "nba_predictions"
    SET playoffRoundWins = 4
    WHERE (YEAR = '2014-15'
        AND team = 'GSW')
    OR (YEAR = '2015-16'
        AND team = 'CLE')
    OR (YEAR = '2016-17'
        AND team = 'GSW')
    OR (YEAR = '2017-18'
        AND team = 'GSW')
    OR (YEAR = '2018-19'
        AND team = 'TOR')
    OR (YEAR = '2019-20'
        AND team = 'LAL');