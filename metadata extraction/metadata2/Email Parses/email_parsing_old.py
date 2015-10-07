import xml.etree.ElementTree as ET
import copy
filename = raw_input()
tree = ET.parse(filename+'.xml')
root = tree.getroot()

import unicodedata

def isEmail(y):
    x=y.strip()
    isatr = 0
    for i in range(len(x)):
	if x[i] == "@":
	    isatr = 1
	if((isatr==1) and (x[i]==".") and (x[i+1]<"z" and x[i+1]>"a")):
	    return "1"
    return "0"

f = open(filename + '_mail_parse.txt','w')
f.write("0\t0\t0\n")
p = []
a = []
count = 0
bracks = 0

for pages in root.findall('PAGE'):
    count+=1
    if count>2:
	break
    for texts in pages.findall('TEXT'):
        for token in texts.findall('TOKEN'):
            if type(token.text) is unicode:
                word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
            else:
                word = token.text

	    if type(word) is not str:
		continue

	    if word.find("{")!=-1 or word.find("[")!=-1:
		bracks+=1
		#print "Found {/["
	    if bracks > 0:
		if(len(word.replace(' ',''))>0):
                    a.append((word.replace(' ','')+"\t").encode("utf-8"))
                    a.append((isEmail(token.text.encode("utf-8").replace(' ','')))+"\t")
                    a.append(("0\n").encode("utf-8"))
	        p.append(copy.copy(a))
		#print p
		del a[:]
	    
            if(len(word.replace(' ',''))>0) and bracks<=0:
                f.write((word.replace(' ','')+"\t").encode("utf-8"))
                f.write((isEmail(token.text.encode("utf-8").replace(' ','')))+"\t")
                f.write(("0\n").encode("utf-8"))
	    if word.find("}")!=-1 or word.find("]")!=-1:
		bracks -= 1
		if int(p[len(p)-1][1])==1:		#If it is email
		    for i in range(len(p)):
			p[i][1] = "1\t"
		#print p
		for i in range(len(p)):
		    for j in p[i]:
			f.write(str(j))
		del p[:]


        f.write("0\t0\t0\n")

f.close()


