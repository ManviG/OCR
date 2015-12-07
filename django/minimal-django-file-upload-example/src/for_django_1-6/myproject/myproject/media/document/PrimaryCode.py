from __future__ import division
import xml.etree.ElementTree as ET
import unicodedata
import threading
import operator
import roman
import re
import os
import string
import sys
import types
import copy

# List of files and the root folder for batch processing
files_list = ["input.xml"]
root_folder = '/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/'

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
        #print (tok1+"\t"+tok2+"\t"+str(tcount)+"\t"+str(boldness)+"\t"+str(round(fsize,2))+"\t"+token_features(tok1)+"\t"+token_features(tok2))
        f.write(tok1+"\t"+tok2+"\t"+str(tcount)+"\t"+str(boldness)+"\t"+str(round(fsize,2))+"\t"+token_features(tok1)+"\t"+token_features(tok2)+"\t0\n")

def group2_work(tree):

    new_newxroot = ET.Element("Document")
    nroot = tree.getroot()

    for chunks in nroot.findall('chunk'):
        nchunk = ET.SubElement(new_newxroot, "chunk")

        tokens = chunks.findall('token')
       # print tokens
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
        #print (tok1+"\t\t\t"+tok2+"\t\t\t"+str(tcount)+"\t\t\t"+str(boldness)+"\t\t\t"+str(round(fsize,2))+"\t\t\t"+tb_heading_features(bool))
        f.write(tok1+"\t\t\t"+tok2+"\t\t\t"+str(round(fsize,2))+"\t\t\t"+str(y_pos)+"\t\t\t"+"0\n")

## Group2_functions

def search_name_year(Reference,name,year):
    name = name.replace(" ","")
    for i in range(len(Reference)):
        refs = Reference[i]    
        if name in refs and year in refs:
            return i
    return 0                                  # make it -1
		
def search_doublename(Reference,name1,name2,year):
    name1 = name1.replace(" ","")
    name2 = name2.replace(" ","")
    for i in range(len(Reference)):
        refs = Reference[i]
        if name1 in refs and name2 in refs and year in refs:
            return i		
    return 0                                 # make it -1
## Group2_functions end


def isEmail(y):
    x=y.strip()
    isatr = 0
    for i in range(len(x)):
        if x[i] == "@":
            isatr = 1
        if((isatr==1) and (x[i]==".") and (x[i+1]<"z" and x[i+1]>"a")):
            return "1"
    return "0"
a_file = raw_input()
foutMail = open(a_file.split(".")[0] + '_mail_parse.txt','w')
foutMail.write("0\t0\t0\n")
p = []
alp = []
count = 0
bracks = 0

def processTokenForMail(word):

    global bracks
    global p
    global alp
    if word.find("{")!=-1 or word.find("[")!=-1:
        bracks=bracks+1
    isthisemail = (isEmail(word))
    if bracks > 0:
        if(len(word.replace(' ',''))>0):
            alp.append((word.replace(' ','')+"\t").encode("utf-8"))
            alp.append(isthisemail+"\t")
            alp.append(("0\n").encode("utf-8"))
        p.append(copy.copy(alp))
        #print p
        del alp[:]
    
    if(len(word.replace(' ',''))>0) and bracks<=0:
        if (isEmail(word)) == "1":
            foutMail.write((word.replace(' ','')+"\t").encode("utf-8"))
            foutMail.write(isthisemail+"\t")
            foutMail.write(("0\n").encode("utf-8"))
    if word.find("}")!=-1 or word.find("]")!=-1:
        bracks -= 1
        if(len(p)!=0):
            if int(p[len(p)-1][1])==1:              #If it is email
                for i in range(len(p)):
                    p[i][1] = "1\t"
            #print p
            for i in range(len(p)):
                for j in p[i]:
                    if p[i][1]=="1\t" or p[i][1]=="1":
                        foutMail.write(str(j))
        del p[:]
    return isthisemail

