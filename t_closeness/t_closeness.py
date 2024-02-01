"""
@author Emmelina Gardewischke, 7585665

"""

import pandas as pd
import numpy as np


class Anonymize:
    
    # Load the original dataset
    def load_original_df(self):
        self.df = pd.read_csv('original_datasets/heart.csv')  
        return self.df

        
    # Load the anonymized dataset
    def load_anonymized_df(self, version):
       self.anonymized_df = pd.read_csv(f'anonymized_datasets/v{version}_heart.csv')
       return self.anonymized_df


    def emd_cat(self, P, Q):
        """
        Calculate the Earth Mover's Distance (EMD) between two categorical distributions.
        
        Args:
            P (np.array): The first distribution.
            Q (np.array): The second distribution.
            
        Returns:
            float: The EMD between P and Q.
        """
        return 0.5 * np.sum(np.abs(P - Q))


    def calculate_emd(self, df, quasi_identifiers_n):
        # Group the data based on quasi-identifiers
        groups = df.groupby(quasi_identifiers_n)

        # Calculate the distribution of 'target' in the whole dataset
        Q_dist = np.array([np.sum(df['target'] == 0) / len(df), np.sum(df['target'] == 1) / len(df)])

        # Initialize a list to store the EMD for each equivalence class
        emd_list = []

        # Iterate over each group (equivalence class)
        for name, group in groups:
            # Calculate the distribution of 'target' in the group
            P_dist = np.array([np.sum(group['target'] == 0) / len(group), np.sum(group['target'] == 1) / len(group)])
            # Calculate the EMD between the distribution in the group and the distribution in the whole dataset
            emd = self.emd_cat(Q_dist, P_dist)
            # Append the EMD to the list
            emd_list.append(emd)

            #print(f"EMD for equivalence class {name}: {emd}")

        # Calculate the average EMD over all equivalence classes
        avg_emd = np.mean(emd_list)

        return avg_emd, len(emd_list)
    

def test_anonymization():
    
    # Load the Anonymize class
    anonymize = Anonymize()
 
    # Load original dataset
    original_df = anonymize.load_original_df()
    
    # Define quasi identifiers for each version
    quasi_identifiers_ori_v1 = ['age', 'sex', 'restecg', 'fbs']
    quasi_identifiers_ano_v1 = ['age_range', 'sex', 'restecg', 'fbs']
    
    quasi_identifiers_ori_v2 = ['age', 'sex']
    quasi_identifiers_ano_v2 = ['age', 'sex']
    
    quasi_identifiers_ori_v3 = ['age', 'sex']
    quasi_identifiers_ano_v3 = ['age_range', 'sex']
    
    quasi_identifiers_ori_v4 = ['age', 'sex', 'restecg', 'fbs']
    quasi_identifiers_ano_v4 = ['age_range', 'sex', 'restecg', 'fbs']
    
    for version in range(1, 5):
        # Load the anonymized dataset
        anonymized_df = anonymize.load_anonymized_df(version)
        
        # Select the appropriate quasi-identifiers for this version
        if version == 1:
            quasi_identifiers_ano = quasi_identifiers_ano_v1
        elif version == 2:
            quasi_identifiers_ano = quasi_identifiers_ano_v2
        elif version == 3:
            quasi_identifiers_ano = quasi_identifiers_ano_v3
        elif version == 4:
            quasi_identifiers_ano = quasi_identifiers_ano_v4
        
        # Call the test function for the anonymized dataset
        avg_emd, num_eq_classes = anonymize.calculate_emd(anonymized_df, quasi_identifiers_ano)
        
        print(f"Average EMD for anonymous dataset v{version}: {avg_emd}")
        print("\n")
        # print(f"Number of equivalence classes for anonymous dataset v{version}: {num_eq_classes}")
    
    return original_df, anonymized_df

original_df, anonymized_df = test_anonymization()