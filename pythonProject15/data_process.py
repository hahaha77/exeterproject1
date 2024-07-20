import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
def data_process():
    # Load the dataset
    file_path = 'METABRIC_RNA_Mutation.csv'
    data = pd.read_csv(file_path, low_memory=False)
    all_columns = [
        'age_at_diagnosis', 'type_of_breast_surgery', 'cancer_type', 'cancer_type_detailed',
        'cellularity', 'pam50_+_claudin-low_subtype', 'er_status', 'her2_status',
        'inferred_menopausal_state', 'integrative_cluster', 'primary_tumor_laterality',
        'pr_status', 'chemotherapy', 'hormone_therapy', 'radio_therapy'
    ]
    state_columns = [
        'age_at_diagnosis', 'type_of_breast_surgery', 'cancer_type', 'cancer_type_detailed',
        'cellularity', 'pam50_+_claudin-low_subtype', 'er_status', 'her2_status',
        'inferred_menopausal_state', 'integrative_cluster', 'primary_tumor_laterality',
        'pr_status'
    ]
    action_columns = ['chemotherapy', 'hormone_therapy', 'radio_therapy']
    # for column in state_data.columns:
    #     print(f"Value counts for column {column}:")
    #     print(state_data[column].value_counts())
    #     print()
    # Define the mappings for the provided categorical variables
    mappings = {
        'type_of_breast_surgery': {'MASTECTOMY': 1, 'BREAST CONSERVING': 2},
        'cancer_type': {'Breast Cancer': 1, 'Breast Sarcoma': 2},
        'cancer_type_detailed': {
            'Breast Invasive Ductal Carcinoma': 1,
            'Breast Mixed Ductal and Lobular Carcinoma': 2,
            'Breast Invasive Lobular Carcinoma': 3,
            'Breast Invasive Mixed Mucinous Carcinoma': 4,
            'Breast': 5,
            'Metaplastic Breast Cancer': 6
        },
        'cellularity': {'Low': 1, 'Moderate': 2, 'High': 3},
        'pam50_+_claudin-low_subtype': {
            'claudin-low': 1, 'LumA': 2, 'LumB': 3, 'Her2': 4, 'Normal': 5, 'Basal': 6, 'NC': 7
        },
        'er_status': {'Positive': 1, 'Negative': 0},
        'her2_status_measured_by_snp6': {'Positive': 1, 'Negative': 0},
        'her2_status': {'Positive': 1, 'Negative': 0},
        'inferred_menopausal_state': {'Post': 1, 'Pre': 0},
        'integrative_cluster': {
            '4ER+': 1, '3': 2, '9': 3, '7': 4, '4ER-': 5, '5': 6, '8': 7, '10': 8, '1': 9, '2': 10, '6': 11
        },
        'primary_tumor_laterality': {'Left': 1, 'Right': 0},
        'pr_status': {'Positive': 1, 'Negative': 0},
        # '3-gene_classifier_subtype': {
        #     'ER-/HER2-': 1, 'ER+/HER2- High Prolif': 2, 'ER+/HER2- Low Prolif': 3, 'HER2+': 4
        # }
    }

    data.columns = data.columns.str.strip()
    for column, mapping in mappings.items():
        if column in data.columns:
            data.loc[:, column] = data[column].map(mapping)
    data = data[all_columns]
    data = data.dropna()
    state_data = data[state_columns]
    scaler = StandardScaler()

    state_data = pd.DataFrame(scaler.fit_transform(state_data), columns=state_data.columns)
    action_data = data[action_columns]
    X_train, X_test, y_train, y_test = train_test_split(state_data, action_data, test_size=0.1, random_state=42)
    return X_train, X_test, y_train, y_test
