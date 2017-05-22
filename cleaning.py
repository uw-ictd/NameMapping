## This module defines the functions used to clean the names of localities.

def removeRomanNumbers(value):
    """ Removes roman numbers from names.

    :param value: A locality name to be cleaned.
    :type value: str
    """
	w = ['i','ii','iii','iv','v','vi','vii','viii','ix','x']
	t = value.rsplit(None,1)
	if len(t)==2 and t[1] in w:
		return t[0]
	return value

def removeBracketWords(value):
    """ Removes words in brackets from names.

    :param value: A locality name to be cleaned.
    :type value: str
    """
	if '(' in value and ')' in value:
		s = value.rfind('(')
		e = value.rfind(')')
		if s < e:
			return value[0:s]+value[e+1:len(value)]
	return value

def isAscii(s):
    return all(ord(c) < 128 for c in s)
