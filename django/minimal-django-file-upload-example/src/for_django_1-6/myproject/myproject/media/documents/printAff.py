flag = "0"   # to check if a Affiliation is already going on
filetoread = raw_input().split(".")[0] + "_parse.txt"
outfile = open(filetoread.split("_parse.txt")[0]+"_AllAffiliations.txt",'w')
outfile.write("<?xml version=\"1.0\" ?>\n")
with open(filetoread,'r') as f:
    for line in f:
        abc = line.split()

        if len(abc) >= 1:  # if not a blank line

	        if abc[1] == "1":   #output column
	        	if flag == "0":  #if start of Affiliation
	        		outfile.write("\n<Affiliation>\n\t")
	        	outfile.write((abc[0].strip(',')).strip('.') + ' ')
	        	flag = "1"
	        else:
			if flag == "1":
				outfile.write("\n</Affiliation>\n")
				flag = "0"
	        	

outfile.close()
