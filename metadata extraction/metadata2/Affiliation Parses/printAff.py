flag = "0"   # to check if a Affiliation is already going on
filetoread = "final.txt"
outfile = open('AllAffiliations.txt','a')
with open(filetoread,'r') as f:
    for line in f:
        abc = line.split()

        if len(abc) >= 1:  # if not a blank line

	        if abc[3] == "6":   #output column
	        	if flag == "0":  #if start of Affiliation
	        		outfile.write("#a ")
	        	outfile.write(abc[0] + ' ')
	        	flag = "1"
	        else:
			if flag == "1":
				outfile.write("\n")
				flag = "0"
	        	
outfile.write("\nEOF\n\n")
outfile.close()
