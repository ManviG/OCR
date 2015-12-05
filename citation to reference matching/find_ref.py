__author__ = 'ManviG'

import xml.etree.ElementTree as ET
import re
import os
import string
import sys
import nltk.data
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

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
print "xmax = " + str(xmax)

xmed = (xmin+xmax)/2
print xmed

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
   

index = 0
flag_nw = False
italic_nw = False
reg_ex = False
is_ref_numbered = False

while index<(len(dictionary)-1):
    l = list(dictionary[index][0])
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
                idx_nw=0
                if (next_word[0].isupper()):
                    flag_nw = True
                
                regex = re.compile("(\[\d{1,2}\])")
                result = re.findall(regex, str_nw)
                if len(result)>0:
                    reg_ex =True
                    is_ref_numbered = True

                if ((float(y2)-float(y1))>1):
                    if reg_ex==True:
                        reg_ex= False
                        refer_str = "".join(refer_str)
                        Reference.append(refer_str)
                        refer_str = []
                    else:
                        if is_ref_numbered==True:
                            refer_str.append(l[index2])
                            flag_nw = False
                            italic_nw = False
                        elif (flag_nw==True and italic_nw==False):
                            if (float(x2)<xmed):
                                if (float(x2)-xmin>1) :
                                    refer_str.append(l[index2])
                                    flag_nw = False
                                    italic_nw = False
                                else:
                                    refer_str = "".join(refer_str)
                                    Reference.append(refer_str)
                                    refer_str = []
                                    flag_nw=False
                                    italic_nw= False
                            else:
                                if (float(x2)-xmin2>1):
                                    refer_str.append(l[index2])
                                    flag_nw = False
                                    italic_nw = False
                                else:
                                    refer_str = "".join(refer_str)
                                    Reference.append(refer_str)
                                    refer_str = []
                                    flag_nw=False
                                    italic_nw= False
                        else:
                            refer_str.append(l[index2])
                            flag_nw = False
                            italic_nw = False
                elif((float(y1)-float(y2))>50):
                    print "\n new Reference in next col"
                    print "current word = " + str(x1) + "  next_word = "+ str(x2)
                    print "string = " +str_nw
                    refer_str = "".join(refer_str)
                    Reference.append(refer_str)
                    refer_str = []
                    flag_nw=False
                    italic_nw= False
                else:
                    refer_str.append(l[index2])
                    flag_nw = False
                    italic_nw = False
        index2+=1
    try:
        refer_str.append(" ")
    except :
        print "refer_str is not a list anymore. It is a string now."
    index+=1      


# print "\n\n\n"

# for i in Reference:
#     print i
#     print "\n"


References = [[]]

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

punkt_param = PunktParameters()
punkt_param.abbrev_types = set(['pp','Eds','eds','Vol','vol','op','cit', 'proc','syst','inf','knowl','trans','comput',
                                  'res','oper','commun', 'artif','intell','assoc'])
sent_detector = PunktSentenceTokenizer(punkt_param)

ref_list = " ".join(ref)

line = sent_detector.tokenize(ref_list.strip())


author_name= []
year_of_pub= []
paper_name=[]
journal_name=[]

year_found = False
req_idx = 1
for i in Reference:
    line = sent_detector.tokenize(i.strip())
    line2 = sent_detector.sentences_from_text(i.strip() )
    References.append(line)
    line3 = [x for x in line if x != "."]
    if len(line3)==4:
        j=0        
        author_name.append(line3[j])
        year_of_pub.append(line3[j+1])
        paper_name.append(line3[j+2])
        journal_name.append(line3[j+3])
    else:
        name_str = []
        regex = re.compile("(\d{4})")
        idx=0
        req_idx = 1
        while(idx<len(line3)):
            result = re.findall(regex,line3[idx])
            if len(result)>0:
                # print line3[idx]
                year_found=True
                req_idx = idx
                break
            idx+=1
        k=0
        while k<req_idx:
            # print line3[k]
            name_str.append(line3[k])
            k+=1
        name_str = " ".join(name_str)
        author_name.append(name_str) 
        year_of_pub.append(line3[req_idx])
        paper_name.append(line3[req_idx+1])
        journal_name.append(line3[req_idx+2])


print len(author_name)
print len(year_of_pub)
print len(paper_name)
print len(journal_name)


tokenized_dict = zip(author_name[0:1], year_of_pub[0:1], paper_name[0:1],journal_name[0:1])


# i = 0 
# while(i<len(author_name)):
#     print author_name[i]
#     print "\n"
#     i+=1 

# i = 0 
# while(i<len(year_of_pub)):
#     print year_of_pub[i]
#     print "\n"
#     i+=1            
    
# i = 0 
# while(i<len(paper_name)):
#     print paper_name[i]
#     print "\n"
#     i+=1 

# i = 0 
# while(i<len(journal_name)):
#     print journal_name[i]
#     print "\n"
#     i+=1