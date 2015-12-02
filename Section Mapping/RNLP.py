
from __future__ import division
import xml.etree.ElementTree as ET
import unicodedata
import operator
import roman
import math



files = ["chi1.xml"]

# ,"acl2.xml","acm_journal1.xml","acm_journal2.xml","ACM-sig1.xml","ACM-sig2.xml","ACM-sig3.xml","chi1.xml","chi2.xml"
# ,"ieee1.xml","ieee2.xml","ieee3.xml"
# ,"ieee1_journal1.xml","ieee2_journal1.xml","Springer1.xml","Springer2.xml"
# ,"arxiv1.xml","arxiv2.xml"

# "2010_SAC_Word_Template.xml"
# "acl.xml"
# "coli_a_00209.xml"
# "coli_a_00210.xml"
# "fftw-paper-ieee.xml"
# "Rod99.xml"
# "sping3.xml"
# "spring2.xml"
# "test1.xml"
# "Volatility.xml"
# "acl1.xml"
# "acl2.xml"
# "summarization.xml"
# "CIKM11-Yan-Citation-Count-Prediction.xml"
# "different_pdf_tools.xml"




def binary(x):
    if x == "yes":
        return "1"
    return "0"


def token_features(y):
    x=y.strip()
    parts=x.split('.')
    if(x=="Abstract" or x== "ABSTRACT" or x=="Acknowledgement" or x== "ACKNOWLEDGEMENT" or x=="References" or x== "Reference" or x == "REFERENCE" or x=="REFERENCES" or x=="Acknowledgements" or x== "ACKNOWLEDGEMENTs"):
        return "6"
    if(x=="$$$"):
        return "5"
    if x=="Table" or x=="TABLE" or x=="Figure" or x=="FIGURE" or x=="Fig.":
        return "0"
    p_len = len(parts)
    if(p_len==1):
        if(x.isdigit() and 1<=int(x)<=20):
            return "1"
    if(p_len==2 or p_len==3):
        if(parts[0].isdigit() and 1<=int(parts[0])<=20):
            if(parts[1]=='' or (parts[1].isdigit() and int(parts[1])<=20)):
                if(p_len==2):
                    return "1"
                if(parts[1].isdigit() and int(parts[1])<=20 and parts[2]==''):
                    return "1"
    if(p_len==1 or (p_len==2 and parts[1]=='')):
        try:
            val = roman.fromRoman(parts[0].upper())
            if(val<=20):
                return "1"
        except:
            None
        if((len(parts[0])==1 and 'A'<=parts[0]<='Z') or (len(parts[0])==3 and parts[0][0]=='(' and parts[0][2]==')' and parts[0][1].isalpha() and parts[0][1].isupper()) or (len(parts[0])==2 and parts[0][1]==')' and parts[0][0].isalpha() and parts[0][0].isupper())):
            if(p_len==1 or (p_len==2 and parts[1]=='')):
                return "1"
    if x[0].isupper():
        return "2"
    if (not(parts[0].isalpha() or parts[0].isdigit())):
        return "3"
    return "4"


pdfcount =0
for ff in files:
    tree = ET.parse('/home/blumonkey/PycharmProjects/NLP/'+ff)
    root = tree.getroot()

    max_fs = 0
    p_yloc = None
    y_diff={}
    fsizes = {}

    for pages in root.findall('PAGE'):
        pre_y=0
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                try:
                    # print(token.attrib)
                    fsizes[round(abs(float(token.attrib['font-size'])))]=fsizes.get(round(abs(float(token.attrib['font-size']))),0)+1
                    if(p_yloc is None):
                        p_yloc=float(token.attrib['y'])
                    if(float(token.attrib['font-size'])>max_fs):
                        max_fs=float(token.attrib['font-size'])
                    y_diff[round(abs(float(token.attrib['y'])-pre_y))]=y_diff.get(round(abs(float(token.attrib['y'])-pre_y)),0)+1
                    pre_y=float(token.attrib['y'])
                except:
                    print "Oops"
    max_fs = 0
    for shit in fsizes.keys():
        # print fsizes[shit]
        if(max_fs == 0):
            max_fs = shit
            continue
        if(fsizes[shit]>fsizes[max_fs]):
            max_fs=shit
    print max_fs
    print("fsizes!!!")
    print fsizes

    # exit(0)
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

    limit = max([x[0] for x in new_l])+1
    print(limit)
    # exit(0)



    xroot = ET.Element("Document")
    chunk = ET.SubElement(xroot, "chunk")
    for pages in root.findall('PAGE'):
        for texts in pages.findall('TEXT'):
            for token in texts.findall('TOKEN'):
                if type(token.text) is unicode:
                    word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                else:
                    word = token.text
                if(word and len(word.replace(' ',''))>0):
                    if( abs(float(token.attrib['y'])-p_yloc)>=limit):
                        chunk = ET.SubElement(xroot, "chunk")
                    p_yloc = float(token.attrib['y'])
                    ET.SubElement(chunk, "token", font_size=token.attrib['font-size'], bold=token.attrib['bold']).text = word

    tree = ET.ElementTree(xroot)
    tree.write(ff+"_res.xml")
    # print(tree._root)

    newxroot = ET.Element("Document")
    chunk = ET.SubElement(newxroot, "chunk")


    count =0
    p_fsize = None

    root = tree.getroot()

    for chunks in root.findall('chunk'):
        chunk = ET.SubElement(newxroot, "chunk")
        count =0
        stat = 0
        if(len(chunks)>20):stat =1
        for token in chunks.findall('token'):
            # print(token.text + " " + token.attrib["font_size"])
            if(count < 15 and p_fsize is not None and float(token.attrib["font_size"]) < p_fsize and stat==1 ):
                chunk = ET.SubElement(newxroot, "chunk")
                ET.SubElement(chunk, "token", font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
            else:
                ET.SubElement(chunk, "token", font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
                count  = count + 1
            p_fsize = float(token.attrib['font_size'])

    tree = ET.ElementTree(newxroot)
    tree.write(ff+"_fin.xml")

    f = open(ff.split('.')[0]+'_out_new.txt','w')

    newxroot = tree.getroot()

    for achunk in newxroot.findall('chunk'):
        boldness = 0
        fsize = 0
        tcount = 0
        bool = None
        tokens = achunk.findall('token')
        if(len(tokens)==0):
            continue
        elif(len(tokens) ==1):
            tok1 = '$$$'
            tok2 = tokens[0].text
            # bool = tok2
        else:
            tok1 = tokens[0].text
            tok2 = tokens[1].text
            # bool = tok1
        tcount = len(tokens)
        for t in tokens:
            if(t.attrib['bold']=="yes"):
                boldness=boldness+1
            fsize = fsize + float(t.attrib['font_size'])
        boldness = round(boldness/tcount,2)
        fsize = (fsize/tcount)/max_fs
        tcount = math.floor(tcount / 16)
        print (tok1+"\t"+tok2+"\t"+str(int(tcount))+"\t"+str(boldness)+"\t"+str(round(fsize,2))+"\t"+token_features(tok1)+"\t"+token_features(tok2))
        f.write(tok1+"\t"+tok2+"\t"+str(int(tcount))+"\t"+str(boldness)+"\t"+str(round(fsize,2))+"\t"+token_features(tok1)+"\t"+token_features(tok2)+"\t0\n")