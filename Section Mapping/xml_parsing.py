__author__ = 'blumonkey'

import xml.etree.ElementTree as ET
import unicodedata
import operator
from xml.sax.saxutils import escape


files =["jors2012123a.xml"]

# jors2012123a.xml
# "Adjunct or Alternative to Citation Counting.xml",
# "CIKM11-Yan-Citation-Count-Prediction.xml",
# "different_pdf_tools.xml",
# "Some results on the function andquality of citations.xml",
# "staticrank.xml",
# "summary_citation_context_works.xml",


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
    p_yloc = None
    y_diff={}

    for pages in root.findall('PAGE'):
        pre_y=0
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                if(p_yloc is None):
                    p_yloc=float(token.attrib['y'])
                if(float(token.attrib['font-size'])>max_fs):
                    max_fs=float(token.attrib['font-size'])
                y_diff[round(abs(float(token.attrib['y'])-pre_y))]=y_diff.get(round(abs(float(token.attrib['y'])-pre_y)),0)+1
                pre_y=float(token.attrib['y'])

    print max_fs
    new_l = sorted(y_diff.iteritems(), key=operator.itemgetter(1), reverse=True)[:7]
    x_l = []
    print(new_l)
    for k in new_l:
        if(k[0]>6.0):
            x_l.append(k)
    new_l=x_l

    x_l=[]
    mode=new_l[0][1]
    for k in new_l:
        if(not(k[1]<=mode/2 or abs(new_l[0][0]-k[0])>=4)):
            x_l.append(k)

    new_l=x_l
    print(new_l)
    del x_l

    limit = max([x[0] for x in new_l])+2
    print(limit)
    # exit(0)
    #
    # f = open('_res.xml','w')
    # # f.write("0\t0\t0\t0\t0\t0\n")
    # f.write("<Document>\n<chunk>\n")


    xroot = ET.Element("Document")
    chunk = ET.SubElement(xroot, "chunk")
    for pages in root.findall('PAGE'):
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                if type(token.text) is unicode:
                    word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                else:
                    word = token.text
                if(len(word.replace(' ',''))>0):
                    if( abs(float(token.attrib['y'])-p_yloc)>=limit):
                        chunk = ET.SubElement(xroot, "chunk")
                    p_yloc = float(token.attrib['y'])
                    ET.SubElement(chunk, "token", font_size=token.attrib['font-size']).text = word
                    # f.write(escape("\t"+(word.replace(' ','')+"\t").encode("utf-8")))
                    # f.write(escape(("\n").encode("utf-8")))
    # f.write("</chunk>\n</Document>\n")
    # f.close()


    tree = ET.ElementTree(xroot)
    tree.write(ff+"_res.xml")
    print(tree._root)

    newxroot = ET.Element("Document")
    chunk = ET.SubElement(newxroot, "chunk")

    count =0
    p_fsize = None

    root = tree.getroot()

    for chunks in root.findall('chunk'):
        chunk = ET.SubElement(newxroot, "chunk")
        count =0

        for token in chunks.findall('token'):
            # print(token.text)
            if(count < 15 and p_fsize is not None and token.attrib["font_size"] < p_fsize ):
                chunk = ET.SubElement(newxroot, "chunk")
                ET.SubElement(chunk, "token", font_size=token.attrib['font_size']).text = token.text
            else:
                ET.SubElement(chunk, "token", font_size=token.attrib['font_size']).text = token.text
                count  = count + 1
            p_fsize = token.attrib['font_size']

    tree = ET.ElementTree(newxroot)
    tree.write(ff+"_fin.xml")







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