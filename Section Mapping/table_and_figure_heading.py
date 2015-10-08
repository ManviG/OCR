from __future__ import division
import xml.etree.ElementTree as ET
import unicodedata
import operator
import re
import roman

from xml.sax.saxutils import escape


files =["acl2.xml"]


def binary(x):
    if x == "yes":
        return "1"
    return "0"


def tb_heading_features(y):
    x=y.strip()
    parts=x.split('.',2)
    pattern = re.compile('[1-9][0-9]*(\.)?([1-9][0-9]*(\.([1-9][0-9]*)?)?)?')
    m = pattern.match(x)
    if x=="Table" or x=="TABLE" or x=="Figure" or x=="FIGURE" or x=="Fig." or x=="FIG.":
        return "0"
    if m and m.span()==(0, len(x)):
        return "1"
    try:
        roman.fromRoman(parts[0].upper())
        return "1"
    except:
        if x[0].isupper():
            return "2"
        return "3"



for ff in files:
    print ff
    tree = ET.parse('/home/blumonkey/Acads/NLP/test_pdfs/'+ff)
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
                    print(token.attrib)
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
        print fsizes[shit]
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

    limit = max([x[0] for x in new_l])+2
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
                    ET.SubElement(chunk, "token", y=token.attrib['y'], font_size=token.attrib['font-size'], bold=token.attrib['bold']).text = word

    tree = ET.ElementTree(xroot)
    #tree.write("/home/kumar_ayush/PycharmProjects/NLP/mid_train/test/text/"+ff+"_res.xml")
    print(tree._root)

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
            print(token.text + " " + token.attrib["font_size"])
            if(count < 15 and p_fsize is not None and float(token.attrib["font_size"]) < p_fsize and stat==1 ):
                chunk = ET.SubElement(newxroot, "chunk")
                ET.SubElement(chunk, "token",  y=token.attrib['y'], font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
            else:
                ET.SubElement(chunk, "token",  y=token.attrib['y'], font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
                count  = count + 1
            p_fsize = float(token.attrib['font_size'])

    tree = ET.ElementTree(newxroot)
    #tree.write("/home/kumar_ayush/PycharmProjects/NLP/mid_train/test/text/"+ff+"_fin.xml")


    ##############################
    new_newxroot = ET.Element("Document")
    chunk = ET.SubElement(new_newxroot, "chunk")

    root = tree.getroot()

    for chunks in root.findall('chunk'):
        chunk = ET.SubElement(new_newxroot, "chunk")

        tokens = chunks.findall('token')
        print tokens
        if(len(tokens)>0 and ((tokens[0].text == 'Table' or tokens[0].text == 'TABLE') and tokens[0].attrib['bold'] == 'yes')):
            stat =1
        else :
            stat =0
        prev_bold =1
        for token in chunks.findall('token'):
           if(stat==1 and prev_bold ==1 and token.attrib['bold']== 'no' ):
                chunk = ET.SubElement(new_newxroot, "chunk")
                ET.SubElement(chunk, "token",  y=token.attrib['y'], font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
           else :
                ET.SubElement(chunk, "token",  y=token.attrib['y'], font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text

    tree = ET.ElementTree(new_newxroot)
    tree.write("/home/kumar_ayush/PycharmProjects/NLP/mid_train/test/text/"+ff+"_fin_fin.xml")

    ##############################


    f = open("/home/kumar_ayush/PycharmProjects/NLP/mid_train/test/text/"+ff+'_out.txt','w')

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
            bool = tok2
        else:
            tok1 = tokens[0].text
            tok2 = tokens[1].text
            bool = tok1
        tcount = len(tokens)
        for t in tokens:
            if(t.attrib['bold']=="yes"):
                boldness=boldness+1
            fsize = fsize + float(t.attrib['font_size'])
        boldness = boldness/tcount
        fsize = (fsize/tcount)/max_fs
        y_pos = tokens[0].attrib['y']
        print (tok1+"\t\t\t"+tok2+"\t\t\t"+str(tcount)+"\t\t\t"+str(boldness)+"\t\t\t"+str(round(fsize,2))+"\t\t\t"+tb_heading_features(bool))
        f.write(tok1+"\t\t\t"+tok2+"\t\t\t"+str(round(fsize,2))+"\t\t\t"+str(y_pos)+"\t\t\t"+0+"\n")