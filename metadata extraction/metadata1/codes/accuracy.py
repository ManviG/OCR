author = "barno"

total = float(0)
correct = float(0)
with open('final.txt','r') as f:
    for line in f:
        abc = line.split()

        if len(abc) > 1:  # if not a blank line
        	total = total + 1
        	if abc[5] == abc [6]:
        		correct = correct + 1

print correct/total * 100