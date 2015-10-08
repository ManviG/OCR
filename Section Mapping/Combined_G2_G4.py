
from __future__ import division
import xml.etree.ElementTree as ET
import unicodedata
import threading
import operator
import roman
import re
# List of files and the root folder for batch processing
files_list = ["acl2.xml"]
root_folder = '/home/blumonkey/Acads/NLP/test_pdfs/'

# Binary coverter for strings
def binary(x):
    if x == "yes":
        return "1"
    return "0"

# Function to classify tokens into features for CRF
def token_features(y):
    x=y.strip()
    parts=x.split('.')
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


def group4_work(tree):
    f = open(a_file.split('.')[0]+'_g4_out.txt','w')
    newxroot = tree.getroot()
    for achunk in newxroot.findall('chunk'):
        boldness = 0
        fsize = 0
        tokens = achunk.findall('token')
        if(len(tokens)==0):
            continue
        elif(len(tokens) ==1):
            tok1 = '$$$'
            tok2 = tokens[0].text
        else:
            tok1 = tokens[0].text
            tok2 = tokens[1].text
        tcount = len(tokens)
        for t in tokens:
            if(t.attrib['bold']=="yes"):
                boldness=boldness+1
            fsize = fsize + float(t.attrib['font_size'])
        boldness = boldness/tcount
        fsize = (fsize/tcount)/modal_fs
        print (tok1+"\t"+tok2+"\t"+str(tcount)+"\t"+str(boldness)+"\t"+str(round(fsize,2))+"\t"+token_features(tok1)+"\t"+token_features(tok2))
        f.write(tok1+"\t"+tok2+"\t"+str(tcount)+"\t"+str(boldness)+"\t"+str(round(fsize,2))+"\t"+token_features(tok1)+"\t"+token_features(tok2)+"\t0\n")

