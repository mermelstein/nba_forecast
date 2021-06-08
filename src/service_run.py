from scrapers.score_scraper import score_scraper
from scrapers.upcoming_scraper import upcoming_scraper
from utils.db_connection import queryDB, writeDB
from models.prediction_model import predictions
from site_update import preds, accuracy
import subprocess

if __name__ == '__main__':
	print("SUCCESS: docker running the service orchestrator")

# determine which part of the season we're in
page = queryDB("""
select 
  gs.page,
  gs.results
from season_dates sd
join game_source gs on gs.category = sd.category
where current_date between sd.start_date and sd.end_date
""")

game_page = page['page'][0]
results_page = page['results'][0]

# run scrapers
games = score_scraper(results_page)
	# add to games table if no duplication
db_games = queryDB("select game_id, game_date||home||away as joiner from games")
games['joiner'] = games['game_date'].astype(str) + games['home'] + games['away']
	# check which games are missing
new_games = games.merge(db_games.loc[:, ['game_id', 'joiner']], how='left', on='joiner')
new_games = new_games[new_games['game_id'].isnull()]

	# write to the db if there are new games
if new_games.empty == True:
	print('no new games')
else:
	# write to games table and generate game_id
	writeDB(new_games.loc[:, ['game_date', 'home', 'away']], 'games')

	# check if scores are missing
db_scores = queryDB("""
select 
  g.game_id,
  g.game_date||g.home||g.away as joiner
from games g
left join scores s on s.game_id = g.game_id 
where s.game_id is null""")
	# check which scores are missing
new_scores = games.merge(db_scores.loc[:, ['game_id', 'joiner']], how='inner', on='joiner')

if new_scores.empty == True:
	print('no new scores')
else:
	# write new data to scores table
	writeDB(new_scores.drop(columns=['joiner', 'run_date']), 'scores')
	print(str(len(new_scores)) + ' new scores written to db')
	# re-run predictions for any upcoming games with this new input
	predict_games = queryDB("select * from games where game_date::date >= current_date")
	if predict_games.empty == True:
		print('no upcoming games that need to have updated predictions')
	else:
		predictions_df = predictions(predict_games[["game_id", "game_date", "home", "away"]])
		writeDB(predictions_df.loc[:, ['game_id', 'run_date', 'win_pred']], 'predictions')
		print('predictions updated for ' + str(len(predict_games)) + ' games')

# collect upcoming games and run predictions
upcoming_games = upcoming_scraper(game_page)
	# add to games table if no duplication
upcoming_games['joiner'] = upcoming_games['game_date'].astype(str) + upcoming_games['home'] + upcoming_games['away']
	# check which games are missing
new_games = upcoming_games.merge(db_games.loc[:,['game_id','joiner']], how='left', on='joiner')
new_games = new_games[new_games['game_id'].isnull()]

	# write to the db if there are new games and run predictions for upcoming games
if new_games.empty == True:
	print('no new upcoming games')
else:
	# write to games table and generate game_id
	writeDB(new_games.loc[:, ['game_date', 'home', 'away']], 'games')
	# get new game_id values
	db_games = queryDB("select game_id, game_date||home||away as joiner from games")
	new_games = new_games.drop(columns=['game_id']).merge(db_games.loc[:, ['game_id', 'joiner']], how='left', on='joiner')

	# run predictions for the new games
	predictions_df = predictions(new_games[["game_id", "game_date", "home", "away"]])
	writeDB(predictions_df.loc[:, ['game_id', 'run_date', 'win_pred']], 'predictions')
	print('predictions written for new games')

# update pages
preds()
accuracy()

# push to S3
subprocess.call("s3_push.sh")