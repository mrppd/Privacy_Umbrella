"""
@author Kristian Lee, 6547510

"""

import pandas as pd
from typing import List


class Anonymize:
    """
    Anonymization class for assessing (k, e)-anonymity in a dataset.
    """

    def load_dataset(self, file_name: str) -> pd.DataFrame:
        """
        Load a dataset from a CSV file.

        Args:
            file_name (str): The name of the CSV file.

        Returns:
            pd.DataFrame: The loaded dataset.
        """
        df = pd.read_csv(file_name)
        return df

    def find_k(self, df: pd.DataFrame, quasi_identifiers: List[str]) -> int:
        """
        Find the K-anonymity level of the dataset based on the quasi-identifiers.

        Args:
            df (pd.DataFrame): The dataset.
            quasi_identifiers (List[str]): List of column names representing the quasi-identifiers.

        Returns:
            int: The minimum group size, which represents the K-anonymity level.
        """
        groups = df.groupby(quasi_identifiers)
        group_sizes = groups.size()
        k_anonymity_level = group_sizes.min()
        return k_anonymity_level

    def find_e(self, df: pd.DataFrame, quasi_identifiers: List[str], sensitive_attr: str, e: int) -> bool:
        """
        Check if the dataset satisfies the desired E-uniqueness level based on the proportions of group sizes.

        Args:
            df (pd.DataFrame): The dataset.
            quasi_identifiers (List[str]): List of column names representing the quasi-identifiers.
            sensitive_attr (str): The column name representing the sensitive attribute.
            e (int): The maximum privacy parameter for E-uniqueness.

        Returns:
            bool: True if the dataset satisfies the desired E-uniqueness level, False otherwise.
        """
        groups_with_sensitive = df.groupby(quasi_identifiers + [sensitive_attr])
        group_sizes_with_sensitive = groups_with_sensitive.size()

        groups_without_sensitive = df.groupby(quasi_identifiers)
        group_sizes_without_sensitive = groups_without_sensitive.size()

        matching_group_sizes_without_sensitive = group_sizes_without_sensitive.loc[
            group_sizes_with_sensitive.index.to_list()]

        proportions = group_sizes_with_sensitive / matching_group_sizes_without_sensitive

        e_uniqueness_values = (proportions <= 1 / e)

        return all(e_uniqueness_values)

    def check_k(self, df: pd.DataFrame, quasi_identifiers: List[str], k: int) -> bool:
        """
        Check if the dataset satisfies the desired K-anonymity level based on the quasi-identifiers.

        Args:
            df (pd.DataFrame): The dataset.
            quasi_identifiers (List[str]): List of column names representing the quasi-identifiers.
            k (int): The desired minimum group size representing the K-anonymity level.

        Returns:
            bool: True if the dataset satisfies the desired K-anonymity level, False otherwise.
        """
        groups = df.groupby(quasi_identifiers)
        group_sizes = groups.size()
        k_anonymity_check = (group_sizes >= k).all()
        return k_anonymity_check


def test_anonymization(config: dict):
    """
    Perform the anonymization test for a specific configuration.

    Args:
        config (dict): Dictionary containing the configuration parameters.
    """
    anonymize = Anonymize()

    df = anonymize.load_dataset(config['file_name'])
    k_anonymity_check = anonymize.check_k(df, config['quasi_identifiers'], config['k'])

    e_value = config['e']
    while e_value >= 0:
        e_uniqueness = anonymize.find_e(df, config['quasi_identifiers'], config['sensitive_attr'], e_value)
        if k_anonymity_check and e_uniqueness:
            print(f"Dataset {config['file_name']} satisfies desired (k, e)-anonymity for k={config['k']} and e={e_value}")
            break
        e_value -= 0.01
    else:
        print(f"Dataset {config['file_name']} does not satisfy desired (k, e)-anonymity for k={config['k']} and any e value below or equal to 10")


configs = [
    {
        'file_name': 'v1_heart.csv',
        'quasi_identifiers': ['age_range', 'sex', 'cp', 'trestbps', 'chol_range', 'fbs', 'restecg', 'thalach', 'exang',
                              'oldpeak_range', 'slope', 'ca', 'thal'],
        'sensitive_attr': 'target',
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v2_heart.csv',
        'quasi_identifiers': ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang',
                              'oldpeak', 'slope', 'ca', 'thal'],
        'sensitive_attr': 'target',
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v3_heart.csv',
        'quasi_identifiers': ['sex', 'cp', 'trestbps', 'fbs', 'restecg', 'thalach', 'exang', 'slope','ca', 'thal',
                              'age_range', 'chol_range', 'oldpeak_range'],
        'sensitive_attr': 'target',
        'e': 10,
        'k': 5,
    },
    {
        'file_name': 'v4_heart.csv',
        'quasi_identifiers': ['sex', 'cp', 'trestbps', 'fbs', 'restecg', 'thalach', 'exang', 'slope', 'ca', 'thal',
                              'age_range', 'chol_range', 'oldpeak_range'],
        'sensitive_attr': 'target',
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v5_heart.csv',
        'quasi_identifiers': ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang',
                              'oldpeak', 'slope', 'ca', 'thal'],
        'sensitive_attr': 'target',
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v1_sepsis.csv',
        'quasi_identifiers': ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender'],
        'sensitive_attr': 'SepsisLabel',
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v2_sepsis.csv',
        'quasi_identifiers': ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender'],
        'sensitive_attr': 'SepsisLabel',
        'e': 10,
        'k': 5,
    },
    {
        'file_name': 'v3_sepsis.csv',
        'quasi_identifiers': ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender'],
        'sensitive_attr': 'SepsisLabel',
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v4_sepsis.csv',
        'quasi_identifiers': ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender'],
        'sensitive_attr': 'SepsisLabel',
        'e': 10,
        'k': 3,
    },
    # Add other configuration dictionaries here
]

for config in configs:
    test_anonymization(config)