def group2_work(tree):

    new_newxroot = ET.Element("Document")
    nroot = tree.getroot()

    for chunks in nroot.findall('chunk'):
        nchunk = ET.SubElement(new_newxroot, "chunk")

        tokens = chunks.findall('token')
        print tokens
        if(len(tokens)>0 and ((tokens[0].text == 'Table' or tokens[0].text == 'TABLE') and tokens[0].attrib['bold'] == 'yes')):
            stat =1
        else :
            stat =0
        prev_bold =1
        for token in chunks.findall('token'):
           if(stat==1 and prev_bold ==1 and token.attrib['bold']== 'no' ):
                nchunk = ET.SubElement(new_newxroot, "chunk")
                ET.SubElement(nchunk, "token",  y=token.attrib['y'], font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
           else :
                ET.SubElement(nchunk, "token",  y=token.attrib['y'], font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text

    ntree = ET.ElementTree(new_newxroot)
    f = open(a_file.split('.')[0]+'_g2_out.txt','w')
    newxroot = ntree.getroot()
    for achunk in newxroot.findall('chunk'):
        boldness = 0
        fsize = 0
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
        fsize = (fsize/tcount)/modal_fs
        y_pos = tokens[0].attrib['y']
        print (tok1+"\t\t\t"+tok2+"\t\t\t"+str(tcount)+"\t\t\t"+str(boldness)+"\t\t\t"+str(round(fsize,2))+"\t\t\t"+tb_heading_features(bool))
        f.write(tok1+"\t\t\t"+tok2+"\t\t\t"+str(round(fsize,2))+"\t\t\t"+str(y_pos)+"\t\t\t"+"0\n")

class g4Thread(threading.Thread):
    mytree=None
    def __init__(self, threadID, name, xtree):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.mytree=xtree
    def run(self):
        print "Starting " + self.name
        group4_work(self.mytree)
        print "Exiting " + self.name


class g2Thread(threading.Thread):
    mytree=None
    def __init__(self, threadID, name, xtree):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.mytree=xtree
    def run(self):
        print "Starting " + self.name
        group2_work(self.mytree)
        print "Exiting " + self.name

for a_file in files_list:
    tree = ET.parse(root_folder+a_file)
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
                    fsizes[round(abs(float(token.attrib['font-size'])))]=fsizes.get(round(abs(float(token.attrib['font-size']))),0)+1
                    if(p_yloc is None):
                        p_yloc=float(token.attrib['y'])
                    if(float(token.attrib['font-size'])>max_fs):
                        max_fs=float(token.attrib['font-size'])
                    y_diff[round(abs(float(token.attrib['y'])-pre_y))]=y_diff.get(round(abs(float(token.attrib['y'])-pre_y)),0)+1
                    pre_y=float(token.attrib['y'])
                except:
                    print "Exception Occured"
    modal_fs = 0
    for fontsz in fsizes.keys():
        if(modal_fs == 0):
            modal_fs = fontsz
            continue
        if(fsizes[fontsz]>fsizes[modal_fs]):
            modal_fs=fontsz
    ##############
    # DEBUG
    # print max_fs
    # print("fsizes!!!")
    # print fsizes
    ##############
    new_l = sorted(y_diff.iteritems(), key=operator.itemgetter(1), reverse=True)[:7]
    x_l = []
    # print(new_l)
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
    limit = max([x[0] for x in new_l])+1
    del x_l
    del new_l
    # print(limit)
    ###########################################
    f_fn = open(a_file.split('.')[0]+'_g2_foot.txt','w')
    f_fn.write("0\t0\t0\t0\t0\t0\t0\t0\t0\n")
    f_url = open(a_file.split('.')[0]+'_g2_url.txt','w')
    f_url.write("0\t\t\t\t\t\t0\n")
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    ###########################################
    xroot = ET.Element("Document")
    chunk = ET.SubElement(xroot, "chunk")
    for pages in root.findall('PAGE'):
        for texts in pages.findall('TEXT'):
            fn_flag=1
            for token in texts.findall('TOKEN'):
                if type(token.text) is unicode:
                    word = unicodedata.normalize('NFKD', token.text).encode('ascii','ignore')
                else:
                    word = token.text
                if(word and len(word.replace(' ',''))>0):
                    ###########################################
                    f_fn.write((word.replace(' ','')+"\t\t\t\t\t").encode("utf-8"))
                    f_fn.write((str(round(float(token.attrib['font-size'])/(max_fs),2))+"\t").encode("utf-8"))
                    f_fn.write(((token.attrib['x'])+"\t").encode("utf-8"))
                    f_fn.write(((token.attrib['y'])+"\t").encode("utf-8"))
                    f_fn.write((binary(token.attrib['bold'])+"\t"+binary(token.attrib['italic'])+"\t").encode("utf-8"))
                    f_fn.write((caps(word.replace(' ',''))+"\t").encode("utf-8"))
                    f_fn.write((str(fn_flag)+"\t").encode("utf-8"))
                    f_fn.write(("0\n").encode("utf-8"))
                    #-----------------------------------------
                    f_url.write((word.replace(' ','')+"\t\t\t\t\t\t").encode("utf-8"))
                    x = word.strip('()')
                    if(bool(pattern.match(x.replace(' ','')))):
                        f_url.write(("1\n").encode("utf-8"))
                    else:
                        f_url.write(("0\n").encode("utf-8"))
                    ###########################################
                    if( abs(float(token.attrib['y'])-p_yloc)>=limit):
                        chunk = ET.SubElement(xroot, "chunk")
                    p_yloc = float(token.attrib['y'])
                    ET.SubElement(chunk, "token", y=token.attrib['y'], font_size=token.attrib['font-size'], bold=token.attrib['bold']).text = word
                fn_flag=0
            f_fn.write("0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
            f_url.write("0\t\t\t\t\t\t0\n\n")

    f_fn.close()
    f_url.close()

    tree = ET.ElementTree(xroot)
    # tree.write(file+"_res.xml")
    del xroot
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
            if(count < 15 and p_fsize is not None and float(token.attrib["font_size"]) < p_fsize and stat==1 ):
                chunk = ET.SubElement(newxroot, "chunk")
                ET.SubElement(chunk, "token", y=token.attrib['y'], font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
            else:
                ET.SubElement(chunk, "token", y=token.attrib['y'], font_size=token.attrib['font_size'], bold=token.attrib['bold']).text = token.text
                count  = count + 1
            p_fsize = float(token.attrib['font_size'])

    tree = ET.ElementTree(newxroot)

    # Create new threads
    thread_g4 = g4Thread(1, "Group-4", tree)
    thread_g2 = g2Thread(2, "Group-2", tree)

    # Start new Threads
    thread_g2.start()
    thread_g4.start()
