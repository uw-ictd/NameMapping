import csv
import Levenshtein as lv
import fuzzy as fz
import jellyfish as jf
import numpy as np
from datetime import datetime
import csv


def readCsvFile(filename,hasHeader):
	data = []
	opFile = open(filename,'rU')
	try:
		reader = csv.reader(opFile)
		rowNo = 0
		for row in reader:
			#print row
			if rowNo == 0 and hasHeader:
				header = row
			else:
				data.append(row)
				colNo = 0
				for col in row:
					#print col
					colNo += 1
			rowNo += 1
	finally:
		opFile.close()
	return data

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

		output = [matched , jaro_dist , jaro_dist_clean , metaphone_1 , metaphone_2 , metaphone_1_clean , metaphone_2_clean , levenshtein_dist]
		return output

def findMatches(data1 , data2 , ouptut_file):
	f = open(ouptut_file, 'wt')
	perc = 0
	count = 0
	l = len(data1)
	try:
		writer = csv.writer(f, quoting=csv.QUOTE_ALL)
		writer.writerow( ('ID', 'commune_ID', 'localite', 'localite_ID', 'source', 'ID', 'commune_ID', 'localite', 'localite_ID', 'source' , 'matched' , 'jaro_dist' , 'jaro_dist_clean' , 'metaphone_1' , 'metaphone_2' , 'metaphone_1_clean' , 'metaphone_2_clean' , 'levenshtein_dist') )
		for row1 in data1:
			count = count + 1
			stream = count / l
			if int(stream * 100) > perc :
				perc = int(stream * 100)
				print str(perc) + " % made"
			for row2 in data2:
				if row1[1]==row2[1]:
					match_result = isMatch(row1[2],row2[2])
					if (type(match_result) == list):
						writer.writerow( (row1[0] , row1[1] , row1[2] , row1[3] , row1[4] , \
						row2[0] , row2[1] , row2[2] , row2[3] , row2[4] , \
						match_result[0] , match_result[1] , match_result[2] , match_result[3] , match_result[4] , match_result[5] , match_result[6] , match_result[7]))

	finally:
		f.close()

# TODO Move into pandas : easier for subsetting
data1 = readCsvFile('renaloc_data.csv',True)
data2 = readCsvFile('bureau_data.csv',True)

%%time
findMatches(data1 , data2 , 'renaloc_bureau_full.csv')
