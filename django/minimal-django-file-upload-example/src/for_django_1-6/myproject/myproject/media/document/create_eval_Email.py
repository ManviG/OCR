import xml.etree.ElementTree as ET
f = open("input_Allmails.txt",'r')
out = open('eval_emails.txt','w')
xml = '<root>' + f.read().split('<?xml version="1.0" ?>')[-1] + '</root>'
tree = ET.ElementTree(ET.fromstring(xml))
root = tree.getroot()
for mail in root.findall('email'):
    out.write("<<Email>>\n" + mail.text.strip() + "\n")
f.close()
out.close()
