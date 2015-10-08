__author__ = 'sidhartha4'

import xml.etree.ElementTree as ET

import re
import unicodedata



#files =["elsevier1.xml","elsevier2.xml","ieee1.xml","ieee2.xml","ieee3.xml","ieee_journal1.xml","ieee_journal2.xml","Springer2.xml"]
files=["elsevier1.xml"]

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




for ff in files:
    print ff
    tree = ET.parse('/home/kumar_ayush/PycharmProjects/NLP/mid_train/test/pdf_and_xml/'+ff)
    root = tree.getroot()

    f = open("/home/kumar_ayush/PycharmProjects/NLP/mid_train/test/url/"+ff+'.txt','w')
    f.write("0\t\t\t\t\t\t0\n")

    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


    for pages in root.findall('PAGE'):
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                if type(token.text) is unicode:
                    word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                else:
                    word = token.text
                    print word


                if(word and len(word.replace(' ',''))>0):
                    f.write((word.replace(' ','')+"\t\t\t\t\t\t").encode("utf-8"))
                    x = word.strip('()')
                    if(bool(pattern.match(x.replace(' ','')))):
                        f.write(("1\n").encode("utf-8"))
                    else:
                        f.write(("0\n").encode("utf-8"))

            f.write("0\t\t\t\t\t\t0\n\n")


#from subprocess import call
#f1 = open('config.txt','w')
#call(["unidecode","temp2.txt"],stdout=f1)
#f.close()
#call(["rm","temp2.txt"])