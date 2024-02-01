import pandas
from math import log2

def entropy(member_probabilities):
    _entropy = 0.0
    for probability in member_probabilities:
        _entropy -= probability * log2(probability)
    return _entropy

if __name__ == "__main__":
    print('Privacy Scores')
    print('==============')

    # Specify the list of all datasets to be evaluated. Each dataset is a tuple of the form (path, name, quasi_identifiers).
    testing_sets = [
        ("../original_datasets/sepsis.csv", "Sepsis Original", ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender']),
        ("../anonymized_datasets/v1_sepsis.csv", "Sepsis Anonymized V1", ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender']),
        ("../anonymized_datasets/v2_sepsis.csv", "Sepsis Anonymized V2", ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender']),
        ("../anonymized_datasets/v3_sepsis.csv", "Sepsis Anonymized V3", ['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender']),
        ("../original_datasets/heart.csv", "Heart Original", ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']),
        ("../anonymized_datasets/v1_heart.csv", "Heart Anonymized V1", ['sex', 'cp', 'trestbps', 'chol_range', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak_range', 'slope', 'ca', 'thal']),
        ("../anonymized_datasets/v2_heart.csv", "Heart Anonymized V2", ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']),
        ("../anonymized_datasets/v3_heart.csv", "Heart Anonymized V3", ['sex', 'cp', 'trestbps', 'chol_range', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak_range', 'slope', 'ca', 'thal']),
        ("../anonymized_datasets/v4_heart.csv", "Heart Anonymized V4", ['sex', 'cp', 'trestbps', 'chol_range', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak_range', 'slope', 'ca', 'thal']),
        ("../anonymized_datasets/v5_heart.csv", "Heart Anonymized V5", ['sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']),
    ]
    for path, name, quasi_identifiers in testing_sets:
        # Step 1: Figure out all anonymity sets, and get the size of each one, respectively
        anonymity_sets = pandas.read_csv(path).groupby(quasi_identifiers).size().reset_index(name='Size')

        total_entropy = 0.0

        # Step 2: Loop through all anonymity sets
        for set_size in anonymity_sets['Size']:
            # Step 3: We have to assign a probability to each member of the anonymity set.
            # An adversary could assign this probability for each member using a variety of methods, such as prior knowledge
            # or random guessing. We will use random guessing in this example. Therefore, the probability for each member
            # of the anonymity set to be the target is 1 / set_size.
            total_entropy += entropy(member_probabilities=[1 / set_size for _ in range(set_size)])

        print(f"{name}:", total_entropy)
