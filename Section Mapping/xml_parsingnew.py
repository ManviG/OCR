__author__ = 'blumonkey'

import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

files =["Adjunct or Alternative to Citation Counting.xml"]

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

    # max_fs = 0
    # p_yloc = None
    # y_diff=[]
    #
    # for pages in root.findall('PAGE'):
    #     pre_y=0
    #     for texts in pages.findall('TEXT'):
    #         for token in texts.findall('TOKEN'):
    #             if(p_yloc is None):
    #                 p_yloc=float(token.attrib['y'])
    #             if(float(token.attrib['font-size'])>max_fs):
    #              max_fs=float(token.attrib['font-size'])
    #             y_diff.append(round(abs(float(token.attrib['y'])-pre_y)))
    #             pre_y=float(token.attrib['y'])
    #
    # print max_fs
    # new_l = filter(lambda a: a != 0, y_diff)
    # print(p_yloc)
    # print(sorted(new_l))

    # exit(0)

    f = open('test2_newres.xml','w')
    # f.write("0\t0\t0\t0\t0\t0\n")
    f.write("<Document>\n<chunk>\n")

    p_fn = None
    p_fsize = None

    for pages in root.findall('PAGE'):
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                if type(token.text) is unicode:
                    word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                else:
                    word = token.text
                if(len(word.replace(' ',''))>0):
                   if( p_fsize is None or abs(float(token.attrib['font-size'])-p_fsize)>0.1):
                      f.write("</chunk>\n<chunk>\n")
                      p_fsize = token.attrib['font-size']
                      print(p_fsize)
                   p_fsize = float(token.attrib['font-size'])
                   f.write(escape("\t"+(word.replace(' ','')+"\t").encode("utf-8")))
                   f.write(escape(("\n").encode("utf-8")))
    f.write("</chunk>\n</Document>\n")
    f.close()


#(token.attrib['font-name'].lower()!=p_fn or token.attrib['font-size']!=p_fsize) and

                    # f.write((binary(token.attrib['bold'])+"\t").encode("utf-8"))
                    # f.write((binary(token.attrib['italic'])+"\t").encode("utf-8"))
                    # f.write((str(round(float(token.attrib['font-size'])/(max_fs),2))+"\t").encode("utf-8"))
                    # f.write((caps(token.text.encode("utf-8").replace(' ','')))+"\t")
                    # f.write(("0\n").encode("utf-8"))

    #
    # f.write("0\t0\t0\t0\t0\t0\n\n")
    # from subprocess import call
    #
    # f1 = open('tts.txt','w')
    #
    # call(["unidecode","temp.txt"],stdout=f1)
    # call(["rm","temp.txt"])



 #
 # if( abs(float(token.attrib['y'])-p_yloc)>14.0):
 #                        f.write("</chunk>\n<chunk>\n")
 #                        p_fn = token.attrib['font-name'].lower()
 #                        p_fsize = token.attrib['font-size']
 #                        print(p_yloc)
 #                    p_yloc = float(token.attrib['y'])
 #                    f.write(escape("\t"+(word.replace(' ','')+"\t").encode("utf-8")))
 #                    f.write(escape(("\n").encode("utf-8")))