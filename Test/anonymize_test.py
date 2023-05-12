# -*- coding: utf-8 -*-
"""
Created on Wed May 10 09:06:18 2023

@author: pronaya
"""

import pandas as pd
import numpy as np


class Anonymize:
    
    def load_original_df(self):
        # Load the original dataset
        self.df = pd.read_csv('heart.csv')  
        return self.df
    
    def find_k(self, df, quasi_identifiers_n):
        # Group the data based on quasi-identifiers
        groups = df.groupby(quasi_identifiers_n)

        # Calculate the group sizes
        group_sizes = groups.size()
        print(group_sizes)
        
        # Determine the K-anonymity level
        k_anonymity_level = group_sizes.min()

        return k_anonymity_level     
        
    # Load the anonymized dataset
    def load_anonymized_df(self):
       self.anonymized_df = pd.read_csv('anonymized_heart.csv')      
       return self.anonymized_df


    

def test_anonymization():
    
    # Load the Anonymize class
    anonymize = Anonymize()
 
    # Define quasi identifiers
    quasi_identifiers_ori = ['age', 'sex']
    # Load original dataset
    original_df = anonymize.load_original_df()  
    # Call the test function
    k_anonymity_level_original = anonymize.find_k(original_df, quasi_identifiers_ori)
    # Show results
    print(f"K-anonymity level for original dataset: {k_anonymity_level_original}")
    
    
    # Define quasi identifiers
    quasi_identifiers_ano = ['age_range', 'sex']
    # Load the anonymized dataset
    anonymized_df = anonymize.load_anonymized_df()  
    # Call the test function
    k_anonymity_level_anonymous = anonymize.find_k(anonymized_df, quasi_identifiers_ano)
    # Show results
    print(f"K-anonymity level for anonymous dataset: {k_anonymity_level_anonymous}")
    
    return original_df, anonymized_df

 

original_df, anonymized_df = test_anonymization()



