author = "barno"

total = float(0)
correct = float(0)
with open('final.txt','r') as f:
    for line in f:
        abc = line.split()

        if len(abc) > 1:  # if not a blank line
        	total = total + 1
        	if abc[2] == abc [3] or abc[2] == "00":
        		correct = correct + 1
        	else:
        		print abc[0]

print correct/total * 100