author = "barno"

import xml.etree.ElementTree as ET

directory = '/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/'

tree = ET.parse(directory + 'input.xml')
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

# def comma(y):
#     x = y.strip()
#     if x[len(x)-1] == ',':
#         return "1"
#     else:
#         return "0"

print "titleauthorparse"
#To find max font size and total number to textxs in the file
page = 0
max_fs = 0
tot_txt = 0
for pages in root.findall('PAGE'):
    page = page + 1
    for texts in pages.findall('TEXT'):
    	tot_txt = tot_txt + 1
        for token in texts.findall('TOKEN'):
            if token.text is None:
                continue
            if(float(token.attrib['font-size'])>max_fs):
                if type(token.text) is unicode:
                    word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                else:
                    word = token.text
                # print page
                print word + token.attrib['font-size']
                max_fs=float(token.attrib['font-size'])

f = open(directory + 'test.txt','w')
f.write("0\t0\t0\t0\t0\t0\n")

print "***"
print tot_txt
flagg=0
txt = 0;
count = 0;
for pages in root.findall('PAGE'):
    count = count +1
    if count > 2:     #Only first two pages to search
        break
    for texts in pages.findall('TEXT'):
    	txt = txt + 1;
        for token in texts.findall('TOKEN'):
            if token.text is None:
                continue
            if type(token.text) is unicode:
                word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
            else:
                word = token.text
            if(len(word.replace(' ',''))>0):
                f.write((word.replace(' ','')+"\t").encode("utf-8"))
                f.write((binary(token.attrib['bold'])+"\t").encode("utf-8")) #Bold
                f.write((str(round(float(txt)/(tot_txt),2))+"\t").encode("utf-8")) #Relative position
                f.write((str(round(float(token.attrib['font-size'])/(max_fs),2))+"\t").encode("utf-8")) #Relative size
                f.write((startCaps(token.text.encode("utf-8").replace(' ','')))+"\t")
                # f.write((comma(token.text.encode("utf-8").replace(' ','')))+"\t")
                f.write(("0\n").encode("utf-8"))
        f.write("0\t0\t0\t0\t0\t0\n\n")

f.write("00\t00\t00\t00\t00\t00\n\n")

f.close()