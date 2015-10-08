__author__ = 'ManviG'

import xml.etree.ElementTree as ET
import re
import os
import string
import sys
import types
#import nltk.data
#from nltk.tokenize import sent_tokenize
#from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

tree = ET.parse('/users/user/Desktop/SNLP/xml_files/elsevier2.xml')
root = tree.getroot()

import unicodedata

def binary(x):
    if x == "yes":
        return "1"
    return "0"

flag = False
reg_ex = True

Reference = []

for pages in root.findall('PAGE'):
    texts = pages.findall('TEXT')
    for i in range(len(texts)):

        tokens = texts[i].findall('TOKEN')
        if flag==False:

            for j in range(len(tokens)):
                if type(tokens[j].text) is unicode:
                    word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
                else:
                    word = tokens[j].text
                    if isinstance(word, types.NoneType):
                        print " word type is NoneType"
                        continue
                if(len(word.replace(' ',''))>0):
                    if ((word=="REFERENCES" or word=="References") and binary(tokens[j].attrib['bold'])):
                        print word + " now that's it"
                        flag = True
                        first_text = True
                        continue
        else:
            cur_x = texts[i].attrib['x']
            cur_y = texts[i].attrib['y']
            cur_size = float(tokens[0].attrib['font-size'])
            cur_font = tokens[0].attrib['font-name']
            cur_font = cur_font.lower()
            cur_bold = tokens[0].attrib['bold']
            cur_italic = tokens[0].attrib['italic']
            if first_text:
                start_ref = cur_x
                idx = 0
                Reference.append("")
                first_height = float(texts[i+1].attrib['y']) - float(cur_y)
                first_size = float(tokens[0].attrib['font-size'])
                first_font = tokens[0].attrib['font-name'].lower()
                first_lower = first_font.lower()
                first_bold = tokens[0].attrib['bold']
                first_italic = tokens[0].attrib['italic']
                first_text = False


            else:
                if (float(cur_y) < float(prev_y)):
                    if cur_size < first_size - 0.1 or cur_size > first_size + 0.1 or cur_font != first_font or cur_bold != first_bold or cur_italic != first_italic:
                        #print str(cur_size) + " " + cur_font + " " + cur_bold + " " + cur_italic
                        #print str(first_size) + " " + first_font + " " + first_bold + " " + first_italic
                        print "a"
                        continue
                    k = i + 1
                    while(True):
                        if k >= len(texts):
                            start_ref = cur_x
                            break
                        next_x = texts[k].attrib['x']
                        if(float(next_x) > float(cur_x) + 0.1):
                            start_ref = cur_x
                            idx = idx + 1
                            Reference.append("")
                            break
                        if(float(next_x) < float(cur_x) - 0.1):
                            start_ref = next_x
                            break
                        k = k + 1
                else:
                    if float(cur_y) - float(prev_y) > 3 * first_height:
                        print "b"
                        continue

                    if (float(cur_x) < float(start_ref) + 0.1 ):
                        idx = idx + 1
                        Reference.append("")

            prev_x = cur_x
            prev_y = cur_y


            for j in range(len(tokens)):
                if type(tokens[j].text) is unicode:
                    word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
                else:
                    word = tokens[j].text
                    if isinstance(word, types.NoneType):
                        print " word type is NoneType"
                        continue
                if(len(word.replace(' ',''))>0):
                    Reference[idx] += word

for refs in Reference:
    print refs
    print
    print

def search_name_year(Reference,name,year):
    name = name.replace(" ","")
    for refs in Reference:
        #print refs
        #print name
        #print year
        if name in refs and year in refs:
            print refs
            print
            print

def search_doublename(Reference,name1,name2,year):
    name1 = name1.replace(" ","")
    name2 = name2.replace(" ","")
    for refs in Reference:
        if name1 in refs and name2 in refs and year in refs:
            print refs
            print
            print
citations_no = 0

flag = False

