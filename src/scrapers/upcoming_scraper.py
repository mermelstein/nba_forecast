import bs4, requests, time
import pandas as pd
from utils.char_replace import CharReplace


# pull upcoming games

def upcoming_scraper(game_page):
    html = requests.get(game_page)
    Soup = bs4.BeautifulSoup(html.text, "html.parser")
    elements = Soup.select(".content > .clear")
    if elements == []:
        print('no data')
    else:
        #today = time.strftime("%m/%d/%Y")
        today_records = []
        for element in elements:
            row = element.find_all('div')
            today_records.append([elem.get_text() for elem in row])

        #you now have a list of lists. Delete any sublist that is empty
        today_records = [x for x in today_records if x]

        #add date
        i = 0
        for r in today_records:
            day = elements[i].get('data-esd',None)
            r.insert(0,day)
            i = i + 1

        #add run date
        today = time.strftime("%Y%m%d")
        i = 0
        for r in today_records:
            r.insert(0,today)
            i = i + 1

        CharReplace(today_records)



    # Turn list into pandas DataFrame. Don't need to export to csv and reimport anymore
    today_df = pd.DataFrame.from_records(today_records, columns=['run_date','game_date','1','2','3','home','4','hscore','5','6','7','hq1','hq2','hq3','hq4','8','9','10','11','away','12','ascore','13','14','15','aq1','aq2','aq3','aq4','16','17'])

    # select rows where hscore is empty as today's games to predict
    today_games = today_df[today_df['hscore'] == '']
    # also remove postponed games
    postponed = today_games['3'].str.contains('Postp.')
    today_games = today_games[-postponed]

    # drop all empty columns
    today_games = today_games[["run_date","game_date","home","away"]]

    # change data types for dates
    today_games['run_date'] = today_games['run_date'].astype(int)
    today_games['game_date'] = pd.to_datetime(today_games['game_date'], format='%Y%m%d%H%M%S', errors='ignore')
    today_games['home'] = today_games['home'].str.strip()
    today_games['away'] = today_games['away'].str.strip()

    return today_games