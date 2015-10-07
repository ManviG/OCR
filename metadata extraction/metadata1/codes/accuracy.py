# #############
# Tags:
# 1: title
# 2: first name
# 3: middle name
# 4: last name
# 0: everything else
# #############

author = "barno"

total = float(0)
correct = float(0)
type1 = 0
type2 = 0
with open('/home/barno/Desktop/nlp/files/final.txt','r') as f:
    for line in f:
        abc = line.split()

        #Accuracy check for name by cecking annotated column and predicted column
        if len(abc) > 1 and abc[5] != "0" and abc[5] != "1":
        	total = total + 1
        	if abc [6]!="0" and abc[6] != "1":
        		correct = correct + 1
                else:
                    print abc[0]
                if abc[5] == 0:
                	type2 = type2 + 1
                else:
	        		type1 = type1 + 1

print "Percentage accuracy: ",
print correct/total * 100
print "Total tokens checked: ",
print total
print "Tokens correctly extracted: ",
print correct
print "More tokens that should have been extracted: ",
print type1
print "More tokens that should not have been extracted: ",
print type2