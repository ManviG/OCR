import xml.etree.ElementTree as ET
directory = '/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/'
f = open(directory + "input_Allmails.txt",'r')
out = open(directory + 'eval_emails.txt','w')
xml = '<root>' + f.read().split('<?xml version="1.0" ?>')[-1] + '</root>'
tree = ET.ElementTree(ET.fromstring(xml))
root = tree.getroot()
for mail in root.findall('email'):
    out.write("<<Email>>\n" + mail.text.strip() + "\n")
f.close()
out.close()
