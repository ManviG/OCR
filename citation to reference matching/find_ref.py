__author__ = 'ManviG'

import xml.etree.ElementTree as ET
import re
import os
import string
import sys

tree = ET.parse('/home/manvi/Documents/acads/SNLP/Project/OCR/summary_citation_context_works.xml')
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
tokens_attrib = [{}]
idx=-1
Reference =[]
refer_str = []

for pages in root.findall('PAGE'):
    for texts in pages.findall('TEXT'):
        for token in texts.findall('TOKEN'):
            if type(token.text) is unicode:
                word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
            else:
                word = token.text
            if(len(word.replace(' ',''))>0):
                if ((word=="REFERENCES" or word=="References") and binary(token.attrib['bold'])):
                    print word + " now that's it"
                    flag = True
                    continue
                if flag==False:
                    pass
                if flag==True:
                    tokens_attrib.append(token.attrib)
                    ref.append(word)

xmin = 600.0
xmax = 0.0

idx = 0
while idx<len(tokens_attrib):
    for key,value in tokens_attrib[idx].iteritems():
        if key=="x":
            # print float(value)
            if (float(value)<xmin):
                # print "xmin = "+ value
                xmin = float(value)
            if float(value)>xmax:
                xmax = float(value)
    idx+=1

print "xmin = " + str(xmin)
# print "xmax = " + str(xmax)

xmed = (xmin+xmax)/2
# print xmed

nmin = 600.0
xmin2 = 0

idx=0
while idx<len(tokens_attrib):
    for key,value in tokens_attrib[idx].iteritems():
        if key=="x":
            if (float(value)<nmin and float(value)>=xmed):
                # print "xmin2 = "+ value
                nmin = float(value)
                xmin2 = float(value)
    idx+=1

print " xmin2 = "+ str(xmin2)
# print nmin
print len(ref)

tokens_attrib.pop(0)
print len(tokens_attrib)

# zipped = zip(my_list[0::1],second_list[0::1])
dictionary = zip(ref[0::1], tokens_attrib[0::1])

print len(dictionary)

temp_str = "manvi123 garg"
# print temp_str.split(', ')
print list(temp_str)
   

#### correct code
index = 0
flag_nw = False
italic_nw = False
reg_ex = False


while index<(len(dictionary)-1):
    # print dictionary[index]
    l = list(dictionary[index][0])
    # print l
    index2 =0
    while index2<len(l):
        if l[index2] != ".":
            refer_str.append(l[index2])
        else:
            if index2!=(len(l)-1):
                refer_str.append(l[index2])
            else:
                for key,value in dictionary[index][1].iteritems():
                    if key=="y":
                        y1=value
                    if key=="x":
                        x1=value
                for key,value in dictionary[index+1][1].iteritems():
                    if key=="y":
                        y2=value
                    if key=="x":
                        x2=value
                    if key=="italic":
                        if value=="yes":
                            italic_nw = True
                next_word = list(dictionary[index+1][0])
                str_nw = "".join(next_word)
                print "string = " +str_nw
                idx_nw=0
                if (next_word[0].isupper()):
                    flag_nw = True
                
                regex = re.compile("(\[\d{1,2}\])")
                result = re.findall(regex, str_nw)
                if len(result)>0:
                    reg_ex =True

                if (y1!=y2):
                    if reg_ex==True:
                        print "reg_ex = true"
                        reg_ex= False
                        refer_str = "".join(refer_str)
                        print refer_str
                        Reference.append(refer_str)
                        refer_str = []
                        # break
                    else:
                        if (flag_nw==True and italic_nw==False):
                            print "next word is upper and not italic \n"
                            # print str(x1) + "  and " + str(x2)
                            refer_str = "".join(refer_str)
                            print refer_str
                            Reference.append(refer_str)
                            refer_str = []
                            flag_nw=False
                            italic_nw= False
                            break   
                        else:
                            # print "same ref continued.. "
                            # print flag_nw 
                            # print italic_nw
                            refer_str.append(l[index2])
                            flag_nw = False

                else:
                    # print "same ref continued.. "
                    refer_str.append(l[index2])
                    flag_nw = False
        index2+=1
    try:
        refer_str.append(" ")
    except :
        print "refer_str is not a list anymore. It is a string now."
    index+=1      


print "\n\n\n"

for i in Reference:
    print i
    print "\n"

                    

    
