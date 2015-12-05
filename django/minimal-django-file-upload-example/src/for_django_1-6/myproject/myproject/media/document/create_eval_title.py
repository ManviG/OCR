
from __future__ import division

import xml.etree.ElementTree as ET


# """
# Create an summary file of author names
# """
def genFile(fName, path=""):
    tree = ET.parse("TitleAuthor.xml")
    root = tree.getroot()
    f = open('eval_title.txt','w')
    t = root.findall('title')
    f.write("<<title>>\n")
    if(len(t)>0):
        f.write("Title : "+ t[0].text.strip('\n,\t')+"\n")
    f.close()
    print "Done!!!"


"""Demo call"""
genFile("TitleAuthor.xml")