import numpy as np
import pandas as pd
from joblib import dump
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder


class Commons:
    @staticmethod
    def extract_interesting_features(df, type):
        """
        Extrae las caracteristicas más importantes del dataframe para el modelo seleccionado por parametro.

        :param df: El dataframe del que se extraeran caracteristicas
        :param type: La caracteristica base que identifica al modelo que extrae las caracteristicas
        :return: un dataframe de pandas con las caracteristicas más interesantes dependiendo del modelo
        """
        if (type == "price"):
            interesting_features = ["product_color", "product_variation_inventory", "shipping_is_express",
                                    "origin_country",
                                    "price", "uses_ad_boosts", "rating", "merchant_rating", "merchant_rating_count",
                                    "merchant_has_profile_picture", "badge_product_quality", "has_urgency_banner"]

        else:
            interesting_features = ["product_color", "product_variation_inventory", "shipping_is_express",
                                    "origin_country",
                                    "units_sold", "uses_ad_boosts", "rating", "merchant_rating",
                                    "merchant_rating_count",
                                    "merchant_has_profile_picture", "badge_product_quality", "has_urgency_banner"]

        """Acerca de las varables que no podemos controlar, hay varias con se correlacionan bastante con la cantidad vendida, cómo lo son el rating_count y  los rating_x_count, pero dado que están por fuera de nuestro control, buscamos una manera de realacionaar esas variables con los tags."""

        df_interesting = df.loc[:, interesting_features]
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "<<<---------------------------- INTERESTING FEATURES ----------------------------\n" + pcolors.ENDC)
        print(df_interesting.columns)
        print("\n")
        print(df_interesting.shape)
        print(df_interesting.info())
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "   ---------------------------- INTERESTING FEATURES ---------------------------->>>\n\n" + pcolors.ENDC)
        return df_interesting

    @staticmethod
    def plot_missing_data(df):
        """
        Grafica con seaborn la cantidad de nans por columna del dataframe pasado por parametro.

        :param df: El dataframe de pandas sobre el que se hará la grafica de nans
        """
        columns_with_null = df.columns[df.isna().sum() > 0]
        null_pct = (df[columns_with_null].isna().sum() / df.shape[0]).sort_values(ascending=False) * 100
        plt.figure(figsize=(8, 6))
        sns.barplot(y=null_pct.index, x=null_pct, orient='h')
        plt.title('% Na values in dataframe by columns')

        """Asignamos valores coherentes para remplazar los nans encontrados en el dataset."""

    @staticmethod
    def clean(df):
        """
        Realiza limpieza de datos sobre el dataframe pasado por parametro. No hay valor de retorno ya que la limpieza se hace *in place*.

        :param df: El dataframe de pandas sobre el que se hará limpieza
        """
        nan_replace = {'has_urgency_banner': 0, 'origin_country': 'unknown', 'product_color': 'multicolor'}
        df.fillna(nan_replace, inplace=True)
        df = df.dropna()
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "<<<---------------------------- INTERESTING FEATURES AFTER CLEANING ----------------------------\n" + pcolors.ENDC)
        print(df.info())
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "   ---------------------------- INTERESTING FEATURES AFTER CLEANING ---------------------------->>>\n\n" + pcolors.ENDC)
        # plt.figure(figsize=(20,12))
        # sns.heatmap(corr_map,annot=True,cmap='Blues')
        # plt.xticks(rotation=45,fontsize=14)
        # plt.yticks(rotation=45,fontsize=14)
        # plt.show()

    @staticmethod
    def print_correlation_map(df, col):
        """
        Se imprime la matriz de correlación para la caracteristica seleccionada por parametro.

        :param df: El dataframe sobre el que se hace la matriz de correlación
        :param col: La columna del dataframe que se analizará
        """

        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "<<<---------------------------- CORRELATION MATRIX ----------------------------\n" + pcolors.ENDC)
        print(df.corr()[col].sort_values(ascending=False))
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "   ---------------------------- CORRELATION MATRIX ---------------------------->>>\n\n" + pcolors.ENDC)

    @staticmethod
    def plot_colors_vs_feature(df, feature):
        color_sale = df.groupby('product_color')[feature].mean()
        color_sale = color_sale.reset_index().sort_values(by=feature, ascending=False)
        top_10 = color_sale.head(15)
        sns.barplot(data=top_10, x='product_color', y=feature)

        # Ponemos los otros colores en other, para eliminar ruido
        top_10_vals = top_10.product_color.values
        df['product_color'][-df['product_color'].isin(top_10_vals)] = 'other'
        sns.barplot(data=df, x='product_color', y=feature)

    @staticmethod
    def one_hot_encode(df):
        """
        Ahora realizaremos una codificación onehot, para convertir todas las variables categoricas en varias columnas de valores enteros binarios.

        :param df: El dataframe de pandas sobre el que se hará la codificación *one-hot*
        :return: El dataframe codificado
        """

        # print(df_interesting.columns)
        categories = df.loc[:, ['product_color', 'origin_country']]
        encoder = OneHotEncoder(sparse=False)
        categories_1hot = pd.DataFrame(encoder.fit_transform(categories))
        new_categories_nms = np.concatenate([encoder.categories_[0], encoder.categories_[1]])
        categories_1hot.columns = new_categories_nms
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "<<<---------------------------- CATEGORIES ONE HOT ENCODING ----------------------------\n" + pcolors.ENDC)
        print(categories_1hot.info())
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "   ---------------------------- CATEGORIES ONE HOT ENCODING ---------------------------->>>\n\n" + pcolors.ENDC)
        df = pd.concat([df, categories_1hot], axis=1).drop(['product_color', 'origin_country'], axis=1)
        return df
        # print(df_interesting.info())

    @staticmethod
    def append_tags_analysis_columns(df, df_interesting, col):
        """
        En esta parte agregaremos 2 columnas que se relacionan con los tags:
        *   best_tag_units_sold: Escogemos el valor del tag con las mejores ventas promedio
        *   Elemento de lista: Calculamos el promedio del promedio de las ventas de todos los tag

        El primer paso es crear un diccionario con todas los precios de los productos que tienen un tag especifico.

        :param df: El dataframe original
        :param df_interesting: El dataframe con las caracteristicas de interes
        :param col: La columna de interes de los dataframe
        :return: Los dataframes recibidos por parametro modificados con las nuevas columnas
        """
        dic_tags_uts = {}

        df_search = df.loc[:, ["tags", col]]
        # print(df_search)
        df_search = df_search.values
        for row in df_search:
            # print(row)
            tags = row[0].split(",")
            units = row[1]
            for tag in tags:
                if (tag in dic_tags_uts):
                    dic_tags_uts[tag].append(units)
                else:
                    dic_tags_uts[tag] = [units]
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "<<<---------------------------- TAGS DICTIONARY ----------------------------\n" + pcolors.ENDC)
        print(dic_tags_uts.keys)
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "   ---------------------------- TAGS DICTIONARY ---------------------------->>>\n\n" + pcolors.ENDC)

        """Ahora creamos un diccionario que contiene el promedio de todos esos precios."""

        # Vamos a crear un nuevo diccionario donde solo se guarden los promedios

        for elem in dic_tags_uts:
            arr_tmp = np.array(dic_tags_uts[elem])
            dic_tags_uts[elem] = arr_tmp.mean()

        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "<<<---------------------------- AVG PRICE TAGS DICTIONARY ----------------------------\n" + pcolors.ENDC)
        print(dic_tags_uts.keys)
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "   ---------------------------- AVG PRICE TAGS DICTIONARY ---------------------------->>>\n\n" + pcolors.ENDC)

        """Ahora creamos las listas que seran convertidas en columnas y seran agregadas al data set."""

        # Crear las listas que vamos a agregar al dataset

        grt_tag_price_list = []
        avrg_tag_price_list = []
        tag_dic_vals = {}

        df_search = df.loc[:, ["tags", col]]
        # print(df_search)
        df_search = df_search.values
        for row in df_search:
            # print(row)
            tags = row[0].split(",")
            best_tag = tags[0]
            best_tag_val = dic_tags_uts[best_tag]
            avrg_tag_val = 0

            for tag in tags:
                val = dic_tags_uts[tag]
                if (best_tag_val < val):
                    best_tag = tag
                    best_tag_val = val
                avrg_tag_val += val

            avrg_tag_val /= len(tags)
            grt_tag_price_list.append(best_tag_val)
            avrg_tag_price_list.append(avrg_tag_val)

        dump(dic_tags_uts, './Resources/Persistence/tagDict.joblib')

        """Concatenamos las nuevas columnas al data set."""

        # Concatenar las nuevas columnas al data frame
        if (col == "price"):
            df_interesting["grt_tag_price"] = grt_tag_price_list
            df_interesting["avrg_tag_price"] = avrg_tag_price_list
        else:
            df_interesting["best_tag_sales"] = grt_tag_price_list
            df_interesting["avrg_tag_sales"] = avrg_tag_price_list

        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "<<<---------------------------- RESULTING DATA SET ----------------------------\n" + pcolors.ENDC)
        print(df_interesting.info())
        print(
            pcolors.OKGREEN + pcolors.UNDERLINE + pcolors.BOLD + "   ---------------------------- RESULTING DATA SET ---------------------------->>>\n\n" + pcolors.ENDC)
        return df, df_interesting


class pcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'
