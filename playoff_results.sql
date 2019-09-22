ALTER TABLE "stanley-cup-predictions" ADD playoffRoundWins INT NULL;
UPDATE "stanley-cup-predictions"
	SET playoffRoundWins = 0
	WHERE (season = '20052006'
		AND team IN ('TBL', 'MTL', 'NYR', 'PHI', 'DET', 'DAL', 'CGY', 'NSH'))
	OR (season = '20062007'
		AND team IN ('NYI', 'TBL', 'ATL', 'PIT', 'CGY', 'MIN', 'DAL', 'NSH'))
	OR (season = '20072008'
		AND team IN ('BOS', 'OTT', 'WSH', 'NJD', 'NSH', 'CGY', 'MIN', 'ANA'))
	OR (season = '20082009'
		AND team IN ('MTL', 'NYR', 'NJD', 'PHI', 'SJS', 'CBJ', 'STL', 'CGY'))
	OR (season = '20092010'
		AND team IN ('WSH', 'NJD', 'BUF', 'OTT', 'COL', 'NSH', 'LAK', 'PHX'))
	OR (season = '20102011'
		AND team IN ('NYR', 'BUF', 'MTL', 'PIT', 'CHI', 'LAK', 'PHX', 'ANA'))
	OR (season = '20112012'
		AND team IN ('OTT', 'BOS', 'FLA', 'PIT', 'VAN', 'SJS', 'CHI', 'DET'))
	OR (season = '20122013'
		AND team IN ('NYI', 'MTL', 'WSH', 'TOR', 'MIN', 'ANA', 'VAN', 'STL'))
	OR (season = '20132014'
		AND team IN ('DET', 'TBL', 'CBJ', 'PHI', 'COL', 'STL', 'DAL', 'SJS'))
	OR (season = '20142015'
		AND team IN ('OTT', 'DET', 'PIT', 'NYI', 'STL', 'NSH', 'WPG', 'VAN'))
	OR (season = '20152016'
		AND team IN ('FLA', 'DET', 'PHI', 'NYR', 'MIN', 'CHI', 'ANA', 'LAK'))
	OR (season = '20162017'
		AND team IN ('MTL', 'BOS', 'TOR', 'CBJ', 'CHI', 'MIN', 'CGY', 'SJS'))
	OR (season = '20172018'
		AND team IN ('NJD', 'TOR', 'CBJ', 'PHI', 'COL', 'MIN', 'LAK', 'ANA'))
	OR (season = '20182019'
		AND team IN ('TBL', 'TOR', 'WSH', 'PIT', 'NSH', 'WPG', 'CGY', 'VGK'));

UPDATE "stanley-cup-predictions"
	SET playoffRoundWins = 1
	WHERE (season = '20082009'
		AND team IN ('BOS', 'WSH', 'ANA', 'VAN'))
	OR (season = '20092010'
		AND team IN ('PIT', 'BOS', 'DET', 'VAN'))
	OR (season = '20102011'
		AND team IN ('WSH', 'PHI', 'NSH', 'DET'))
	OR (season = '20112012'
		AND team IN ('WSH', 'PHI', 'STL', 'NSH'))
	OR (season = '20122013'
		AND team IN ('OTT', 'NYR', 'DET', 'SJS'))
	OR (season = '20132014'
		AND team IN ('BOS', 'PIT', 'MIN', 'ANA'))
	OR (season = '20142015'
		AND team IN ('MTL', 'WSH', 'MIN', 'CGY'))
	OR (season = '20152016'
		AND team IN ('NYI', 'WSH', 'DAL', 'NSH'))
	OR (season = '20162017'
		AND team IN ('NYR', 'WSH', 'STL', 'EDM'))
	OR (season = '20172018'
		AND team IN ('BOS', 'PIT', 'NSH', 'SJS'))
	OR (season = '20182019'
		AND team IN ('CBJ', 'NYI', 'DAL', 'COL'));

UPDATE "stanley-cup-predictions"
	SET playoffRoundWins = 2
	WHERE (season = '20082009'
		AND team IN ('CAR', 'CHI'))
	OR (season = '20092010'
		AND team IN ('MTL', 'SJS'))
	OR (season = '20102011'
		AND team IN ('TBL', 'SJS'))
	OR (season = '20112012'
		AND team IN ('NYR', 'PHX'))
	OR (season = '20122013'
		AND team IN ('PIT', 'LAK'))
	OR (season = '20132014'
		AND team IN ('MTL', 'CHI'))
	OR (season = '20142015'
		AND team IN ('NYR', 'ANA'))
	OR (season = '20152016'
		AND team IN ('TBL', 'STL'))
	OR (season = '20162017'
		AND team IN ('OTT', 'ANA'))
	OR (season = '20172018'
		AND team IN ('TBL', 'WPG'))
	OR (season = '20182019'
		AND team IN ('CAR', 'SJS'));

UPDATE "stanley-cup-predictions"
	SET playoffRoundWins = 3
	WHERE (season = '20052006'
		AND team = 'EDM')
	OR (season = '20062007'
		AND team = 'OTT')
	OR (season = '20072008'
		AND team = 'PIT')
	OR (season = '20082009'
		AND team = 'DET')
	OR (season = '20092010'
		AND team = 'PHI')
	OR (season = '20102011'
		AND team = 'VAN')
	OR (season = '20112012'
		AND team = 'NJD')
	OR (season = '20122013'
		AND team = 'BOS')
	OR (season = '20132014'
		AND team = 'NYR')
	OR (season = '20142015'
		AND team = 'TBL')
	OR (season = '20152016'
		AND team = 'SJS')
	OR (season = '20162017'
		AND team = 'NSH')
	OR (season = '20172018'
		AND team = 'VGK')
	OR (season = '20182019'
		AND team = 'BOS');

UPDATE "stanley-cup-predictions"
	SET playoffRoundWins = 4
	WHERE (season = '20052006'
		AND team = 'CAR')
	OR (season = '20062007'
		AND team = 'ANA')
	OR (season = '20072008'
		AND team = 'DET')
	OR (season = '20082009'
		AND team = 'PIT')
	OR (season = '20092010'
		AND team = 'CHI')
	OR (season = '20102011'
		AND team = 'BOS')
	OR (season = '20112012'
		AND team = 'LAK')
	OR (season = '20122013'
		AND team = 'CHI')
	OR (season = '20132014'
		AND team = 'LAK')
	OR (season = '20142015'
		AND team = 'CHI')
	OR (season = '20152016'
		AND team = 'PIT')
	OR (season = '20162017'
		AND team = 'PIT')
	OR (season = '20172018'
		AND team = 'WSH')
	OR (season = '20182019'
		AND team = 'STL');
