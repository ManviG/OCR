author = "barno"

flag = "0"   # to check if a title is already going on
end = 0
with open('/home/barno/Desktop/nlp/files/final.txt','r') as f:
    for line in f:
        abc = line.split()

        if len(abc) > 1:  # if not a blank line

        	# print "***" + abc[0]

        	if(abc[6]=="00"):
        		print

	        if abc[6] == "1":   #output column
	        	if flag == "0":  #if start of title
	        		print("#t"),
	        	print(abc[0] + ' '),
	        	flag = "1"
	        else:
	        	if abc[0] != "0" and flag == "1":
	        		flag = "0"
	        		print

	        if abc[6] == "2": #first name
	        	x = abc[0].strip(',')
	        	print("#f " + x)

	        if abc[6] == "3": #middle name
	        	x = abc[0].strip(',')
	        	print("#m " + x)

	        if abc[6] == "4":  #last name
	        	x = abc[0].strip(',')
	        	print("#l " + x)
	        	
