import xml.etree.ElementTree as ET

# Paper to be parsed
tree = ET.parse('/home/barno/Desktop/nlp/paper5/paper5.xml')
root = tree.getroot()

import unicodedata

def binary(x):
    if x == "yes":
        return "1"
    return "0"

def startCaps(y):
	x=y.strip()
	if x[0].isupper():
		return "1"
	else:
		return "0"

max_fs = 0
tot_txt = 0
for pages in root.findall('PAGE'):
    for texts in pages.findall('TEXT'):
    	tot_txt = tot_txt + 1
        for token in texts.findall('TOKEN'):
            if(float(token.attrib['font-size'])>max_fs):
                max_fs=float(token.attrib['font-size'])

f = open('paper5.txt','w')
f.write("0\t0\t0\t0\t0\t0\n")

txt = 0;
for pages in root.findall('PAGE'):
    for texts in pages.findall('TEXT'):
    	txt = txt + 1;
        for token in texts.findall('TOKEN'):
            if type(token.text) is unicode:
                word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
            else:
                word = token.text
            if(len(word.replace(' ',''))>0):
                f.write((word.replace(' ','')+"\t").encode("utf-8"))
                f.write((binary(token.attrib['bold'])+"\t").encode("utf-8"))
                f.write((str(round(float(txt)/(tot_txt),2))+"\t").encode("utf-8"))
                f.write((str(round(float(token.attrib['font-size'])/(max_fs),2))+"\t").encode("utf-8"))
                f.write((startCaps(token.text.encode("utf-8").replace(' ','')))+"\t")
                f.write(("0\n").encode("utf-8"))
        f.write("0\t0\t0\t0\t0\t0\n\n")

from subprocess import call

f1 = open('config.txt','w')

call(["unidecode","paper5.txt"],stdout=f1)
f.close()

call(["rm","temp1.txt"])