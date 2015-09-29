author = "priyank"

flag = "0"   # to check if a Affiliation is already going on
with open('final.txt','r') as f:
    for line in f:
        abc = line.split()

        if len(abc) >= 1:  # if not a blank line
        	if abc[2] == "00":
        		print
        	else:
		        if abc[3] == "6":   #output column
		        	if flag == "0":  #if start of Affiliation
		        		print("#a "),
		        	print(abc[0] + ' '),
		        	flag = "1"
		        else:
					if flag == "1":
				        	if abc[0] != "0":
				        		flag = "0"
				        		print
