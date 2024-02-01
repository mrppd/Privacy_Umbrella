# -*- coding: utf-8 -*-
"""
Created on Wed June 02 16:31:18 2023

@author: Jawwad Khan, 7417247, Seminar Datenmanagement
"""

import pandas as pd
import numpy as np

class Anonymize:

    def load_original_df(self):
        # Load the original dataset
        self.df = pd.read_csv("C:\\Users\\jawwa\\PycharmProjects\\Privacy_Umbrella\\original_datasets\\heart.csv")
        return self.df

    def privSRD(self,dataset, aux, sT, eT):
        """
        This function implements the formula presented in the Survey paper: privSRD ≡ p(Sim(s, s') ≥ τs) ≥ τe
        The function goes through every record in the dataset and compares each value of the record s' with the target
        record s with the Sim function. Sim will output a probability, which is then compared with the τs and τe.
        Args:
            dataset: Which contains the records we want to check the similarity with
            aux: the auxiliary_information of the adversary
            sT: similarity threshold, a % value which sets the minimum requirements of two values being similar
            eT: error Threshold, a % value which set the maximum allowable error of two records.

        Returns:
            The amount of similar records
        """
        amount_sim = 0
        for record in dataset: # record = s'
            attributes = set(record.keys()).intersection(set(aux.keys())) #Only compare those values which are present
            sim = sum(self.sim(record[i], aux[i]) for i in attributes)
            sim_per = sim/len(attributes) # %-value describing the similarity between target record and dataset record
            print(len(attributes))
            error = 1 - sim_per # 1 - similarity is the error or dissimilarity between target record and dataset record
            if sim >= sT:
                if sim == 1.0: # if the %-value describing the similarity is 1.0, we have a perfect match
                    amount_sim += 1
                elif error <= eT:
                    amount_sim += 1
                else:
                    amount_sim += 0
            else:
                amount_sim += 0
        return amount_sim

    """"
    def Sim(self, attribute_record, attribute_aux):
        if attribute_record == attribute_aux:
            return 1
        else:
            return 0
    """

    def sim(self, record, aux_record):
        """
        This function calculates a numerical value, which represents the similarity between a certain value of the target
        record and dataset record.
        Args:
            record: dataset record
            aux_record: auxiliary_information of the adversary

        Returns:
            float showing how many values are similar.
        """
        try:
            diff_values = (min(record, aux_record)/max(record, aux_record)) # for columns which have values != 0,1,2,3 like chol
            return diff_values
        except ZeroDivisionError:
            if record == aux_record: # for columns which have values == 0,1,2,3
                return 1
            else:
                return 0


    # Load the anonymized dataset
    def load_anonymized_df(self):
        self.anonymized_df = pd.read_csv("C:\\Users\\jawwa\\PycharmProjects\\Privacy_Umbrella\\anonymized_datasets\\v5_heart.csv")
        return self.anonymized_df


