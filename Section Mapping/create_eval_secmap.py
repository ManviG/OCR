
from __future__ import division

import xml.etree.ElementTree as ET


"""
Create an summary file of headings and sections
"""
def genFile(fName, path=""):
    tree = ET.parse(path+fName)
    root = tree.getroot()

    f = open('eval_'+fName.split('.')[0]+'.txt','w')
    for section in root.findall('section'):
        heads = section.findall('heading')
        chunks = section.findall('chunk')
        # print "<<section>>"
        f.write("<<section>>\n")
        if(len(heads)>0):
            # print "Heading: "+heads[0].text
            f.write("Heading: "+heads[0].text+"\n")
        if(len(chunks)>0):
            cw = chunks[0].text.split()
            # print "Chunks: "+" ".join(cw[:5])+" ... "+" ".join(cw[-5:])
            f.write("Chunks: "+" ".join(cw[:5])+" ... "+" ".join(cw[-5:])+"\n")
    print "Done!!!"


"""Demo call"""
genFile("test_secmap.xml")