import itertools
import pandas as pd

import fuzzy as fz
import jellyfish as jf
import Levenshtein as lv

from multiprocessing import cpu_count
import dask.dataframe as dd
from dask.multiprocessing import get

from preprocessing.cleaning import *

def match_metrics(data):
    """ Computes all relevant metrics for two strings, and makes a first a priori matching based on pre-specified thresholds
    """
    value1 = data.list_1
    value2 = data.list_2
    commune_ID = data.commune_ID
    dm = fz.DMetaphone()
    try :
        if isAscii(value1) and isAscii(value2):
            jaro_dist = jf.jaro_winkler(str(value1),str(value2))
            jaro_dist_clean = jf.jaro_winkler(str(removeRomanNumbers(removeBracketWords(value1))), str(removeRomanNumbers(removeBracketWords(value2))))
            metaphone_1 = dm(value1)[0]
            metaphone_2 = dm(value2)[0]
            metaphone_1_clean = dm(removeRomanNumbers(removeBracketWords(value1)))[0]
            metaphone_2_clean = dm(removeRomanNumbers(removeBracketWords(value2)))[0]
            levenshtein_dist = lv.distance(value1,value2)

            output = {'commune_ID':commune_ID,'name_1':value1, 'name_2':value2, 'jaro_dist':jaro_dist, 'jaro_dist_clean':jaro_dist_clean, 'metaphone_1':metaphone_1, 'metaphone_2':metaphone_2, 'metaphone_1_clean':metaphone_1_clean, 'metaphone_2_clean':metaphone_2_clean, 'levenshtein_dist':levenshtein_dist}
            return output
    except TypeError :
        pass

def make_pairs_distances(pairs_df):
    """ Computes all relevant metrics for a paired list of names
    """
    nCores = cpu_count()
    df = dd.from_pandas(pairs_df, npartitions=nCores)
    df_distances = df.map_partitions(
    lambda d : d.apply(
        lambda x : match_metrics(x),
        axis=1),
        meta = pd.DataFrame)
    pairs_metrics = df_distances.compute(get = get).apply(pd.Series)
    pairs_metrics['sound'] = pairs_metrics.metaphone_1 == pairs_metrics.metaphone_2
    return pairs_metrics


### Making Lists of unique names
def make_names_list(name_list):
    """ Takes a list and returns a clean list of unique values
    """
    out_list = list(name_list.unique())
    cleanedList = [x for x in out_list if str(x) != 'nan']
    return cleanedList

def make_pairs(data1, data2):
    """ Takes two lists and returns all combinations of elements from each two lists, stratified by commune_ID
    """
    pairs = []
    communes = []
    for i in data1.commune_ID.unique():
        data1_i = data1[data1.commune_ID == i]
        data2_i = data2[data2.commune_ID == i]
        list1_i = make_names_list(data1_i.localite)
        list2_i = make_names_list(data2_i.localite)
        add_pair = list(itertools.product(list1_i, list2_i))
        pairs = pairs + add_pair
        communes = communes + [i] * len(add_pair)
    pairs_df = pd.DataFrame(pairs, columns = ['list_1', 'list_2'])
    pairs_df['commune_ID'] = communes
    return pairs_df
