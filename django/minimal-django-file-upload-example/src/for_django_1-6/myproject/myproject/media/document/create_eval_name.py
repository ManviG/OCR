
from __future__ import division

import xml.etree.ElementTree as ET


# """
# Create an summary file of author names
# """
def genFile(fName, path=""):
    tree = ET.parse("TitleAuthor.xml")
    root = tree.getroot()
    f = open('eval_author.txt','w')
    for author in root.findall('name'):
        fn = author.findall('first_name')
        mn = author.findall('middle_name')
        ln = author.findall('last_name')
        # print "<<section>>"
        f.write("<<name>>\n")
        if(len(fn)>0):
            f.write("First name : "+fn[0].text+"\n")
        if(len(mn)>0):
            f.write("Middle name : "+mn[0].text+"\n")
        if(len(ln)>0):
            f.write("Last name : "+ln[0].text+"\n")
    f.close()
    print "Done!!!"


"""Demo call"""
genFile("TitleAuthor.xml")