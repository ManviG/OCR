# -*- coding: utf-8 -*-

# ###################
# input : one file that contains the names in the format(other things can be present)
# 		# f <first name>
# 		# m <second name>
# 		# l <last name>

# 		one file that contains only emails in the format
# 		#e <email>
# 		with a blank line separating 2 papers

# output: one file with names as #n <full name>
# 		one file with mapping as <full name> ---> <email>
# ####################


author = "barno"

import codecs
import unicodedata

from itertools import izip

# latin_dict = { 
# ord(u"À"): u"A", ord(u"Á"): u"A", ord(u"Â"): u"A", ord(u"Ã"): u"A",
# ord(u"Ä"): u"A", ord(u"Å"): u"A", ord(u"Æ"): u"Ae",ord( u"Ç"): u"C", ord(u"È"): u"E",
# ord(u"É"): u"E", ord(u"Ê"): u"E", ord(u"Ë"): u"E", ord(u"Ì"): u"I", ord(u"Í"): u"I",
# ord(u"Î"): u"I", ord(u"Ï"): u"I", ord(u"Ð"): u"D", ord(u"Ñ"): u"N", ord(u"Ò"): u"O",
# ord(u"Ó"): u"O", ord(u"Ô"): u"O", ord(u"Õ"): u"O", ord(u"Ö"): u"O", ord(u"×"): u"*",
# ord(u"Ø"): u"O", ord(u"Ù"): u"U", ord(u"Ú"): u"U", ord(u"Û"): u"U", ord(u"Ü"): u"U",
# ord(u"Ý"): u"Y", ord(u"Þ"): u"p", ord(u"ß"): u"b", ord(u"à"): u"a", ord(u"á"): u"a",
# ord(u"â"): u"a", ord(u"ã"): u"a", ord(u"ä"): u"a", ord(u"å"): u"a", ord(u"æ"): u"ae",
# ord(u"ç"): u"c", ord(u"è"): u"e", ord(u"é"): u"e", ord(u"ê"): u"e", ord(u"ë"): u"e",
# ord(u"ì"): u"i", ord(u"í"): u"i", ord(u"î"): u"i", ord(u"ï"): u"i", ord(u"ð"): u"d",
# ord(u"ñ"): u"n", ord(u"ò"): u"o", ord(u"ó"): u"o", ord(u"ô"): u"o", ord(u"õ"): u"o",
# ord(u"ö"): u"o", ord(u"÷"): u"/", ord(u"ø"): u"o", ord(u"ù"): u"u", ord(u"ú"): u"u",
# ord(u"û"): u"u", ord(u"ü"): u"u", ord(u"ý"): u"y", ord(u"þ"): u"p", ord(u"ÿ"): u"y", 
# ord(u"’"): u"'", ord(u"-"):u"",
# }
directory = '/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/'

track = 0
track1 = 0
f = open(directory + 'names.txt','w')
with open(directory + 'title_author.txt','r') as fi:
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
found = 0

with open(directory+'names.txt','r') as f1, open(directory+'input_Allmailsformap.txt','r') as f2:
	for line1 in f1:
		x = line1.split()
		# y = line2.split()

		if len(x) >= 1:

			x.remove("#n")
			# y.remove("#e")

			# fullmail.insert(track,y[0])

			# y1 = y[0].split("@")
			# y1 = y1[0]

			author.insert(track1,x)
			# mail.insert(track,y[0])
			# ma.insert(track,y[0])
			track1 = track1 + 1


	for line2 in f2:
		y = line2.split()
		if len(y) >= 1:

			# x.remove("#n")
			y.remove("#e")

			fullmail.insert(track,y[0])

			y1 = y[0].split("@")
			y1 = y1[0]

			# author.insert(track1,x)
			mail.insert(track,y[0])
			ma.insert(track,y[0])
			track = track + 1

			# print ma


		# print ma
			#Check if name is a substring of the mail
	# print author
	if len(mail) > 0 and len(author) > 0:
		for mai in ma:
			found = 0
			m = mai.split("@")
			m = m[0]
			# print m
			for a in author:
				l = a
				# print a
				for ao in a:
					ao = ao.replace("-","")
				for n in a:
					# print n
					# print m
					if n.lower() in m:
							print "<map>\n\t",
							for na in l:
								print na,
							print "\n\t" + mai
							print "<\map>"
							author.remove(l)
							mail.remove(mai)
							found = 1
							break

				if found == 1:
					break

		s = 0
		i = 0
		an = ""
		del ma[:]
		for m in mail:
			ma.insert(s,m)
			s = s + 1
		s = 0

		#Check if every character in mail occurs the same number of time is the name
		if len(mail) > 0 and len(author) > 0:
			for mai in ma:
				m = mai.split("@")
				m = m[0]
				# print m
				for a in author:
					l = a
					for n in a:
						an = an + n
					while s<len(m):
						if m[s] in an.lower():
							if m[s] in an:
								indexx = an.index(m[s])
							else:
								indexx = an.index(m[s].upper())
							s = s + 1
							an = an[0:indexx] + an[indexx+1:]
						else:
							break
					if s == len(m):
						print "<map>\n\t",
						for na in l:
							print na,
						print "\n\t" + mai
						print "<\map>"
						author.remove(l)
						mail.remove(mai)
					an = ""
					s = 0

				ma[0:] = mail[0:]

				if len(mail) >= 10:
					mail[0:10] = mail[-10:]
					del mail[10:]
					author[0:10] = author[-10:]
					del author[10:]
					ma[0:10] = ma[-10:]
					del ma[10:]
					track = 10
