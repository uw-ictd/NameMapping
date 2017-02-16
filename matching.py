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
		if (jf.jaro_winkler(unicode(value1),unicode(value2))>0.88 and dm(value1)[0]==dm(value2)[0]) or (jf.jaro_winkler(unicode(value1),unicode(value2))>0.8399 and lv.distance(value1,value2)<4 and dm(value1)[0]==dm(value2)[0]) or (jf.jaro_winkler(unicode(removeRomanNumbers(removeBracketWords(value1))),unicode(removeRomanNumbers(removeBracketWords(value2))))>0.88 and dm(removeRomanNumbers(removeBracketWords(value1)))[0]==dm(removeRomanNumbers(removeBracketWords(value2)))[0]):
			return True
	return False

def findMatches(data1,data2):
	f = open('renaloc_bureau.csv', 'wt')
	st = datetime.now()
	counter=0
	try:
		writer = csv.writer(f, quoting=csv.QUOTE_ALL)
		writer.writerow( ('ID', 'commune_ID', 'localite', 'localite_ID', 'source', 'ID', 'commune_ID', 'localite', 'localite_ID', 'source') )
		for row1 in data1:
			print row1[0]
			for row2 in data2:
				if row1[1]==row2[1]:
					#print row1[1]+' <-> '+row2[1]
					counter+=1
					if isMatch(row1[2],row2[2]):
						writer.writerow( (row1[0],row1[1],row1[2],row1[3],row1[4],row2[0],row2[1],row2[2],row2[3],row2[4]) )
				elif int(row1[1])<int(row2[1]):
					break
			#if counter>5000:
			#	break
	finally:
		f.close()
	
	ed = datetime.now()
	dif = ed-st
	print dif
	print counter


data1 = readCsvFile('renaloc_data.csv',True)
data2 = readCsvFile('bureau_data.csv',True)
findMatches(data1,data2)

