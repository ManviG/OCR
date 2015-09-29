author = "barno"

from itertools import izip

track = 0
f = open('/home/barno/Desktop/nlp/files/names.txt','w')
with open('/home/barno/Desktop/nlp/files/title_author.txt','r') as fi:
	for line in fi:
		abc = line.split()

		if len(abc) >= 1:
			if abc[0] == "#f":
				track = 0
				names = ""
				names = names + " " + abc[1]
				track = track + 1
			if abc[0] == "#m":
				names = names + " " + abc[1]
				track = track + 1
			if abc[0] == "#l":
				names = names + " " + abc[1]
				track = track + 1
				f.write("#n " + names + "\n")

		else:
			f.write("\n")

f.close()

track = 0
author = []
mail = []
ma = []
fullmail = []

with open('/home/barno/Desktop/nlp/files/names.txt','r') as f1, open('/home/barno/Desktop/nlp/files/emails.txt','r') as f2:
    for line1,line2 in izip(f1,f2):
        x = line1.split()
        y = line2.split()

        if len(x) >= 1 and len(y) >= 1:

        	x.remove("#n")
        	y.remove("#e")

        	fullmail.insert(track,y[0])
        	# print y[0]

        	y1 = y[0].split("@")
        	y1 = y1[0]

        	author.insert(track,x)
        	mail.insert(track,y[0])
        	ma.insert(track,y[0])
        	track = track + 1

        else:

        	for mai in ma:
	        	m = mai.split("@")
	        	m = m[0]
        		for a in author:
        			for n in a:
        				if n.lower() in m:
        					for na in a:
        						print na,
        					print " ----> ",
        					print mai
        					author.remove(a)
        					mail.remove(mai)
        					break

        	s = 0
        	i = 0
        	an = ""
        	del ma[:]
        	for m in mail:
        		ma.insert(s,m)
        		s = s + 1
        	s = 0
        	if len(mail) > 0 and len(author) > 0:
        		for mai in ma:
        			# print "MAI",
        			# print mai
        			# print ma
        			# print mail
        			m = mai.split("@")
        			m = m[0]
        			for a in author:
        				for n in a:
        					an = an + n
      					while s<len(m):
	  						if m[s] in an.lower():
	  							s = s + 1
	  						else:
	  							break
      					if s == len(m):
      						for na in a:
      							print na,	
        					print " ----> ",
        					print mai
        					author.remove(a)
        					mail.remove(mai)
        				an = ""
        				s = 0

		del mail[:]
		del ma[:]
		del author[:]
		track = 0
		print
