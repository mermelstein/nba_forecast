import pandas as pd

def accuracy_calc(outcomes):
    # create new dataframe with text and game values
    accuracy_df = pd.DataFrame([['Last 50 Games', 50, 0],['Last 100 Games', 100, 0], ['Last 200 Games', 200, 0]], columns=['description','game_count','accuracy'])

    for r in range(0, len(accuracy_df)):
        accuracy_df.iloc[r,2] = outcomes.loc[:accuracy_df.loc[r,"game_count"],"correct_prediction"].sum() / accuracy_df.loc[r,"game_count"]
        # format percentages
        accuracy_df.iloc[r,2] = str(round((accuracy_df.iloc[r,2]*100))) + str('%')

    return accuracy_df