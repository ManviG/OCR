flag = "0"   # to check if found the domain (1 => found)
flag2 = "0"  # to check if we were in a email block (1=>yes) or we have a seperate email (0 => seperate email)
emails = []
filetoRead = "final.txt"
outfile = open("Allmails.txt",'a')
with open(filetoRead,'r') as f:
    for line in f:
        abc = line.split()

        if len(abc) >= 1:  # if not a blank line

	        if abc[3] == "5":   #output column
			if abc[0].find('{')!=-1 or abc[0].find('[')!=-1:
			    flag2 = "1"
			if abc[0].find('}')==-1 and abc[0].find(']')==-1:
	        	    emails.append((((abc[0].strip('{')).strip('[')).strip(',')))
			if abc[0].find("}")!=-1:
			    domain = str(abc[0].split('}')[len(abc[0].split('}'))-1])
			    for email in ((((abc[0].strip('{')).strip('[')).strip(',')).split('}')[0]).split(','):	#done since there may
			    	emails.append(email)									#not be spaces b/w ,
	        	    flag = "1"
			    flag2 = "0"
			if abc[0].find("]")!=-1:
			    domain = str(abc[0].split(']')[len(abc[0].split(']'))-1])
			    for email in ((((abc[0].strip('{')).strip('[')).strip(',')).split(']')[0]).split(','):
			    	emails.append(email)
	        	    flag = "1"
			    flag2 = "0"
			if flag == "0" and flag2 == "0":
			    outfile.write("#e " + abc[0].strip(',') + "\n")
			if flag == "1":
			    for usernames in emails:
				usernames += domain
				outfile.write("#e " + usernames + "\n")
			    flag = "0"
	        else:
	        	if abc[0] != "0":
	        		flag = "0"
				del emails[:]

outfile.write("\nEOF\n\n")
outfile.close()
