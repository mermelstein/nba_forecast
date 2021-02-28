import datetime
from utils.db_connection import queryDB
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

def predictions(target_df):

    # Read game data
    game_data = queryDB("select distinct * from scores "
                     "order by game_date desc limit 1000")

    # add target variable
    game_data['wins'] = game_data.apply(lambda row: ( 1
                                                if row['hscore'] - row['ascore'] > 0
                                                else 0),
                                       axis=1)

    train = game_data.iloc[:,:]

    # Create modeling dataset
    home_train = train[['home','hscore','ascore']].groupby(['home'], as_index=False).sum()
    away_train = train[['away','ascore','hscore']].groupby(['away'], as_index=False).sum()

    # calculate averages
    h_played = train[['home','hq1']].groupby(['home'], as_index=False).count()
    a_played = train[['away','hq1']].groupby(['away'], as_index=False).count()

    for r in range(0, len(home_train)):
        home_train.iloc[r,1:] = home_train.iloc[r,1:]/h_played.iloc[r,1]
    for r in range(0, len(away_train)):
        away_train.iloc[r,1:] = away_train.iloc[r,1:]/a_played.iloc[r,1]

    hwinning = train[['home','wins']].groupby(['home'], as_index=False).sum()
    awinning = train[['away','wins']].groupby(['away'], as_index=False).sum()

    h_rate = hwinning.merge(h_played, how='left', on='home')
    a_rate = awinning.merge(a_played, how='left', on='away')
    h_rate['win_rate'] = h_rate.apply(lambda row: (row['wins']/row['hq1']), axis=1)
    a_rate['win_rate'] = a_rate.apply(lambda row: (row['wins']/row['hq1']), axis=1)
    h_rate = h_rate.drop(['wins','hq1'],axis=1)
    a_rate = a_rate.drop(['wins','hq1'],axis=1)

    # Finalize training set
    train_mv = train[['home','away','wins']]
    train_mv = train_mv.merge(home_train, how='left', on='home')
    train_mv = train_mv.merge(away_train, how='left', on='away')
    train_mv = train_mv.merge(h_rate, how='left', on='home')
    train_mv = train_mv.merge(a_rate, how='left', on='away')


    train_cols = train_mv.columns[3:10]

    # Create prediction input set
    today_games_mv = target_df.merge(home_train, how='left', on='home')
    today_games_mv = today_games_mv.merge(away_train, how='left', on='away')
    today_games_mv = today_games_mv.merge(h_rate, how='left', on='home')
    today_games_mv = today_games_mv.merge(a_rate, how='left', on='away')

    Gaussmodel = GaussianNB()
    LRmodel = LogisticRegression()

    Gaussmodel.fit( train_mv[train_cols] , train_mv['wins'])
    train_mv['Gaussian'] = Gaussmodel.predict( train_mv[train_cols] )
    today_games_mv['Gaussian'] = Gaussmodel.predict( today_games_mv[train_cols] )
    # update training columns
    train_cols = train_mv.columns[3:10]

    # Run logit model
    LRmodel.fit( train_mv[train_cols] , train_mv['wins'] )
    today_games_mv['win_pred'] = LRmodel.predict_proba( today_games_mv[train_cols] )[:,1]

    today_games_mv['run_date'] = datetime.datetime.now(datetime.timezone.utc)

    predictions_df = today_games_mv[['run_date','game_id','game_date','home','away','win_pred']]

    return predictions_df