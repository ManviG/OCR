
from __future__ import division

import xml.etree.ElementTree as ET

directory = '/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/'

# """
# Create an summary file of author names
# """
def genFile(fName, path=""):
    tree = ET.parse(directory + "TitleAuthor.xml")
    root = tree.getroot()
    f = open(directory + 'eval_title.txt','w')
    t = root.findall('title')
    f.write("<<title>>\n")
    if(len(t)>0):
        f.write("Title : "+ t[0].text.strip('\n,\t')+"\n")
    f.close()
    print "Done!!!"


"""Demo call"""
genFile("TitleAuthor.xml")