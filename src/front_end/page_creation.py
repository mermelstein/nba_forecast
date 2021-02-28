import os
from pytz import timezone
from datetime import date
import jinja2

def create_index(predictions):
	# remove whitespace around team names
	predictions["home"] = predictions["home"].str.strip()
	predictions["away"] = predictions["away"].str.strip()

	predictions["upcoming"] = 0
	# set game_date to EST
	for x in range(0, len(predictions)):
		predictions.loc[x,"game_date"] = timezone('UTC').localize(predictions.loc[x,"game_date"])
		predictions.loc[x,"game_date"] = predictions.loc[x,"game_date"].astimezone(timezone('US/Eastern'))
		if predictions.loc[x,"game_date"] >= date.today():
			predictions.loc[x, "upcoming"] = 1
		predictions.loc[x,"game_date"] = predictions.loc[x,"game_date"].strftime("%Y-%m-%d %H:%M")
		# format win_prob percentages
		predictions.loc[x, "win_pred"] = str(round((predictions.loc[x, "win_pred"] * 100), 2)) + str('%')

	# after converting from UTC limit to games happening today
	predictions = predictions.loc[(predictions['upcoming'] == 1)]

	# convert to an iterable list
	predictions_list = predictions.to_dict("records")
	templateLoader = jinja2.FileSystemLoader(searchpath="./")
	templateEnv = jinja2.Environment(loader=templateLoader)
	# load template
	TEMPLATE_FILE = "front_end/templates/index_template.html"
	template = templateEnv.get_template(TEMPLATE_FILE)
	# add in the variables
	outputPage = template.render(
		predictions=predictions_list
	)

	# save the new front page
	index = open(os.path.join(os.getcwd(), "front_end/templates/index.html"), "w")
	index.write(outputPage)
	index.close()

def create_accuracy(stats):
	stats_list = stats.to_dict("records")
	templateLoader = jinja2.FileSystemLoader(searchpath="./")
	templateEnv = jinja2.Environment(loader=templateLoader)
	# load template
	TEMPLATE_FILE = "front_end/templates/accuracy_template.html"
	template = templateEnv.get_template(TEMPLATE_FILE)
	# add in the variables
	outputPage = template.render(
		stats=stats_list
	)

	# save the new front page
	index = open(os.path.join(os.getcwd(), "front_end/templates/accuracy.html"), "w")
	index.write(outputPage)
	index.close()