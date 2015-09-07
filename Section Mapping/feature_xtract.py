__author__ = 'blumonkey'

import xml.etree.ElementTree as ET

files =["test3.xml"]

# "Adjunct or Alternative to Citation Counting.xml",
# "CIKM11-Yan-Citation-Count-Prediction.xml",
# "different_pdf_tools.xml",
# "Some results on the function andquality of citations.xml",
# "staticrank.xml",
# "summary_citation_context_works.xml",

import unicodedata

def binary(x):
    if x == "yes":
        return "1"
    return "0"


def caps(y):
    x=y.strip()
    parts=x.split('.',2)
    if x.islower():
        return "0"
    elif x.isupper():
        return "1"
    elif x.isdigit():
        return "2"
    elif x[:-1].isdigit() or (parts[0].isdigit() and parts[1].isdigit()):
        return "3"
    elif x[1:].islower() and x[0].isupper():
        return "4"
    else:
        return "5"
# print caps("11.")
# print caps("3.3")

# exit()

for ff in files:
    tree = ET.parse('/home/blumonkey/Acads/NLP/pdfs/'+ff)
    root = tree.getroot()

    max_fs = 0
    for pages in root.findall('PAGE'):
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                if(float(token.attrib['font-size'])>max_fs):
                    max_fs=float(token.attrib['font-size'])

    print max_fs

    f = open('temp.txt','w')
    f.write("0\t0\t0\t0\t0\t0\n")

    for pages in root.findall('PAGE'):
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                if type(token.text) is unicode:
                    word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                else:
                    word = token.text
                if(len(word.replace(' ',''))>0):
                    f.write((word.replace(' ','')+"\t").encode("utf-8"))
                    f.write((binary(token.attrib['bold'])+"\t").encode("utf-8"))
                    f.write((binary(token.attrib['italic'])+"\t").encode("utf-8"))
                    f.write((str(round(float(token.attrib['font-size'])/(max_fs),2))+"\t").encode("utf-8"))
                    f.write((caps(token.text.encode("utf-8").replace(' ','')))+"\t")
                    f.write(("0\n").encode("utf-8"))
            f.write("0\t0\t0\t0\t0\t0\n\n")

    from subprocess import call

    f1 = open(ff+'.txt','w')

    call(["unidecode","temp.txt"],stdout=f1)
    f.close()

    call(["rm","temp.txt"])