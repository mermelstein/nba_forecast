import bs4, requests, time
import pandas as pd
from utils.char_replace import CharReplace

# pull recent game scores

def score_scraper(result_page):
    html = requests.get(result_page)
    Soup = bs4.BeautifulSoup(html.text, "html.parser")
    elements = Soup.select(".content > .clear")
    if elements == []:
        print('no data')
    else:
        records = []
        for element in elements:
            row = element.find_all('div')
            records.append([elem.get_text() for elem in row])

        #add date
        i = 0
        for r in records:
            day = elements[i].get('data-esd',None)
            r.insert(0,day)
            i = i + 1
        #delete first object in list
        records = records[1:]

        #add run date
        today = time.strftime("%Y%m%d")
        i = 0
        for r in records:
            r.insert(0,today)
            i = i + 1

        CharReplace(records)


    # Turn list into pandas DataFrame. Don't need to export to csv and reimport anymore
    df = pd.DataFrame.from_records(records, columns=['run_date','game_date','1','2','3','home','4','hscore','5','6','7','hq1','hq2','hq3','hq4','8','9','10','11','away','12','ascore','13','14','15','aq1','aq2','aq3','aq4','16','17'])
    # Select columns we'll be working with
    sub_df = df.loc[:,['run_date','game_date','home','hscore','hq1','hq2','hq3','hq4','away','ascore','aq1','aq2','aq3','aq4']]

    # Drop rows where Hscore is empty
    sub_df = sub_df[sub_df['hscore'] != '']
    sub_df = sub_df[sub_df['hscore'] != 'NA']
    sub_df = sub_df[sub_df['hscore'] != 'None']
    sub_df = sub_df.dropna(axis=0, how='any', subset=['hscore'])

    # Change data types and clean
    sub_df['run_date'] = sub_df['run_date'].astype(int)
    sub_df['game_date'] = pd.to_datetime(sub_df['game_date'], format='%Y%m%d%H%M%S', errors='ignore')
    sub_df['home'] = sub_df['home'].str.strip()
    sub_df['away'] = sub_df['away'].str.strip()
    sub_df['hscore'] = sub_df['hscore'].astype(int)
    sub_df['hq1'] = sub_df['hq1'].astype(int)
    sub_df['hq2'] = sub_df['hq2'].astype(int)
    sub_df['hq3'] = sub_df['hq3'].astype(int)
    sub_df['hq4'] = sub_df['hq4'].astype(int)
    sub_df['ascore'] = sub_df['ascore'].astype(int)
    sub_df['aq1'] = sub_df['aq1'].astype(int)
    sub_df['aq2'] = sub_df['aq2'].astype(int)
    sub_df['aq3'] = sub_df['aq3'].astype(int)
    sub_df['aq4'] = sub_df['aq4'].astype(int)

    return sub_df