###############################Email over affiliation start#########################################


def isAffiliation(y,fs):
    x=y.strip()                                         
    x=x.strip(',')
    if fs == max_fs:            #If in Title (Biggest Font Size) it can't be affiliation.
        #print x
        return "0"              #Done to prevent cases when "Research" comes in title (often)
    if x.find("Universit")!=-1 or x.find(" Labs")!=-1 or x.find("Laboratories")!=-1 or x.find("Institut")!=-1 or x.find("Research")!=-1 or x.find("College")!=-1 or x.find("Corporat")!=-1 or x.find("Academy")!=-1:
        t = x.split(' ')
        countsmall = 0
        countall = 0
        for word in t:
            countall += 1
            if word == word.lower():
                countsmall += 1
        #print str(countall) + " " + str(countsmall)  
        if countsmall > 3:
                return "0"
        #print "Yes " + word
        return "1"
    return "0"

AffiliationOutputFile = open(a_file.split(".")[0]+'_parse.txt','w')
AffiliationOutputFile.write("0\t0\t0\n")
cit2ref = open(a_file.split(".")[0]+'cit2ref.txt','w');
def FindAffiliation(stri,fs):
    l = []
    a = []
    stri = ((((((((((stri.strip('1')).strip('2')).strip('3')).strip('4')).strip('5')).strip('6')).strip('7'))).strip('8')).strip('9')).strip('0')
    #print stri
    t = stri.split(',')
    aff = "0"
    for j in t:
        j = j.strip()
        #print j
        if aff == "1" and isAffiliation(j,fs) == "0":
            if (j.split(' '))[0] is "":
                continue
            if ((j.split(' '))[0])[0].isupper():
                aff = "1"
            else:
                aff = "0"
        else:
            aff = isAffiliation(j,fs)
        #print aff
        x = j.split(' ')
        for i in x:
            if len(i) > 0:
                if(aff!="0"):
                    AffiliationOutputFile.write((i+"\t").encode("utf-8"))
                    AffiliationOutputFile.write(aff + "\t")
                    AffiliationOutputFile.write(("0\n").encode("utf-8"))


#######################################\PRIYANK#####################################################

#########################################Barno######################################################
def startCaps(y):
    x=y.strip()
    if x[0].isupper():
        return "1"
    else:
        return "0"

def comma(y):
    x = y.strip()
    if x[len(x)-1] == ',':
        #print y
        return "1"
    else:
        return "0"

def parse2() :
    fi = open(a_file.split('.')[0]+'_NameAndTitle.txt','w')

    flag = "0"   # to check if a title is already going on
    end = 0
    with open(a_file.split('.')[0]+'_NameAndTitle1.txt','r') as NameAndTitle1:
        for line in NameAndTitle1:
            abc = line.split()

            if len(abc) > 1:  # if not a blank line

                l = abc[0] + "\t" + abc[1] + "\t" + abc[2] + "\t" + abc[3] + "\t" + abc[4] + "\t" + comma(abc[0]) + "\t" + abc[5] + "\n"

                fi.write(l);

    fi.close()
########################################\Barno######################################################

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

tree = ET.parse(a_file)
root = tree.getroot()
max_fs = 0
p_yloc = None
y_diff={}
fsizes = {}

tot_txt = 0

flag = False
reg_ex = True
Reference = []

