author = "barno"

directory = '/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/'


flag = "0"   # to check if a title is already going on
end = 0
titl = 0;
print("<?xml version=\"1.0\" ?>\n")
print("<title_author>\n")
with open(directory + 'final.txt','r') as f:
    for line in f:
        abc = line.split()

        if len(abc) > 1:  # if not a blank line

        	# print "***" + abc[0]

        	if(abc[7]=="00"):
        		print

	        if abc[7] == "1":   #output column
	        	titl = 1;
	        	if flag == "0":  #if start of title
	        		print("\t<title>\n\t"),
	        	print(abc[0] + ' '),
	        	flag = "1"
	        else:
	        	if abc[0] != "0" and flag == "1":
	        		if(titl==1):
	        			print("\n\t</title>")
	        			titl = 0;
	        		flag = "0"
	        		print

	        if abc[7] == "2": #first name
	        	if(titl==1):
	        			print("\n\t</title>")
	        			titl = 0;
	        	x = abc[0].strip(',')
	        	print("\t<name>\n\t\t<first_name> " + x + " </first_name>\n")

	        if abc[7] == "3": #middle name
	        	x = abc[0].strip(',')
	        	print("\t\t<middle_name> " + x + " </middle_name>\n")

	        if abc[7] == "4":  #last name
	        	x = abc[0].strip(',')
	        	print("\t\t<last_name> " + x + " </last_name>\n\t</name>")
	        	
print("</title_author>\n")