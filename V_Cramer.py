#########################################
# Chargement des packages necessaires ###
#########################################
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
import scipy.stats as ss

def V_cramer(confusion_matrix):
    chi2 = ss.chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum()
    min_dim = min(confusion_matrix.shape) - 1
    return np.sqrt(chi2 / (n * min_dim))

def V_cramer_matrix(df):
    columns = df.columns
    cramers_v_matrix = pd.DataFrame(index=columns, columns=columns)

    for col1 in columns:
        for col2 in columns:
            if col1 != col2:
                confusion_matrix = pd.crosstab(df[col1], df[col2])
                cramers_v_matrix.loc[col1, col2] = V_cramer(confusion_matrix.values)
            else:
                cramers_v_matrix.loc[col1, col2] = 1.0

    return cramers_v_matrix

#####################################################################
### Utilisation #####################################################
#####################################################################

# Charger le dataset Iris
iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['target'] = iris.target

# Discrétiser les variables continues
for col in df.columns[:-1]:
    df[col] = pd.qcut(df[col], q=3, labels=['low', 'medium', 'high'])

# Calculer la matrice du V de Cramer
result = V_cramer_matrix(df)

# Afficher le résultat arrondi à 2 décimales
print(result.round(2))