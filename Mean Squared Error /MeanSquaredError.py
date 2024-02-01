# -*- coding: utf-8 -*-
"""
@author: Nicolas Miarka, 6908892
"""
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
import re
class Anonymize:
    
    def load_original_df(self,csvFile):
        # Load the original dataset
        self.df = pd.read_csv("./original_datasets/" + csvFile)  
        return self.df
    
    # Load the anonymized dataset
    def load_anonymized_df(self,csvFile):
       self.anonymized_df = pd.read_csv('./anonymized_datasets/' + csvFile)      
       return self.anonymized_df
    
    def euclidean_distance(self,original_row,anonymized_df): 
        if anonymized_df.empty:
            return 0
        distances = anonymized_df.apply(
        lambda row: euclidean(original_row, row), axis=1
    )
        try:
            closest_idx = distances.idxmin()
        except:
            return None
        return distances[closest_idx]
def compute_mean_from_interval(s):
# Use regex to find numbers in the string
    numbers = re.findall(r'(-?\d+(?:\.\d+)?)', s)
    if numbers:
        return sum([float(x) for x in numbers]) / len(numbers)
    return None  
testing_sets = {
    "heart.csv":[
        ("v1_heart.csv",["trestbps","thalach","ca","thal","age","chol","oldpeak","target"],"target",{"age_range":"age","chol_range":"chol","oldpeak_range":"oldpeak"}),
        ("v2_heart.csv",["trestbps","thalach","age","chol","oldpeak","target"],"target",{"age_range":"age","chol_range":"chol","oldpeak_range":"oldpeak"}),
        ("v3_heart.csv",["trestbps","thalach","ca","thal","age","chol","oldpeak","target"],"target",{"age_range":"age","chol_range":"chol","oldpeak_range":"oldpeak"}),
        ("v4_heart.csv",["trestbps","thalach","ca","thal","age","chol","oldpeak","target"],"target",{"age_range":"age","chol_range":"chol","oldpeak_range":"oldpeak"}),
        ("v5_heart.csv",["trestbps","thalach","ca","thal","age","chol","oldpeak","target"],"target",{"age_range":"age","chol_range":"chol","oldpeak_range":"oldpeak"}),
    ],
    "kidney.csv":[
        ("v1_kidney.csv",['id','age', 'bp', 'bgr', 'bu', 'sc', 'hemo', 'wc', 'rc'],'id'),
        ("v2_kidney.csv",['id','age', 'bp', 'bgr', 'bu', 'sc', 'hemo', 'wc', 'rc'],'id')
    ],
    "sepsis.csv":[
        ("v1_sepsis.csv",["Age","O2Sat","Temp","Resp","WBC","Glucose",'SepsisLabel'],'SepsisLabel',{}),
        ("v2_sepsis.csv",["Age","HR", "SBP", "MAP", "DBP",'SepsisLabel'],'SepsisLabel',{}),
        ("v3_sepsis.csv",["Age","Gender","HR","O2Sat","Temp","SBP","MAP","DBP","Resp","Hgb","WBC","Glucose",'SepsisLabel'],'SepsisLabel',{}),
        ("v4_sepsis.csv",["Age","Gender","HR","O2Sat","Temp","SBP","MAP","DBP","Resp","Hgb","WBC","Glucose",'SepsisLabel'],'SepsisLabel',{})
    ]
}
original_files = ["kidney.csv","heart.csv","sepsis"]


def test_anonymization():

    anonymize = Anonymize()
    original_kidney_df = anonymize.load_original_df("kidney.csv")
    for anonymized_file, quasi_identifieres,sensitive_info in testing_sets["kidney.csv"]:
        mse = 0
        anonymized_kidney_df = anonymize.load_anonymized_df(anonymized_file)
        anonymized_kidney_df = anonymized_kidney_df[quasi_identifieres]
        original_rows = original_kidney_df[quasi_identifieres]
        for column in anonymized_kidney_df.columns:
            if anonymized_kidney_df[column].dtype == object:
                anonymized_kidney_df[column] = anonymized_kidney_df[column].apply(compute_mean_from_interval)
        
        for index, row in original_rows.iterrows():
            filtered_df = anonymized_kidney_df[anonymized_kidney_df["id"] == row["id"]]
            mse += anonymize.euclidean_distance(row,filtered_df)**2
        print(anonymized_file, "MSE: ", mse/len(anonymized_kidney_df))
    


    original_heart_df = anonymize.load_original_df("heart.csv")
    del original_heart_df[original_heart_df.columns[0]]
    for anonymized_file,quasi_identifieres,sensitive_info,renames in testing_sets["heart.csv"]:
        mse = 0
        anonymized_heart_df = anonymize.load_anonymized_df(anonymized_file).rename(columns=renames)[quasi_identifieres]
        anonymized_heart_df = anonymized_heart_df.dropna(subset=quasi_identifieres)
        original_heart_rows = original_heart_df[quasi_identifieres]
        if anonymized_file == "v5_heart.csv":
            for index, row in original_heart_rows.iterrows():
                mse+= euclidean(original_heart_rows.loc[index],anonymized_heart_df.loc[index])**2
                
            print(mse/len(anonymized_heart_df))
        else:
            for column in anonymized_heart_df.columns:
                if anonymized_heart_df[column].dtype == object:
                    anonymized_heart_df[column] = anonymized_heart_df[column].apply(compute_mean_from_interval)
            for index, row in original_heart_rows.iterrows():
                filtered_df = anonymized_heart_df[anonymized_heart_df["target"] == row["target"]]
                mse += anonymize.euclidean_distance(row,filtered_df)**2
            print(anonymized_file, "MSE: ", mse/len(original_heart_df))
    


    original_sepsis_df = anonymize.load_original_df("sepsis.csv")
    for anonymized_file,quasi_identifieres,sensitive_info,renames in testing_sets["sepsis.csv"]:
        mse = 0
        original_sepsis_df.dropna(subset=quasi_identifieres)
        anonymized_sepsis_df = anonymize.load_anonymized_df(anonymized_file).rename(columns=renames)[quasi_identifieres]
        anonymized_sepsis_df = anonymized_sepsis_df.dropna(subset=quasi_identifieres)
        original_sepsis_rows = original_sepsis_df[quasi_identifieres]
        original_sepsis_rows = original_sepsis_rows.dropna()
        if anonymized_file == "v4_sepsis.csv":
            for index, row in original_sepsis_rows.iterrows():
                mse+= euclidean(original_sepsis_rows.loc[index],anonymized_sepsis_df.loc[index])**2
                
            print(mse/len(anonymized_sepsis_df))
        else:
            for column in anonymized_sepsis_df.columns:
                if anonymized_sepsis_df[column].dtype == object:
                    anonymized_sepsis_df = anonymized_sepsis_df[anonymized_sepsis_df[column].apply(lambda x: isinstance(x, str))]
                    anonymized_sepsis_df[column] = anonymized_sepsis_df[column].apply(compute_mean_from_interval)
            for index, row in original_sepsis_rows.iterrows():
                filtered_df = anonymized_sepsis_df[anonymized_sepsis_df["SepsisLabel"] == row["SepsisLabel"]]
                mse += anonymize.euclidean_distance(row,filtered_df)**2
            print(anonymized_file, "MSE: ", mse/len(original_heart_df))
test_anonymization()



