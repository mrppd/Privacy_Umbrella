## Repository Contents

This repository contains 2 folders:

1. **Original Datasets**: This folder includes the sepsis and heart datasets, along with a PDF file summarizing both datasets.

2. **Anonymized Datasets**: This folder contains various versions of each original dataset, anonymized using different approaches.

---

### Sepsis Dataset Anonymization

For the sepsis dataset, the following versions were created:

- **v1**: Generalized using: binning values of some attributes.
- **v2**: Generalized using: binning values of some attributes, other than those of v1.
- **v3**: Generalized using: suppression of rows according to some pre-selected attributes based on l-diversity metric.
- **v4**: Generalized using: adding noise to the original data values.

Versions v1 and v2 are more suitable for testing anonymization using partitioning- and grouping-based metrics.

---

### Heart Dataset Anonymization

For the heart dataset, the following versions were created:

- **v1**: Generalized using: rounding up, binning and categorical generalization of values of some attributes.
- **v2**: Generalized using: binning values of some attributes.
- **v3**: Generalized using: rounding up and binning into different ranges other than those of v1.
- **v4**: Generalized using: rounding up, binning and categorical generalization of values of some attributes (similar to v1, but suppressed based on different parameter values for l-diversity).
- **v5**: Generalized using: adding noise to the original data values.

Versions v1, v2, v3 and v4 are more suitable for testing anonymization using partitioning- and grouping-based metrics.

---

### Sensitive Attribute Information

In both datasets, the sensitive attribute is as follows:

- Sepsis Dataset: Attribute name: `sepsisLabel`. Binary attribute.

- Heart Dataset: Attribute name: `target`. Binary attribute.

Note: In some cases, such as with l-diversity, the parameter `l` can only have the value of 2 due to the binary nature of the sensitive attribute.

---

### Recommended Testing Guidelines

It is recommended, but not required, to follow the guidelines below for testing various metrics:

**For v1_sepsis:**

- Test for k-anonymity using `k = 3` and the following quasi-identifiers: `['Age', 'Temp', 'O2Sat', 'WBC', 'Resp', 'Gender']`.
- Test for l-diversity using the same quasi-identifiers as mentioned above.

**For v1_heart and v2_heart:**

- Test for k-anonymity using `k = 3` and the following quasi-identifiers: `['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']`.
- Test for l-diversity using the quasi-identifiers: `['age', 'sex']`.

**For v2_sepsis:**

- Test for k-anonymity using `k = 5` and the following quasi-identifiers: `['sex', 'cp', 'trestbps', 'fbs', 'restecg', 'thalach', 'exang', 'slope','ca', 'thal', 'age_range', 'chol_range', 'oldpeak_range']`.
- Test for l-diversity using the quasi-identifiers: `['Age', 'Gender']`.

**For v3_heart:**

- Test for k-anonymity using `k = 5` and the following quasi-identifiers: `['Age', 'Gender', 'HR', 'SBP', 'MAP', 'DBP']`.
- Test for l-diversity using the quasi-identifiers: `['age', 'sex']`.

**For v3_sepsis andv4_sepsis:**

- If testing with l-diversity, use `['Age', 'Gender']` as quasi-identifiers.

**For v4_heart:**

- If testing with l-divers

ity, use `['age_range', 'sex', 'restecg', 'fbs']` as quasi-identifiers.

**For Noise-based Metrics (e.g., Differential Privacy):**

- Test with v3_sepsis, v4_sepsis and v5_heart.

---

Please note that the above guidelines are recommended but not mandatory. Adjust them based on your specific testing requirements.

