
"""
@author: Nicolas Miarka, 6908892
"""

import pandas as pd
import numpy as np


class Anonymize:
    
    def load_original_df(self,csvFile):
        # Load the original dataset
        self.df = pd.read_csv("./original_datasets/"+ csvFile)  
        return self.df
    
    # Load the anonymized dataset
    def load_anonymized_df(self,csvFile):
       self.anonymized_df = pd.read_csv('./anonymized_datasets/'+csvFile)      
       return self.anonymized_df


    def privMSE (self,original_data, anonymized_data):
        """
        Calculate the mean squared error between the observed and actual data
        parameter:
            two pandas dataframes representing the original and anonymized data
        returns:
            the mean squared error between the dataframes.
        """
        #sort the columns 
        sorted_original_data = original_data[original_data.columns.sort_values()]
        sorted_anonymized_data = anonymized_data[anonymized_data.columns.sort_values()]
        mse = 0
        # iterate through the columns
        for i in range(len(sorted_original_data.columns)):
            data_type = sorted_anonymized_data[sorted_anonymized_data.columns[i]].dtype 
            if data_type == "int64" or data_type == "float64":
                # calculate the mse of the columns
                column_difference = (sorted_anonymized_data[sorted_anonymized_data.columns[i]] - sorted_original_data[sorted_original_data.columns[i]]).pow(2)
                element = column_difference.sum()/len(column_difference)
            else:
                # anonymized dfs have ranges. we need to prep the range to use them later
                element = 0
                for j in range(len(sorted_anonymized_data.index)-1):
                    try: 
                        a = sorted_anonymized_data[sorted_anonymized_data.columns[i]][j].split(",")
                    except:
                        continue
                    start = float(a[0][1:])
                    stop = float(a[1][:len(a[1])-1])
                    # calculate the average error of a range of values and the true outcome.
                    test = np.mean((np.linspace(start,stop,1000) - sorted_original_data[sorted_original_data.columns[i]][j])**2)
                    element+=test
                element = element/len(sorted_anonymized_data[sorted_anonymized_data.columns[i]])
            mse += element
        return mse/len(sorted_original_data.columns)   

    

def test_anonymization():
    
    # Load the Anonymize class
    anonymize = Anonymize()
    heart_csv = ["v1_heart.csv","v2_heart.csv","v3_heart.csv","v4_heart.csv","v5_heart.csv",]
    original_df = anonymize.load_original_df("heart.csv")
    # drop the Unnamed:0 column from the original dataframe because we won't need it for mse calculation.
    del original_df[original_df.columns[0]]
    for csvFile in heart_csv:
        #read the anonymized csv
        anonymized_heart_df = anonymize.load_anonymized_df(csvFile)
        #calculate the mse
        mse = anonymize.privMSE(original_df,anonymized_heart_df)
        print(csvFile, "MSE: ", mse)

test_anonymization()

