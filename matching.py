import csv
import Levenshtein as lv
import fuzzy as fz
import jellyfish as jf
import numpy as np
from datetime import datetime
import time
import pandas as pd

import ipyparallel
import subprocess

import os

os.chdir('../NameMapping')

start_cluster_command = 'ipcluster start -n 4'
subprocess.Popen(start_cluster_command)


print('Starting Cluster')
for i in range(0,100):
    while True:
        try:
            clients = ipyparallel.Client()
            dview = clients[:]
        except:
            time.sleep(5)
            continue
        break


def removeRomanNumbers(value):
	w = ['i','ii','iii','iv','v','vi','vii','viii','ix','x']
	t = value.rsplit(None,1)
	if len(t)==2 and t[1] in w:
		return t[0]
	return value

def removeBracketWords(value):
	if '(' in value and ')' in value:
		s = value.rfind('(')
		e = value.rfind(')')
		if s < e:
			return value[0:s]+value[e+1:len(value)]
	return value

def isAscii(s):
    return all(ord(c) < 128 for c in s)

def isMatch(value1,value2):
	dm = fz.DMetaphone()
	soundex = fz.Soundex(7)
	try :
		if isAscii(value1) and isAscii(value2):
		#if jf.jaro_winkler(unicode(value1),unicode(value2))>0.88 and lv.distance(value1,value2)<4 and dm(value1)[0]==dm(value2)[0] and fz.nysiis(value1)==fz.nysiis(value2):
		#if jf.jaro_winkler(unicode(value1),unicode(value2))>0.88 and lv.distance(value1,value2)<4 and dm(value1)[0]==dm(value2)[0]:
		#if jf.jaro_winkler(unicode(value1),unicode(value2))>0.88 and dm(value1)[0]==dm(value2)[0]:
		#if (jf.jaro_winkler(unicode(value1),unicode(value2))>0.88 and dm(value1)[0]==dm(value2)[0]) or (jf.jaro_winkler(unicode(value1),unicode(value2))>0.8399 and lv.distance(value1,value2)<4 and dm(value1)[0]==dm(value2)[0]) or (jf.jaro_winkler(unicode(removeRomanNumbers(removeBracketWords(value1))),unicode(removeRomanNumbers(removeBracketWords(value2))))>0.88 and dm(removeRomanNumbers(removeBracketWords(value1)))[0]==dm(removeRomanNumbers(removeBracketWords(value2)))[0]):
		#if (jf.jaro_winkler(unicode(value1),unicode(value2))>0.88 and dm(value1)[0]==dm(value2)[0]) or (jf.jaro_winkler(unicode(value1),unicode(value2))>0.8399 and lv.distance(value1,value2)<4 and dm(value1)[0]==dm(value2)[0]) or (jf.jaro_winkler(unicode(removeBracketWords(value1)),unicode(removeBracketWords(value2)))>0.88 and dm(removeBracketWords(value1))[0]==dm(removeBracketWords(value2))[0]):
			jaro_dist = jf.jaro_winkler(unicode(value1),unicode(value2))
			jaro_dist_clean = jf.jaro_winkler(unicode(removeRomanNumbers(removeBracketWords(value1))), unicode(removeRomanNumbers(removeBracketWords(value2))))
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
	localite_1 = data1['localite']
	localite_2 = data2['localite'].iloc[0]
	match_result = isMatch(localite_1 , localite_2)
	if (type(match_result) == dict):
		match_result['localite_1'] = localite_1
		match_result['localite_2'] = localite_2
		match_out = pd.DataFrame(match_result , index = [data1['ID']])
		return match_out

def findMatches(data1 , data2):
	data1 = data1.iloc[0]
	print(data1['localite_ID'])
	commune_ID = data1['commune_ID']
	data2_commune = data2[data2.commune_ID == commune_ID]
	data_out = data2_commune.groupby('localite_ID').apply(match_and_output , data1)
	return data_out.reset_index()



#data1 = pd.read_csv('renaloc_data.csv')
#data2 = pd.read_csv('bureau_data.csv')


## Create Cluster to run
%%time
out = data1.groupby(['commune_ID' , 'localite_ID']).apply(findMatches , data2)



out.to_csv('renaloc_bureau_full.csv')
