__author__ = 'blumonkey'

import xml.etree.ElementTree as ET
import re
import os
import string
import sys

tree = ET.parse('/home/manvi/Documents/acads/SNLP/Project/summarization.xml')
root = tree.getroot()

import unicodedata

def binary(x):
    if x == "yes":
        return "1"
    return "0"


def caps(y):
    x=y.strip()
    if x.islower():
        return "0"
    elif x.isupper():
        return "1"
    elif x.isdigit():
        return "2"
    elif x[:-1].isdigit():
        return "3"
    elif x[1:].islower() and x[0].isupper():
        return "4"
    else:
        return "5"


max_fs = 0
for pages in root.findall('PAGE'):
    for texts in pages.findall('TEXT'):
        for token in texts.findall('TOKEN'):
            if(float(token.attrib['font-size'])>max_fs):
                max_fs=float(token.attrib['font-size'])

print max_fs

f = open('temp.txt','w')
f.write("0\t0\t0\t0\t0\t0\n")


flag = False
reg_ex = True
my_list=[]

ref = []
strs = [[]]
idx=-1

for pages in root.findall('PAGE'):
    for texts in pages.findall('TEXT'):
        for token in texts.findall('TOKEN'):
            if type(token.text) is unicode:
                word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
            else:
                word = token.text
            if(len(word.replace(' ',''))>0):
                if (word=="REFERENCES"):
                    print word + " now that's it"
                    flag = True
                    continue
                if flag==False:
                    print "REFERENCES not yet found"
                if flag==True:
                    regex = re.compile("(\[\d{1,2}\])")
                    result = re.findall(regex, word)
                    if len(result) > 0: 
                        reg_ex = True
                        idx+=1
                        if idx>0:
                            string  = " ".join(ref)
                            # print string
                            strs.append(ref)
                            my_list.append(string)
                            del ref[:] 
                        # for a in result:
                        #     # print a
                    ref.append(word)

i=0
for i in my_list:
    regex = re.compile("(\[\d{1,2}\])")
    result = re.findall(regex, i)
    print i


from subprocess import call

f1 = open('config.txt','w')

# call(["unidecode","temp.txt"],stdout=f1)
f.close()

call(["rm","temp.txt"])