for pages in root.findall('PAGE'):
    pre_y = 0;
    texts = pages.findall('TEXT')
    for i  in range(len(texts)):
        tot_txt += 1        
        tokens = texts[i].findall('TOKEN')        
        if flag==False:            
            for j in range(len(tokens)):
                if tokens[j] is None:
                    continue
                try:
                    fsizes[round(abs(float(tokens[j].attrib['font-size'])))]=fsizes.get(round(abs(float(tokens[j].attrib['font-size']))),0)+1
                    if(p_yloc is None):
                        p_yloc=float(tokens[j].attrib['y'])
                    if(float(tokens[j].attrib['font-size'])>max_fs):
                        max_fs=float(tokens[j].attrib['font-size'])
                    y_diff[round(abs(float(tokens[j].attrib['y'])-pre_y))]=y_diff.get(round(abs(float(tokens[j].attrib['y'])-pre_y)),0)+1
                    pre_y=float(tokens[j].attrib['y'])
                except:
                    pass
                    #print "Exception Occured" 

                if type(tokens[j].text) is unicode:
                    word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
                else:
                    word = tokens[j].text
                    if isinstance(word, types.NoneType): 
                        #print " word type is NoneType" 
                        continue

                if(len(word.replace(' ',''))>0):
                    if ((word=="REFERENCES" or word=="References") and binary(tokens[j].attrib['bold'])):
                        #print word + " now that's it"
                        flag = True
                        first_text = True
                        continue
        else:
            cur_x = texts[i].attrib['x']
            cur_y = texts[i].attrib['y'] 
            cur_size = float(tokens[0].attrib['font-size'])
            cur_font = tokens[0].attrib['font-name']
            cur_font = cur_font.lower()
            cur_bold = tokens[0].attrib['bold']
            cur_italic = tokens[0].attrib['italic']
         
            if first_text:              
                start_ref = cur_x
                idx = 0
                Reference.append("")
                first_height = float(texts[i+1].attrib['y']) - float(cur_y)
                first_size = float(tokens[0].attrib['font-size'])
                first_font = tokens[0].attrib['font-name'].lower()
                first_lower = first_font.lower()
                first_bold = tokens[0].attrib['bold']
                first_italic = tokens[0].attrib['italic']
                first_text = False                
            else:               
                if (float(cur_y) < float(prev_y)):
                    if cur_size < first_size - 0.1 or cur_size > first_size + 0.1 or cur_font != first_font or cur_bold != first_bold or cur_italic != first_italic:
                        continue
                    k = i + 1
                    while(True):
                        if k >= len(texts):
                            start_ref = cur_x
                            break
                        next_x = texts[k].attrib['x']
                        if(float(next_x) > float(cur_x) + 0.1):
                            start_ref = cur_x
                            idx = idx + 1
                            Reference.append("")
                            break
                        if(float(next_x) < float(cur_x) - 0.1):
                            start_ref = next_x
                            break
                        k = k + 1
                else:
                    if float(cur_y) - float(prev_y) > 3 * first_height:
                        continue                                         
                    if (float(cur_x) < float(start_ref) + 0.1 ):
                        idx = idx + 1
                        Reference.append("")   
             
            prev_x = cur_x
            prev_y = cur_y 

            for j in range(len(tokens)):

                try:
                    fsizes[round(abs(float(tokens[j].attrib['font-size'])))]=fsizes.get(round(abs(float(tokens[j].attrib['font-size']))),0)+1
                    if(p_yloc is None):
                        p_yloc=float(tokens[j].attrib['y'])
                    if(float(tokens[j].attrib['font-size'])>max_fs):
                        max_fs=float(tokens[j].attrib['font-size'])
                    y_diff[round(abs(float(tokens[j].attrib['y'])-pre_y))]=y_diff.get(round(abs(float(tokens[j].attrib['y'])-pre_y)),0)+1    
                    pre_y=float(tokens[j].attrib['y'])
                except:
                    print "Exception Occured"

                if type(tokens[j].text) is unicode:
                    word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')
                else:
                    word = tokens[j].text
                    if isinstance(word, types.NoneType): 
                        print " word type is NoneType" 
                        continue
                if(len(word.replace(' ',''))>0):
                    Reference[idx] += word
                    Reference[idx] += " "
cit2ref.write("<?xml version=\"1.0\" ?>\n")
for i in range(len(Reference)):
    cit2ref.write("-<Reference")
    cit2ref.write(" id=\"" + str(i + 1) + "\" >");
    cit2ref.write(Reference[i]);
    cit2ref.write("</Reference>\n\n")

