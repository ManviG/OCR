__author__ = 'kumar_ayush'

import xml.etree.ElementTree as ET

xml_list = ['sigdial_crosslinguistic_camera_ready']

files =["elsevier1.xml","elsevier2.xml","ieee1.xml","ieee2.xml","ieee3.xml","ieee_journal1.xml","ieee_journal2.xml","Springer2.xml"]


for i in files:
    print i
    tree = ET.parse('/home/kumar_ayush/PycharmProjects/NLP/mid_train/test/pdf_and_xml/'+i)
    root = tree.getroot()

    import unicodedata

    def binary(x):
        if x == "yes":
            return "1"
        return "0"

    max_fs = 0
    for pages in root.findall('PAGE'):
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                #print token.text
                if(token.text and float(token.attrib['font-size'])>max_fs):
                    max_fs=float(token.attrib['font-size'])

    print max_fs

    f_fn = open('/home/kumar_ayush/PycharmProjects/NLP/mid_train/test/footnote/test/'+i+'.txt','w')
    f_fn.write("0\t0\t0\t0\t0\t0\t0\t0\t0\n")

    for pages in root.findall('PAGE'):
        for texts in pages.findall('TEXT'):
            flag=1
            for token in texts.findall('TOKEN'):
                if type(token.text) is unicode:
                    word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                else:
                    word = token.text
                if(word and len(word.replace(' ',''))>0):
                    f_fn.write((word.replace(' ','')+"\t\t\t\t\t").encode("utf-8"))
                    f_fn.write((str(round(float(token.attrib['font-size'])/(max_fs),2))+"\t").encode("utf-8"))
                    f_fn.write(((token.attrib['x'])+"\t").encode("utf-8"))
                    f_fn.write(((token.attrib['y'])+"\t").encode("utf-8"))
                    f_fn.write((binary(token.attrib['bold'])+"\t"+binary(token.attrib['italic'])+"\t").encode("utf-8"))
                    f_fn.write((caps(word.replace(' ',''))+"\t").encode("utf-8"))
                    f_fn.write((str(flag)+"\t").encode("utf-8"))
                    f_fn.write(("0\n").encode("utf-8"))
                flag=0
            f_fn.write("0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")