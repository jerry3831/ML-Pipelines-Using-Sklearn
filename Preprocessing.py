import pandas as pd 
import numpy as np
from sklearn.preprocessing import StandardScaler

class Preprocessor:
    # ! target column included as default for testing purposes
    def __init__(self, target_col='mood_score'):
        self.scaler = StandardScaler()
        self.target_col = target_col

    def processor(self, df):
        for col in df.columns:
            pass
    
    def handle_outliers(self, df, method='iqr', strategy='remove'):
        if method == 'iqr':
            outliers = None
            for col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                low_bound = Q1 - 1.5 * IQR
                up_bound = Q3 + 1.5 * IQR
                outliers = df[(df[col] < low_bound) | df[col] > up_bound]
            if strategy == 'remove':
                df = df.drop(outliers.index)
            elif strategy == 'replace':
                df.loc[outliers.index, col] = df[col].median()
            else:
                print('invalid strategy, try another one')

        if method == "zscore":
            outliers = None
            for col in df.columns:
                mean = df[col].mean()
                std = df[col].std()
                zscores = np.abs((df[col] - mean) / std)
                outliers = df[zscores > 3]
            if strategy == 'remove':
                df = df.drop(outliers.index)
            elif strategy == 'replace':
                df.loc[outliers.index, col] = df[col].median()
            else:
                print('invalid strategy, try another one')
            

    def fit(self, dataframe):
        dataframe = dataframe.copy()
        processed_df = self.handle_outliers(dataframe, method='iqr', strategy='remove')
        return processed_df


process = Preprocessor()
data = pd.read_csv(r'digital_habits_vs_mental_health.csv', encoding='windows-1256')

sample = process.fit(data)
print(sample.head())

#  TODO: check the loops and inner iterations and figure out why the outlier handling method outputs 
#  TODO: a non-type