cit2ref.write("\n\n")

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

NameAndTitle = open(a_file.split('.')[0]+'_NameAndTitle1.txt','w')
NameAndTitle.write("0\t0\t0\t0\t0\t0\n")

pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
###########################################
xroot = ET.Element("Document")
chunk = ET.SubElement(xroot, "chunk")
citations_no = 0
flag = True
stringForAff = ""
txt = 0

for pages in root.findall('PAGE'):
    count+=1    
    texts = pages.findall('TEXT')
    for i  in range(len(texts)):
        line = ""
        fn_flag=1
        txt += 1
        tokens = texts[i].findall('TOKEN')
        for j in range(len(tokens)):            
            if type(tokens[j].text) is unicode:
                word = unicodedata.normalize('NFKD', tokens[j].text).encode('ascii','ignore')

                
            else:
                word = tokens[j].text

                if(word and len(word.replace(' ',''))>0):
                    ###########################################
                    f_fn.write((word.replace(' ','')+"\t\t\t\t\t").encode("utf-8"))
                    f_fn.write((str(round(float(tokens[j].attrib['font-size'])/(max_fs),2))+"\t").encode("utf-8"))
                    f_fn.write(((tokens[j].attrib['x'])+"\t").encode("utf-8"))
                    f_fn.write(((tokens[j].attrib['y'])+"\t").encode("utf-8"))
                    f_fn.write((binary(tokens[j].attrib['bold'])+"\t"+binary(tokens[j].attrib['italic'])+"\t").encode("utf-8"))
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
                    if( abs(float(tokens[j].attrib['y'])-p_yloc)>=limit):
                        chunk = ET.SubElement(xroot, "chunk")
                    p_yloc = float(tokens[j].attrib['y'])
                    ET.SubElement(chunk, "token", y=tokens[j].attrib['y'], font_size=tokens[j].attrib['font-size'], bold=tokens[j].attrib['bold']).text = word

                if count<=2:
                    if type(word) is not str:
                        continue

                    RetVal = processTokenForMail(word);

                    if(RetVal=="1"):
                        foutMail.write("0\t0\t0\n")

                    stringForAff += word + " "

                    if(len(word.replace(' ',''))>0):
                        NameAndTitle.write((word.replace(' ','')+"\t").encode("utf-8"))
                        NameAndTitle.write((binary(tokens[j].attrib['bold'])+"\t").encode("utf-8")) #Bold
                        NameAndTitle.write((str(round(float(txt)/(tot_txt),2))+"\t").encode("utf-8")) #Relative position
                        NameAndTitle.write((str(round(float(tokens[j].attrib['font-size'])/(max_fs),2))+"\t").encode("utf-8")) #Relative size
                        NameAndTitle.write((startCaps(tokens[j].text.encode("utf-8").replace(' ','')))+"\t")
                        # NameAndTitle.write((comma(tokens[j].text.encode("utf-8").replace(' ','')))+"\t")
                        NameAndTitle.write(("0\n").encode("utf-8"))

                if isinstance(word, types.NoneType):
                    continue
                if (len(word)>0) and flag==True:
                    if ((word=="REFERENCES" or word=="References") and binary(tokens[j].attrib['bold'])):
                        flag = False
                    word += " "
                    line += word


        f_fn.write("0\t0\t0\t0\t0\t0\t0\t0\t0\n\n")
        f_url.write("0\t\t\t\t\t\t0\n\n")
        
        if(count<=2):
            FindAffiliation(stringForAff,float(tokens[j].attrib['font-size']))
            stringForAff = ""
            AffiliationOutputFile.write("0\t0\t0\n")
            NameAndTitle.write("0\t0\t0\t0\t0\t0\n\n")
    
        if flag==True:    
            regex = re.compile("([A-Z][a-zA-Z]* et al[.] \[(\d{1,3})\])")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    cit2ref.write("<citation ref_id=\"" + a[1] + "\"")
                    cit2ref.write("  reference=\"" + Reference[int(a[1])-1] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n")
                    


            regex = re.compile("([A-Z][a-zA-Z]* \[(\d{2})\])")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    cit2ref.write("<citation ref_id=\"" + a[1] + "\"")
                    cit2ref.write("  reference=\"" + Reference[int(a[1])-1] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")
            
            regex = re.compile("([A-Z][a-zA-Z]* et al[.][ ]*\[(\d{1})\])")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    cit2ref.write("<citation ref_id=\"" + a[1] + "\"")
                    cit2ref.write("  reference=\"" + Reference[int(a[1])-1] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")
            
            regex = re.compile("(([A-Z][a-zA-Z]*) et al[.][,] (\d{4}))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")
                
            regex = re.compile("(([A-Z][a-zA-Z]*) et al[.] (\d{4}))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")                

            regex = re.compile("(([A-Z][a-zA-Z]*) and ([A-Z][a-zA-Z]*) \((\d{4})\))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_doublename(Reference,a[1],a[2],a[3])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")

        
            regex = re.compile("(([A-Z][a-zA-Z]*) and ([A-Z][a-zA-Z]*)[,] (\d{4}))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_doublename(Reference,a[1],a[2],a[3])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")             
        
            regex = re.compile("(([A-Z][a-zA-Z]*)[,] (\d{4}))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")
            
            regex = re.compile("(([A-Z][a-zA-Z]*) (\d{4}))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")                   
        
            regex = re.compile("(([A-Z][a-zA-Z]*) \((\d{4}[a-z]*)\))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")  
                
            regex = re.compile("(([A-Z][a-zA-Z]*) et al[.], (\d{4}[a-z]))")
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n")  
        
            regex = re.compile("(.*?\((.*?)\))")
            result = re.findall(regex, line)
            if len(result) > 0:
                    for a in result:
                        citations_no += 1
                        temp = a[0]
                        regex1 = re.compile("\d{4}$")
                        cits = a[1].split(';')
                        for citation in cits:
                            citation = citation.replace(" ","")
                            if regex1.match(citation):
                                #print citation
                                #print "a"
                                #print line
                                temp = temp.replace(citation,'CITATION')
                                #print Reference[int(citation)-1]
                                #print
                    line = line.replace(a[0],temp)
            
            regex = re.compile("(.*?\[(.*?)\])")
            result = re.findall(regex, line)
            if len(result) > 0:
                for a in result:
                    citations_no += 1
                    temp = a[0]
                    regex1 = re.compile("\d{1,3}$")
                    cits = a[1].split(',')
                    #print cits
                    #print "b"
                    for citation in cits:
                        citation = citation.replace(" ","")
                        if regex1.match(citation):
                            #print citation
                            #print "a"
                            #print line
                            temp = temp.replace(citation,'CITATION')
                            cit2ref.write("<citation ref_id=\"" + citation + "\"")
                            cit2ref.write("  reference=\"" + Reference[int(citation)-1] + "\" >")
                            cit2ref.write(a[0] + "</citation>\n\n")                              
                line = line.replace(a[0],temp)

            regex = re.compile("(([A-Z][a-zA-Z]*) et al[.], (\d{4}[a-z]))")    
            result = re.findall(regex, line)
            if len(result) > 0: 
                for a in result:
                    citations_no += 1
                    line = line.replace(a[0],'CITATION')
                    r_id = search_name_year(Reference,a[1],a[2])
                    cit2ref.write("<citation ref_id=\"" + str(r_id + 1) + "\"")
                    cit2ref.write("  reference=\"" + Reference[r_id] + "\" >")
                    cit2ref.write(a[0] + "</citation>\n\n") 

NameAndTitle.write("00\t00\t00\t00\t00\t00\n\n")
NameAndTitle.close()
parse2()
f_fn.close()
f_url.close()
AffiliationOutputFile.close()

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

