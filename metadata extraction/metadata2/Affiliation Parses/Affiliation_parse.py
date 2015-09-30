__author__ = 'priyankpalod'

import xml.etree.ElementTree as ET

tree = ET.parse('/home/barno/Desktop/nlp/tfiles/t1.xml')
root = tree.getroot()

import unicodedata

max_fs = 0
for pages in root.findall('PAGE'):
    for texts in pages.findall('TEXT'):
        for token in texts.findall('TOKEN'):
            if(float(token.attrib['font-size'])>max_fs):
                max_fs=float(token.attrib['font-size'])

print max_fs


def isAffiliation(y,fs):
    x=y.strip()						
    if fs == max_fs:		#If in Title (Biggest Font Size) it can't be affiliation.
	# print x
	return "0"		#Done to prevent cases when "Research" comes in title (often)
    if x.find("University")!=-1 or x.find("School")!=-1 or x.find("Labs")!=-1 or x.find("Laboratories")!=-1 or x.find("Institute")!=-1 or x.find("Institution")!=-1 or x.find("Laboratory")!=-1 or x.find("Research")!=-1 or x.find("College")!=-1:
        return "1"
    return "0"

f = open('t1.txt','w')
f.write("0\t0\t0\n")

def FindAffiliation(stri,fs):
    l = []
    a = []
    t = stri.split(',')
    for j in t:
	j = j.strip()
	#print j
	aff = isAffiliation(j,fs)
	#print aff
	x = j.split(' ')
	for i in x:
	    if len(i) > 0:
	    	f.write((i+"\t").encode("utf-8"))
	    	f.write(aff + "\t")
	    	f.write(("0\n").encode("utf-8"))

stri = ""
count = 0;
for pages in root.findall('PAGE'):
    count+=1
    if count>2:
	break
    for texts in pages.findall('TEXT'):
        for token in texts.findall('TOKEN'):
	    if type(token.text) is unicode:
		stri += unicodedata.normalize('NFKD', token.text).encode('ascii','ignore') + " "
	    else:
		stri += token.text + " "
	FindAffiliation(stri,float(token.attrib['font-size']))
	stri = ""
        f.write("0\t0\t00\n")

f.close()

