author = "priyank"

flag = "0"   # to check if a Email is already going on
emails = []
with open('final.txt','r') as f:
    for line in f:
        abc = line.split()

        if len(abc) >= 1:  # if not a blank line
        	if abc[2] == "00":
        		print
        	else:
		        if abc[3] == "5":   #output column
		        	if abc[0].find("{") == -1 and len(emails) == 0:
		        		print "#e " + abc[0]
		        	else:
		        		emails.append(((abc[0].strip('{')).strip(',')))
				if abc[0].find("}")!=-1:
				    domain = str(abc[0].split('}')[1])
				    emails[len(emails)-1] = emails[len(emails)-1].split('}')[0]
		        	    flag = "1"
				if flag == "1":
				    for usernames in emails:
					usernames += domain
					print "#e " + usernames
		        else:
		        	if abc[0] != "0":
		        		flag = "0"
					del emails[:]
