import re
import sys
import os
import string

cues= open('insignificant_cues','a+')
count = 0
add = []
directoryList = "crawled_papers/"



# my_list = []

c=0
os.mkdir("citation_context_parsed",0755)

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
	print result
		   


for root,dirs,files in os.walk(directoryList):
	for file in files:
		text_file = open(directoryList+file,"r")
		output = open("citation_context_parsed/"+file,"w")
		for line in text_file:
			#regex = re.compile("(.*? and .*? \[\d{2}\])")
			# print line
			line = line.split(' ',1)
			if len(line) >1:
				line = line[1]
			else : 
				line = line[0]
			# print line
			# exit()
			# c+=1;
			# if c>30:
			# 	exit()
			count1 = 1
			
			# regex = re.compile("([A-Z][a-zA-Z]* and [A-Z][a-zA-Z]* \[\d{1,2}\])")
			# result = re.findall(regex, line)
			# # print result
			# if len(result) > 0: 
			# 	for a in result:
			# 		print a
			# 		for i in my_list:
			# 			print i
			# 			if a in i:
			# 				print "yayy"
			# 		line = line.replace(a,'CITATION')
			# 		# print line
			# 		count1 += 1

			# regex = re.compile("([A-Z][a-zA-Z]* et al[.] \[\d{2,4}\])")
			# result = re.findall(regex, line)
			# if len(result) > 0: 
			# 	for a in result:
			# 		print a
			# 		for i in my_list:
			# 			if a in i:
			# 				print "yayy"
			# 		line = line.replace(a,'CITATION')
			# 		count1 += 1			

			# regex = re.compile("([A-Z][a-zA-Z]* \[\d{2}\])")
			# result = re.findall(regex, line)
			# if len(result) > 0: 
			# 	for a in result:
			# 		print a
			# 		for i in my_list:
			# 			if a in i:
			# 				print "yayy"
			# 		line = line.replace(a,'CITATION')
			# 		count1 += 1
			
			# regex = re.compile("([A-Z][a-zA-Z]* et al[.][ ]*\[\d{1}\])")
			# result = re.findall(regex, line)
			# if len(result) > 0: 
			# 	for a in result:
			# 		print a
			# 		for i in my_list:
			# 			if a in i:
			# 				print "yayy"
			# 		line = line.replace(a,'CITATION')
			# 		count1 += 1
			
			# regex = re.compile("([A-Z][a-zA-Z]* et al[.][,] \d{4})")
			# result = re.findall(regex, line)
			# if len(result) > 0: 
			# 	for a in result:
			# 		print a
			# 		for i in my_list:
			# 			if a in i:
			# 				print "yayy"
			# 		line = line.replace(a,'CITATION')
			# 		count1 += 1

			# regex = re.compile("([A-Z][a-zA-Z]* and [A-Z][a-zA-Z]* \(\d{4}\))")
			# result = re.findall(regex, line)
			# if len(result) > 0: 
			# 	for a in result:
			# 		print a
			# 		for i in my_list:
			# 			if a in i:
			# 				print "yayy"
			# 		line = line.replace(a,'CITATION')
			# 		# print line
			# 		count1 += 1
			
			# regex = re.compile("([A-Z][a-zA-Z]* and [A-Z][a-zA-Z]*[,] \d{4})")
			# result = re.findall(regex, line)
			# if len(result) > 0: 
			# 	for a in result:
			# 		print a
			# 		for i in my_list:
			# 			if a in i:
			# 				print "yayy"
			# 		line = line.replace(a,'CITATION')
			# 		# print line
			# 		count1 += 1			
		
			# regex = re.compile("([A-Z][a-zA-Z]*[,] \d{4})")
			# result = re.findall(regex, line)
			# if len(result) > 0: 
			# 	for a in result:
			# 		print a
			# 		for i in my_list:
			# 			if a in i:
			# 				print "yayy"
			# 		line = line.replace(a,'CITATION')
			# 		# print line
			# 		count1 += 1			
			
			# regex = re.compile("([A-Z][a-zA-Z]* \(\d{4}[a-z]*\))")
			# result = re.findall(regex, line)
			# if len(result) > 0: 
			# 	for a in result:
			# 		# print a
			# 		for i in my_list:
			# 			if a in i:
			# 				print "yayy"
			# 		line = line.replace(a,'CITATION')
			# 		# print line
			# 		count1 += 1
			
			
			# regex = re.compile(".*?\((.*?)\)")
			# result = re.findall(regex, line)
			# if len(result) > 0: 
			# 	for a in result:
			# 		temp = a
			# 		result1 = re.findall(r'\d{4}', a)
			# 		# print result1
			# 		print len(result1)
			# 		if len(result1) > 0:
			# 			line = line.replace('('+a+')',a)
			# 			cits = a.split(';')
			# 			print cits
			# 			for citation in cits:
			# 				print citation
			# 				temp = temp.replace(citation,'CITATION')
			# 				count1 = count1 + 1
			# 			temp = temp.replace(';',', ')
			# 			print temp
			# 			print line
			# 			line = line.replace(a,temp)
			# 			print line

			
		
			regex = re.compile(".*?\[(.*?)\]")
			result = re.findall(regex, line)
			if len(result) > 0: 
				for a in result:
					temp = a
					result1 = re.findall(r'\d{1,3}', a)
					if len(result1) > 0:
						line = line.replace('('+a+')',a)
						cits = a.split(',')
						for citation in cits:
							print "citation = "+citation
							length = len(citation)
							for i in my_list:
								temp_exp = i[0] + citation + i[length+1]
								idx=0
								temp_exp2 = ""
								while (idx <= (len(citation)+1)):
									temp_exp2 =temp_exp2+ i[idx]
									idx+=1
								if (temp_exp2==temp_exp):
									print i + "\n\n"
							temp = temp.replace(citation,'CITATION')
							count1 += 1		
				line = line.replace(a,temp)

			# regex = re.compile("([A-Z][a-zA-Z]* et al[.], \d{4}[a-z])")
			# result = re.findall(regex, line)
			# if len(result) > 0: 
			# 	for a in result:
			# 		print a
			# 		line = line.replace(a,'CITATION')
			# 		count1 += 1
			
			output.write(line)


