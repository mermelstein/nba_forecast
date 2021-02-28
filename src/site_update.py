from utils.db_connection import queryDB
from utils.accuracy import accuracy_calc
from front_end.page_creation import create_index, create_accuracy

def preds():
	# pull all the most recent predictions for upcoming games
	predictions = queryDB("""
	with predict as (
		select 
			p.game_id,
			p.run_date::date,
			g.game_date,
			g.home,
			g.away,
			p.win_pred ,
			row_number() over (partition by g.game_id order by p.run_date desc) as num
		from predictions p
		join games g on g.game_id = p.game_id 
		where g.game_date::date >= current_date
		order by game_id, run_date desc
	)
	select *
	from predict
	where num = 1
	""")

	if predictions.empty == True:
		print('no updates for prediction page')
	else:
		create_index(predictions)

def accuracy():
	outcomes = queryDB("""
	with outcomes as (
		select 
			p.run_date as predict_date,
			g.game_date,
			g.game_id,
			g.home,
			s.hscore,
			s.ascore,
			g.away,
			p.win_pred as win_pred,
			case when s.hscore > s.ascore then 1 else 0 end as game_result,
			case when p.win_pred >= 0.5 then 1 else 0 end as predicted_winner,
			row_number() over (partition by g.game_id order by p.run_date desc) as num
		from games g
		join predictions p on g.game_id = p.game_id 
		join scores s on s.game_id = g.game_id 
	)
	select distinct 
		*,
		case when game_result = predicted_winner then 1 else 0 end as correct_prediction
	from outcomes
	where num = 1
	order by game_id desc, predict_date desc, game_date desc
	limit 1000
	""")

	stats = accuracy_calc(outcomes)
	create_accuracy(stats)