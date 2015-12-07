author = "barno"

directory = '/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/'


def comma(y):
	x = y.strip()
	if x[len(x)-1] == ',':
		return "1"
	else:
		return "0"

fi = open(directory + 'test_file.txt','w')

flag = "0"   # to check if a title is already going on
end = 0
with open(directory + 'test.txt','r') as f:
	for line in f:
		abc = line.split()

		if len(abc) > 1:  # if not a blank line

			l = abc[0] + "\t" + abc[1] + "\t" + abc[2] + "\t" + abc[3] + "\t" + abc[4] + "\t" + comma(abc[0]) + "\t" + abc[5] + "\n"

			fi.write(l);

fi.close()