def test_anonymization():
    # Load the Anonymize class
    anonymize = Anonymize()

    # Load original dataset
    original_df = anonymize.load_original_df()  #

    # The orignal def contains a column called Unnamed: 0, which is the row number for the record.
    dataset = original_df.to_dict("records")
    for r in dataset:
        r.pop("Unnamed: 0")

    # Load the anonymized dataset
    anonymized_df = anonymize.load_anonymized_df()

    anonymized_dataset = anonymized_df.to_dict("records")

    # sampled from dataset d, can be modified
    auxiliary_information  = [
        {'age': 52, 'sex': 1, 'cp': 0, 'trestbps': 125, 'chol': 212, 'fbs': 0, 'restecg': 1, 'thalach': 168, 'exang': 0,'oldpeak': 1.0, 'slope': 2, 'ca': 2, 'thal': 3, 'target': 0},
        {'age': 53, 'sex': 1, 'cp': 0, 'trestbps': 140, 'chol': 203, 'fbs': 1, 'restecg': 0, 'thalach': 155, 'exang': 1,'oldpeak': 3.1, 'slope': 0, 'ca': 0, 'thal': 3, 'target': 0},
        {'age': 70, 'sex': 1, 'cp': 0, 'trestbps': 145, 'chol': 174, 'fbs': 0, 'restecg': 1, 'thalach': 125, 'exang': 1,'oldpeak': 2.6, 'slope': 0, 'ca': 0, 'thal': 3, 'target': 0}
    ]

    # for testing
    test_aux = [
        {'age': 52, 'sex': 1, 'cp': 0, 'trestbps': 125, 'chol': 212, 'fbs': 0, 'restecg': 1, 'thalach': 168, 'exang': 0,'oldpeak': 1.0, 'slope': 2, 'ca': 2, 'thal': 3, 'target': 0}
    ]

    # for testing
    test_data = [
        {'age': 52, 'sex': 1, 'cp': 0, 'trestbps': 125, 'chol': 212, 'fbs': 0, 'restecg': 1, 'thalach': 168, 'exang': 0, 'oldpeak': 1.0, 'slope': 2, 'ca': 2, 'thal': 3, 'target': 0},
        {'age': 53, 'sex': 1, 'cp': 0, 'trestbps': 140, 'chol': 203, 'fbs': 1, 'restecg': 0, 'thalach': 155, 'exang': 1, 'oldpeak': 3.1, 'slope': 0, 'ca': 0, 'thal': 3, 'target': 0},
        {'age': 70, 'sex': 1, 'cp': 0, 'trestbps': 145, 'chol': 174, 'fbs': 0, 'restecg': 1, 'thalach': 125, 'exang': 1, 'oldpeak': 2.6, 'slope': 0, 'ca': 0, 'thal': 3, 'target': 0},
        {'age': 61, 'sex': 1, 'cp': 0, 'trestbps': 148, 'chol': 203, 'fbs': 0, 'restecg': 1, 'thalach': 161, 'exang': 0, 'oldpeak': 0.0, 'slope': 2, 'ca': 1, 'thal': 3, 'target': 0},
        {'age': 62, 'sex': 0, 'cp': 0, 'trestbps': 138, 'chol': 294, 'fbs': 1, 'restecg': 1, 'thalach': 106, 'exang': 0, 'oldpeak': 1.9, 'slope': 1, 'ca': 3, 'thal': 2, 'target': 0},
        {'age': 58, 'sex': 0, 'cp': 0, 'trestbps': 100, 'chol': 248, 'fbs': 0, 'restecg': 0, 'thalach': 122, 'exang': 0, 'oldpeak': 1.0, 'slope': 1, 'ca': 0, 'thal': 2, 'target': 1},
        {'age': 58, 'sex': 1, 'cp': 0, 'trestbps': 114, 'chol': 318, 'fbs': 0, 'restecg': 2, 'thalach': 140, 'exang': 0, 'oldpeak': 4.4, 'slope': 0, 'ca': 3, 'thal': 1, 'target': 0},
        {'age': 55, 'sex': 1, 'cp': 0, 'trestbps': 160, 'chol': 289, 'fbs': 0, 'restecg': 0, 'thalach': 145, 'exang': 1, 'oldpeak': 0.8, 'slope': 1, 'ca': 1, 'thal': 3, 'target': 0},
        {'age': 46, 'sex': 1, 'cp': 0, 'trestbps': 120, 'chol': 249, 'fbs': 0, 'restecg': 0, 'thalach': 144, 'exang': 0, 'oldpeak': 0.8, 'slope': 2, 'ca': 0, 'thal': 3, 'target': 0},
        {'age': 54, 'sex': 1, 'cp': 0, 'trestbps': 122, 'chol': 286, 'fbs': 0, 'restecg': 0, 'thalach': 116, 'exang': 1, 'oldpeak': 3.2, 'slope': 1, 'ca': 2, 'thal': 2, 'target': 0},
        {'age': 71, 'sex': 0, 'cp': 0, 'trestbps': 112, 'chol': 149, 'fbs': 0, 'restecg': 1, 'thalach': 125, 'exang': 0, 'oldpeak': 1.6, 'slope': 1, 'ca': 0, 'thal': 2, 'target': 1},
        {'age': 43, 'sex': 0, 'cp': 0, 'trestbps': 132, 'chol': 341, 'fbs': 1, 'restecg': 0, 'thalach': 136, 'exang': 1, 'oldpeak': 3.0, 'slope': 1, 'ca': 0, 'thal': 3, 'target': 0},
        {'age': 34, 'sex': 0, 'cp': 1, 'trestbps': 118, 'chol': 210, 'fbs': 0, 'restecg': 1, 'thalach': 192, 'exang': 0, 'oldpeak': 0.7, 'slope': 2, 'ca': 0, 'thal': 2, 'target': 1},
            ]


    # for every auxiliary information the adversary has, we output how many similar records we found and a percentage value
    # with the original dataset
    sT = [0.1, 0.3, 0.5, 0.7, 0.9]
    eT = [0.1, 0.3, 0.5, 0.7, 0.9]
    for i in sT:
        for j in eT:
            print("--------------------")
            print(i, j)
            results = []
            for aux in anonymized_dataset:
                result = anonymize.privSRD(dataset, aux, i, j)
                #print("---------------------------------------------------------------------------------------------------------")
                #print("Amount of similar records", result)
                #print("With auxiliary_information = ", aux)
                #print("Adversary’s Success Rate: ", (result/len(dataset))*100, "%")
                results.append((result/len(dataset)))
                #print("---------------------------------------------------------------------------------------------------------")
            print(sum(results) / len(results))

            #print("<------------------------------------------------anonymized dataset------------------------------------------------>")


            # for every auxiliary information the adversary has, we output how many similar records we found and a percentage value
            # with the anonymized dataset
            anonymized_results = []
            for aux in dataset:
                a_result = anonymize.privSRD(anonymized_dataset, aux, i, j)
                #print("---------------------------------------------------------------------------------------------------------")
                #print("Amount of similar records", result)
                #print("With auxiliary_information = ", aux)
                #print("Adversary’s Success Rate: ", (a_result/len(dataset))*100, "%")
                anonymized_results.append((a_result/len(dataset)))
                #print("---------------------------------------------------------------------------------------------------------")
            print(sum(anonymized_results) / len(anonymized_results))


    return original_df, anonymized_df


original_df, anonymized_df = test_anonymization()