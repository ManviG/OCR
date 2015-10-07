__author__ = 'priyankpalod'
import xml.etree.ElementTree as ET
filename = raw_input()
tree = ET.parse(filename+'.xml')
root = tree.getroot()

import unicodedata

max_fs = 0
for pages in root.findall('PAGE'):
    for texts in pages.findall('TEXT'):
        for token in texts.findall('TOKEN'):
	    if token.text is None:
		continue
            if(float(token.attrib['font-size'])>max_fs):
                max_fs=float(token.attrib['font-size'])

#print max_fs


def isAffiliation(y,fs):
    x=y.strip()						
    x=x.strip(',')
    if fs == max_fs:		#If in Title (Biggest Font Size) it can't be affiliation.
	#print x
	return "0"		#Done to prevent cases when "Research" comes in title (often)
    if x.find("Universit")!=-1 or x.find(" Labs")!=-1 or x.find("Laboratories")!=-1 or x.find("Institut")!=-1 or x.find("Research")!=-1 or x.find("College")!=-1 or x.find("Corporat")!=-1:
	t = x.split(' ')
	countsmall = 0
	countall = 0
	for word in t:
	    countall += 1
	    if word == word.lower():
		countsmall += 1
	#print str(countall) + " " + str(countsmall)  
	if countsmall > 3:
		return "0"
	#print "Yes " + word
        return "1"
    return "0"

f = open(filename+'_parse.txt','w')
f.write("0\t0\t0\n")

def FindAffiliation(stri,fs):
    l = []
    a = []
    stri = ((((((((((stri.strip('1')).strip('2')).strip('3')).strip('4')).strip('5')).strip('6')).strip('7'))).strip('8')).strip('9')).strip('0')
    #print stri
    t = stri.split(',')
    aff = "0"
    for j in t:
	j = j.strip()
	#print j
	if aff == "1" and isAffiliation(j,fs) == "0":
	    if (j.split(' '))[0] is "":
		continue
	    if ((j.split(' '))[0])[0].isupper():
		aff = "1"
	    else:
		aff = "0"
	else:
	    aff = isAffiliation(j,fs)
	#print aff
	x = j.split(' ')
	for i in x:
	    if len(i) > 0:
	    	f.write((i+"\t").encode("utf-8"))
	    	f.write(aff + "\t")
	    	f.write(("0\n").encode("utf-8"))
stri = ""
countpage = 0
for pages in root.findall('PAGE'):
    countpage+=1
    if countpage>1:
	break
    for texts in pages.findall('TEXT'):
        for token in texts.findall('TOKEN'):
	    if token.text is None:
		continue
	    if type(token.text) is unicode:
		stri += unicodedata.normalize('NFKD', token.text).encode('ascii','ignore') + " "
	    else:
		stri += token.text + " "
	if stri.replace(' ','').upper is "ABSTRACT" or stri.replace(' ','').upper is "INTRODUCTION":
	    break
	FindAffiliation(stri,float(token.attrib['font-size']))
	stri = ""
        f.write("0\t0\t0\n")

f.close()

