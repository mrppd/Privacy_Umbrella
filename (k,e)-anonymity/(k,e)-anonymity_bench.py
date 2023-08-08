"""
@author Kristian Lee, 6547510

"""

import pandas as pd
from typing import List


class Anonymize:
    """
    Anonymization class for assessing K-anonymity, L-diversity, and E-uniqueness levels in a dataset.
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

    def find_l(self, df: pd.DataFrame, quasi_identifiers: List[str], sensitive_attr: str, l: int) -> bool:
        """
        Check if the dataset satisfies the desired L-diversity level based on the quasi-identifiers and
        the number of unique values in the sensitive attribute.

        Args:
            df (pd.DataFrame): The dataset.
            quasi_identifiers (List[str]): List of column names representing the quasi-identifiers.
            sensitive_attr (str): The column name representing the sensitive attribute.
            l (int): The desired minimum number of unique values in the sensitive attribute.

        Returns:
            bool: True if the dataset satisfies the desired L-diversity level, False otherwise.
        """
        groups = df.groupby(quasi_identifiers)
        l_diversity_values = groups[sensitive_attr].apply(lambda x: x.nunique() >= l)
        return all(l_diversity_values)

    def find_e(self, df: pd.DataFrame, quasi_identifiers: List[str], sensitive_attr: str, e: int) -> bool:
        """
        Check if the dataset satisfies the desired E-uniqueness level based on the proportions of group sizes.

        Args:
            df (pd.DataFrame): The dataset.
            quasi_identifiers (List[str]): List of column names representing the quasi-identifiers.
            sensitive_attr (str): The column name representing the sensitive attribute.
            e (int): The privacy parameter for E-uniqueness.

        Returns:
            bool: True if the dataset satisfies the desired E-uniqueness level, False otherwise.
        """
        # Group by quasi-identifiers and sensitive attribute.
        groups_with_sensitive = df.groupby(quasi_identifiers + [sensitive_attr])
        # Compute the sizes of these groups.
        group_sizes_with_sensitive = groups_with_sensitive.size()

        # Group by quasi-identifiers only.
        groups_without_sensitive = df.groupby(quasi_identifiers)
        # Compute the sizes of these groups.
        group_sizes_without_sensitive = groups_without_sensitive.size()

        # For each group defined by quasi-identifiers + sensitive attribute,
        # find the corresponding group size of the group defined by quasi-identifiers only.
        indices_to_match = [index[:-1] for index in group_sizes_with_sensitive.index.to_list()]
        matching_group_sizes_without_sensitive = group_sizes_without_sensitive.reindex(indices_to_match).fillna(0)

        # Compute the proportions.
        proportions = group_sizes_with_sensitive / matching_group_sizes_without_sensitive.values

        # Check if all proportions are less than or equal to 1/e.
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
    l_diversity = anonymize.find_l(df, config['quasi_identifiers_l'], config['sensitive_attr'], config['l'])
    e_uniqueness = anonymize.find_e(df, config['quasi_identifiers_l'], config['sensitive_attr'], config['e'])

    print(f"Dataset {config['file_name']} satisfies desired K-anonymity level: {k_anonymity_check}")
    print(f"Dataset {config['file_name']} satisfies desired L-diversity level: {l_diversity}")
    print(f"Dataset {config['file_name']} satisfies desired E-uniqueness level: {e_uniqueness}")


configs = [
    {
        'file_name': 'v1_heart.csv',
        'quasi_identifiers': ['age_range', 'sex', 'cp', 'trestbps', 'chol_range', 'fbs', 'restecg', 'thalach', 'exang',
                              'oldpeak_range', 'slope', 'ca', 'thal'],
        'quasi_identifiers_l': ['age_range', 'sex'],
        'sensitive_attr': 'target',
        'l': 2,
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v2_heart.csv',
        'quasi_identifiers': ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang',
                              'oldpeak', 'slope', 'ca', 'thal'],
        'quasi_identifiers_l': ['age', 'sex'],
        'sensitive_attr': 'target',
        'l': 2,
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v3_heart.csv',
        'quasi_identifiers': ['sex', 'cp', 'trestbps', 'fbs', 'restecg', 'thalach', 'exang', 'slope','ca', 'thal',
                              'age_range', 'chol_range', 'oldpeak_range'],
        'sensitive_attr': 'target',
        'quasi_identifiers_l': ['age_range', 'sex'],
        'l': 2,
        'e': 10,
        'k': 5,
    },
    {
        'file_name': 'v4_heart.csv',
        'quasi_identifiers': ['sex', 'cp', 'trestbps', 'fbs', 'restecg', 'thalach', 'exang', 'slope', 'ca', 'thal',
                              'age_range', 'chol_range', 'oldpeak_range'],
        'sensitive_attr': 'target',
        'quasi_identifiers_l': ['age_range', 'sex', 'restecg', 'fbs'],
        'l': 2,
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v5_heart.csv',
        'quasi_identifiers': ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang',
                              'oldpeak', 'slope', 'ca', 'thal'],
        'sensitive_attr': 'target',
        'quasi_identifiers_l': ['age', 'sex'],
        'l': 2,
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v1_sepsis.csv',
        'quasi_identifiers': ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender'],
        'quasi_identifiers_l': ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender'],
        'sensitive_attr': 'SepsisLabel',
        'l': 2,
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v2_sepsis.csv',
        'quasi_identifiers': ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender'],
        'quasi_identifiers_l': ['Age', 'Gender'],
        'sensitive_attr': 'SepsisLabel',
        'l': 2,
        'e': 10,
        'k': 5,
    },
    {
        'file_name': 'v3_sepsis.csv',
        'quasi_identifiers': ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender'],
        'quasi_identifiers_l': ['Age', 'Gender'],
        'sensitive_attr': 'SepsisLabel',
        'l': 2,
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v4_sepsis.csv',
        'quasi_identifiers': ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender'],
        'quasi_identifiers_l': ['Age', 'Gender'],
        'sensitive_attr': 'SepsisLabel',
        'l': 2,
        'e': 10,
        'k': 3,
    },
    {
        'file_name': 'v1_kidney.csv',
        'quasi_identifiers': ['age', 'bp', 'bgr', 'bu', 'sc', 'hemo', 'wc', 'rc'],
        'quasi_identifiers_l': ['age'],
        'sensitive_attr': 'classification',
        'l': 2,
        'e': 10,
        'k': 2,
    },
    {
        'file_name': 'v2_kidney.csv',
        'quasi_identifiers': ['age', 'bp', 'bgr', 'bu', 'sc', 'hemo', 'wc', 'rc'],
        'quasi_identifiers_l': ['age'],
        'sensitive_attr': 'classification',
        'l': 2,
        'e': 10,
        'k': 2,
    },
    {
        'file_name': 'v1_personal_key_indicators.csv',
        'quasi_identifiers': ['Sex', 'Race'],
        'quasi_identifiers_l': ['AgeCategory'],
        'sensitive_attr': 'HeartDisease',
        'l': 2,
        'e': 10,
        'k': 2,
    },
    {
        'file_name': 'anonymized_PKI .csv',
        'quasi_identifiers': ['Sex', 'Race'],
        'quasi_identifiers_l': ['AgeCategory'],
        'sensitive_attr': 'HeartDisease',
        'l': 2,
        'e': 10,
        'k': 2,
    },
    # Add other configuration dictionaries here
]

for config in configs:
    test_anonymization(config)
