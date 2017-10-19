## This modules defines the functions used for the unsupervised matching of names from different sources

import Levenshtein as lv
import fuzzy as fz
import jellyfish as jf
import pandas as pd

from cleaning import *

def isMatch(value1,value2):
    """ Computes all relevant metrics for two strings, and makes a first a priori matching based on pre-specified thresholds
    TODO: This function should probably be split in two separate functions :
        * Computing the methods
        * Thresholding
    """
    dm = fz.DMetaphone()
    soundex = fz.Soundex(7)
    try :
        if isAscii(value1) and isAscii(value2):
            jaro_dist = jf.jaro_winkler(str(value1),str(value2))
            jaro_dist_clean = jf.jaro_winkler(str(removeRomanNumbers(removeBracketWords(value1))), str(removeRomanNumbers(removeBracketWords(value2))))
            metaphone_1 = dm(value1)[0]
            metaphone_2 = dm(value2)[0]
            metaphone_1_clean = dm(removeRomanNumbers(removeBracketWords(value1)))[0]
            metaphone_2_clean = dm(removeRomanNumbers(removeBracketWords(value2)))[0]
            levenshtein_dist = lv.distance(value1,value2)

            matched = (jaro_dist > 0.88 and metaphone_1 == metaphone_2) or \
                ( jaro_dist >0.8399 and levenshtein_dist <4 and metaphone_1 == metaphone_2 ) or \
                (jaro_dist_clean > 0.88 and  metaphone_1_clean == metaphone_2_clean)

            output = {'matched':matched , 'jaro_dist':jaro_dist , 'jaro_dist_clean':jaro_dist_clean , 'metaphone_1':metaphone_1 , 'metaphone_2':metaphone_2 , 'metaphone_1_clean':metaphone_1_clean , 'metaphone_2_clean':metaphone_2_clean , 'levenshtein_dist':levenshtein_dist}

            return output
    except TypeError :
        pass



def match_and_output(data2 , data1):
    """ Wrapper that takes commune subset, makes the match and formats the output
    """
    localite_1 = data1['localite']
    localite_2 = data2['localite'].iloc[0]
    match_result = isMatch(localite_1 , localite_2)
    if (type(match_result) == dict):
        match_result['localite_1'] = localite_1
        match_result['localite_2'] = localite_2
        match_out = pd.DataFrame(match_result , index = [data1['ID']])
        return match_out

def findMatches(data1 , data2):
    """ Wrapper function that takes the raw data, subsets the second dataset on commune, and returns all pairs"""
    data1 = data1.iloc[0]
    print(data1['localite_ID'])
    commune_ID = data1['commune_ID']
    data2_commune = data2[data2.commune_ID == commune_ID]
    data_out = data2_commune.groupby('localite_ID').apply(match_and_output , data1)
    return data_out.reset_index()
