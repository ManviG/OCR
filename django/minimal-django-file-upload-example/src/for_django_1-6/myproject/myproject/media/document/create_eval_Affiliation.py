import xml.etree.ElementTree as ET
f = open("input_AllAffiliations.txt",'r')
out = open('eval_Affiliations.txt','w')
xml = '<root>' + f.read().split('<?xml version="1.0" ?>')[-1] + '</root>'
tree = ET.ElementTree(ET.fromstring(xml))
root = tree.getroot()
for affs in root.findall('Affiliation'):
    out.write("<<Affiliation>>\n" + affs.text.strip() + "\n")
f.close()
out.close()
