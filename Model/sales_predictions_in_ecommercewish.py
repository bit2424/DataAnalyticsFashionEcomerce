# -*- coding: utf-8 -*-
"""Sales_Predictions_in_EcommerceWish.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sZQYDMGy6m20itdCYiy2wiWSKutaTh76

# Predicciones de cantidad de ventas en wish

En este nootebook se utiliza un dataset de las ventas de verano en el 2019 de Wish, la intención es ser capaces de predecir la cantidad de ventas de un producto basados en caracteristicas del producto que podamos observar o determinar, y qué estén incluidos en el dataset.

El primer paso es importar todas las librerias necesarias para el procesamiento de los datos e importar el dataset montado en una carpeta de drive.
"""

import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
# models
from sklearn.tree import DecisionTreeClassifier
from xgboost.sklearn import XGBClassifier

from common import Commons
from common import pcolors


# !pip install pywaffle --quiet


# from google.colab import drive

# drive.mount('/content/drive')

class SalesModel:
    def __init__(self):
        self.df = pd.read_csv("./Resources/Datasets/summer-products.csv")
        # /summer-products-with-rating-and-performance_2020-08.csv
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "<<<---------------------------- ORIGINAL ----------------------------\n" + pcolors.ENDC + pcolors.ENDC)
        print(self.df.columns)
        print("\n")
        print(self.df.shape)
        # https://www.kaggle.com/jmmvutu/summer-products-and-sales-in-ecommerce-wish
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "   ---------------------------- ORIGINAL ---------------------------->>>\n\n" + pcolors.ENDC)
        self.df_interesting = Commons.extract_interesting_features(self.df)

    def execute(self):
        Commons.plot_missing_data(self.df_interesting)
        Commons.clean(self.df_interesting)
        Commons.print_correlation_map(self.df_interesting, 'units_sold')
        Commons.plot_colors_vs_feature(self.df_interesting, 'units_sold')
        self.df_interesting = Commons.one_hot_encode(self.df_interesting)

        # correlation again
        Commons.print_correlation_map(self.df_interesting, 'price')
        self.df, self.df_interesting = Commons.append_tags_analysis_columns(self.df, self.df_interesting)
        self.models_creation()

    def models_creation(self):
        """# Creación de modelos

        Lo primero es seperar el dataset en tres:
        *   Conjunto de entrenamiento
        *   Conjunto de selección de hiper parametros
        *   Conjunto de prueba
        """

        X = self.df_interesting.drop(['units_sold'], axis=1)
        Y = self.df_interesting['units_sold']
        trainig_size = 0.6
        testing_size = 1 - trainig_size
        random_seed = 42
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=testing_size, random_state=random_seed,
                                                            shuffle=True)
        X_test, X_test_hp, y_test, y_test_hp = train_test_split(X, Y, test_size=0.5, random_state=random_seed,
                                                                shuffle=True)

        """En esta etapa escogemos algunos modelos que queremos entrenar y ver cómo se comportan con los datos de entrada.
        
        Escogemos una estrategía de validación cruzada para validar los resultados que obtenemos al entrenar los modelos.
        """

        base_models = [('DT_model', DecisionTreeClassifier(random_state=random_seed)),
                       ('RF_model', RandomForestClassifier(random_state=random_seed, n_jobs=-1)),
                       ('LR_model', LogisticRegression(random_state=random_seed, n_jobs=-1)),
                       ("XGB_model", XGBClassifier(random_state=random_seed, n_jobs=-1)),
                       ("ETR_model", ExtraTreesRegressor(n_estimators=20, random_state=random_seed))]
        # Dividir los datos en partes 'kfolds' para la validación cruzada
        # utilizar la random shufle para garantizar la distribución aleatoria de los datos
        kfolds = 5
        split = KFold(n_splits=kfolds, shuffle=True, random_state=random_seed)

        # Preprocesamiento, entrenamiento y calificación para cada uno de los modelos que escogimos:
        for name, model in base_models:
            temp_model = Pipeline(steps=[('model', model)])
            temp_model.fit(X_train, y_train)
            cv_results = cross_val_score(temp_model, X_train, y_train, cv=split, n_jobs=-1)
            # Salida:
            min_score = round(min(cv_results), 4)
            max_score = round(max(cv_results), 4)
            mean_score = round(np.mean(cv_results), 4)
            std_dev = round(np.std(cv_results), 4)
            print(
                f'{name} cross validation accuracy score:{mean_score} +- {std_dev} (std) min:{min_score},max:{max_score}')

        """Seleccionamos los 3 modelos con mejores resultados y procedemos a ajustar algunos hiperparametros que nos permitan obtener mejores resultados."""

        # temp_model =
        # temp_model.fit(X_test_hp, y_tes_hp)
        # cv_results = cross_val_score(temp_model,X_train,y_train,cv=split,n_jobs=-1)
        # # output:
        # min_score = round(min(cv_results),4)
        # max_score = round(max(cv_results),4)
        # mean_score = round(np.mean(cv_results),4)
        # std_dev = round(np.std(cv_results),4)
        # print(f'{name} cross validation accuracy score:{mean_score} +- {std_dev} (std) min:{min_score},max:{max_score}')

        x_vals = []
        y_scores = []
        # X_test.drop("prediction",axis=1)
        for i in range(1, 30):
            temp_model = ExtraTreesRegressor(n_estimators=i, random_state=random_seed)
            temp_model.fit(X_train, y_train)
            cv_results = cross_val_score(temp_model, X_test_hp, y_test_hp, cv=split, n_jobs=-1)
            y_predict = cv_results.mean()
            x_vals.append(i)
            y_scores.append(y_predict)

        sns.scatterplot(x=x_vals, y=y_scores)
        # print(y_scores)
        print(X_test_hp.columns)
        print(temp_model.feature_importances_)

        x_vals = []
        y_scores = []
        # X_test.drop("prediction",axis=1)
        for i in range(1, 30):
            temp_model = DecisionTreeClassifier(random_state=random_seed, max_depth=i)
            temp_model.fit(X_train, y_train)
            cv_results = cross_val_score(temp_model, X_test_hp, y_test_hp, cv=split, n_jobs=-1)
            y_predict = cv_results.mean()
            x_vals.append(i)
            y_scores.append(y_predict)

        sns.scatterplot(x=x_vals, y=y_scores)
        print(X_test_hp.columns)
        print(temp_model.feature_importances_)

        x_vals = []
        y_scores = []
        # X_test.drop("prediction",axis=1)
        for i in range(1, 40):
            temp_model = XGBClassifier(random_state=random_seed, n_jobs=-1, n_estimators=i)
            temp_model.fit(X_train, y_train)
            cv_results = cross_val_score(temp_model, X_test_hp, y_test_hp, cv=split, n_jobs=-1)
            y_predict = cv_results.mean()
            x_vals.append(i)
            y_scores.append(y_predict)

        sns.scatterplot(x=x_vals, y=y_scores)
        # print(y_scores)
        print(X_test_hp.columns)
        print(temp_model.feature_importances_)

        """Al final evaluamos el mejor modelo con los datos de testing, para ver cómo nos va. """

        temp_model = ExtraTreesRegressor(n_estimators=30, random_state=random_seed)
        temp_model.fit(X_train, y_train)
        cv_results = cross_val_score(temp_model, X_test, y_test, cv=split, n_jobs=-1)
        # output:
        min_score = round(min(cv_results), 4)
        max_score = round(max(cv_results), 4)
        mean_score = round(np.mean(cv_results), 4)
        std_dev = round(np.std(cv_results), 4)
        print(f'{name} cross validation accuracy score:{mean_score} +- {std_dev} (std) min:{min_score},max:{max_score}')

        """El modelo tuvo un resultado que todavía puede mejorar, somos capaces de predecir la cantidad vendida adecuada casí un 40% de las veces, si bien no es ideal es una guia bastante buena que pude seguir mejorando."""
