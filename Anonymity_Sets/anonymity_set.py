import pandas as pd
import numpy as np

"""
@author Daniel Hahn, 7570542

This program implements the calculation of the anonymity set based on the formula 1/n 
without its duplicates.
"""


class AnonymitySet:
    #The class calculates the anonymity set based on a dataset.

    def __init__(self, csvFile):
        #Initializes the class with a csvFile.    
        self.df = pd.read_csv(csvFile)
        
    def calculate(self):
        lengthWithoutDuplicates = len(self.df.drop_duplicates().axes[0])    #Calculation of the length without the duplicates.
        return (1/lengthWithoutDuplicates)  #Returns the final value 1/n.


def test_databases():
    #This function tests all datasets and shows their values.
    testdatabase = AnonymitySet('heart.csv')
    print("The privacy level of heart.csv is ",testdatabase.calculate())
    testdatabase = AnonymitySet('v1_heart.csv')
    print("The privacy level of v1_heart.csv is ",testdatabase.calculate())
    testdatabase = AnonymitySet('v2_heart.csv')
    print("The privacy level of v2_heart.csv is ",testdatabase.calculate())
    testdatabase = AnonymitySet('v3_heart.csv')
    print("The privacy level of v3_heart.csv is ",testdatabase.calculate())
    testdatabase = AnonymitySet('v4_heart.csv')
    print("The privacy level of v4_heart.csv is ",testdatabase.calculate())
    testdatabase = AnonymitySet('v5_heart.csv')
    print("The privacy level of v5_heart.csv is ",testdatabase.calculate())
    testdatabase = AnonymitySet('sepsis.csv')
    print("The privacy level of sepsis.csv is ",testdatabase.calculate())
    testdatabase = AnonymitySet('v1_sepsis.csv')
    print("The privacy level of v1_sepsis.csv is ",testdatabase.calculate())
    testdatabase = AnonymitySet('v2_sepsis.csv')
    print("The privacy level of v2_sepsis.csv is ",testdatabase.calculate())
    testdatabase = AnonymitySet('v3_sepsis.csv')
    print("The privacy level of v3_sepsis.csv is ",testdatabase.calculate())
    testdatabase = AnonymitySet('v4_sepsis.csv')
    print("The privacy level of v4_sepsis.csv is ",testdatabase.calculate())

test_databases()