for pages in root.findall('PAGE'):
    if flag==True:
        break
    texts = pages.findall('TEXT')
    for i  in range(len(texts)):
        line = ""
        tokens = texts[i].findall('TOKEN')
        if flag==True:
            break
        for j in range(len(tokens)):
            if type(tokens[j].text) is unicode:
                word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
            else:
                word = tokens[j].text
                if isinstance(word, types.NoneType):
                    continue
                if(len(word)>0):
                    if ((word=="REFERENCES" or word=="References") and binary(tokens[j].attrib['bold'])):
                        flag = True
                        break
                    word += " "
                    line += word

        regex = re.compile("([A-Z][a-zA-Z]* et al[.] \[(\d{1,3})\])")
        result = re.findall(regex, line)
        if len(result) > 0:
            for a in result:
                citations_no += 1
                print a[0]
                line = line.replace(a[0],'CITATION')
                print line
                print Reference[int(a[1])-1]
                print

        regex = re.compile("([A-Z][a-zA-Z]* \[(\d{2})\])")
        result = re.findall(regex, line)
        if len(result) > 0:
            for a in result:
                citations_no += 1
                print a[0]
                line = line.replace(a[0],'CITATION')
                print line
                print Reference[int(a[1])-1]
                print

        regex = re.compile("([A-Z][a-zA-Z]* et al[.][ ]*\[(\d{1})\])")
        result = re.findall(regex, line)
        if len(result) > 0:
            for a in result:
                citations_no += 1
                print a[0]
                line = line.replace(a[0],'CITATION')
                print line
                print Reference[int(a[1])-1]
                print

        regex = re.compile("(([A-Z][a-zA-Z]*) et al[.][,] (\d{4}))")
        result = re.findall(regex, line)
        if len(result) > 0:
            for a in result:
                citations_no += 1
                print a[0]
                print a[1]
                print a[2]
                print line
                line = line.replace(a[0],'CITATION')
                search_name_year(Reference,a[1],a[2])


        regex = re.compile("(([A-Z][a-zA-Z]*) and ([A-Z][a-zA-Z]*) \((\d{4})\))")
        result = re.findall(regex, line)
        if len(result) > 0:
                for a in result:
                    citations_no += 1
                    print a[0]
                    print line
                    line = line.replace(a[0],'CITATION')
                    search_doublename(Reference,a[1],a[2],a[3])


        regex = re.compile("(([A-Z][a-zA-Z]*) and ([A-Z][a-zA-Z]*)[,] (\d{4}))")
        result = re.findall(regex, line)
        if len(result) > 0:
                for a in result:
                    citations_no += 1
                    print a[0]
                    print line
                    line = line.replace(a[0],'CITATION')
                    search_doublename(Reference,a[1],a[2],a[3])

        regex = re.compile("(([A-Z][a-zA-Z]*)[,] (\d{4}))")
        result = re.findall(regex, line)
        if len(result) > 0:
            for a in result:
                citations_no += 1
                print a[0]
                print line
                line = line.replace(a[0],'CITATION')
                search_name_year(Reference,a[1],a[2])

        regex = re.compile("(([A-Z][a-zA-Z]*) (\d{4}))")
        result = re.findall(regex, line)
        if len(result) > 0:
            for a in result:
                citations_no += 1
                print a[0]
                print line
                line = line.replace(a[0],'CITATION')
                search_name_year(Reference,a[1],a[2])

        regex = re.compile("(([A-Z][a-zA-Z]*) \((\d{4}[a-z]*)\))")
        result = re.findall(regex, line)
        if len(result) > 0:
            for a in result:
                citations_no += 1
                print a[0]
                print line
                line = line.replace(a[0],'CITATION')
                search_name_year(Reference,a[1],a[2])

        regex = re.compile("(([A-Z][a-zA-Z]*) et al[.], (\d{4}[a-z]))")
        result = re.findall(regex, line)
        if len(result) > 0:
            for a in result:
                citations_no += 1
                print a[0]
                print line
                line = line.replace(a[0],'CITATION')
                search_name_year(Reference,a[1],a[2])

        regex = re.compile("(.*?\((.*?)\))")
        result = re.findall(regex, line)
        if len(result) > 0:
                for a in result:
                    citations_no += 1
                    temp = a[0]
                    regex1 = re.compile("\d{4}$")
                    cits = a[1].split(';')
                    for citation in cits:
                        citation = citation.replace(" ","")
                        if regex1.match(citation):
                            print citation
                            #print "a"
                            print line
                            temp = temp.replace(citation,'CITATION')
                            #print Reference[int(citation)-1]
                            print
                line = line.replace(a[0],temp)

        regex = re.compile("(.*?\[(.*?)\])")
        result = re.findall(regex, line)
        if len(result) > 0:
                for a in result:
                    citations_no += 1
                    temp = a[0]
                    regex1 = re.compile("\d{1,3}$")
                    cits = a[1].split(',')
                    #print cits
                    #print "b"
                    for citation in cits:
                        citation = citation.replace(" ","")
                        if regex1.match(citation):
                            print citation
                            #print "a"
                            print line
                            temp = temp.replace(citation,'CITATION')
                            print Reference[int(citation)-1]
                            print
                line = line.replace(a[0],temp)

        regex = re.compile("(([A-Z][a-zA-Z]*) et al[.], (\d{4}[a-z]))")
        result = re.findall(regex, line)
        if len(result) > 0:
            for a in result:
                citations_no += 1
                print a[0]
                print line
                line = line.replace(a[0],'CITATION')
                search_name_year(Reference,a[1],a[2])