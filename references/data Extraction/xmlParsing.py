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

tree = ET.parse('/home/manvi/Documents/acads/SNLP/Project/OCR/pdfs/acl2.xml')
root = tree.getroot()

f = open("/home/manvi/Documents/acads/SNLP/Project/OCR/references/test_file.txt", 'a')


import unicodedata


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

def binary(x):
    if x == "yes":
        return "1"
    return "0"

flag = False
reg_ex = True

Reference = []

for pages in root.findall('PAGE'):
    texts = pages.findall('TEXT')
    for i  in range(len(texts)):
        
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
				Reference.append(" ")
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
							Reference.append(" ")
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
						Reference.append(" ")
                	
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
					print word
					f.write((word.replace(' ','')+"\t").encode("utf-8"))
					f.write(((binary(tokens[j].attrib['bold'])).replace(' ','')+"\t").encode("utf-8"))
					f.write(((binary(tokens[j].attrib['italic'])).replace(' ','')+"\t").encode("utf-8"))
					f.write(((str(round(float(tokens[j].attrib['font-size'])/(max_fs),2))).replace(' ','')+"\t").encode("utf-8"))
					f.write((caps(word.encode("utf-8").replace(' ','')))+"\t\n")


for refs in Reference:
	print refs
	print
	print