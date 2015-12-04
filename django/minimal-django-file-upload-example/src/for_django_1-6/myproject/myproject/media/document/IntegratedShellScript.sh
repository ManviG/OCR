Directory=/home/priyank/Desktop/SNLP_Project/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents
echo "script starts"
#/home/barno/work/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/
for f in $Directory/*.pdf
do
	echo "filename = $f"
	# ./pdftoxml.linux64.exe.1.2_7 $f
	echo "pdftoxml done\n"
done

for f in $Directory/*.xml
do
	echo "filename = $f \n"
	python $Directory/PrimaryCode.py <<EOF
$f
EOF
	python $Directory/printEmail.py <<EOF
$f
EOF

	python $Directory/printAff.py <<EOF
$f
EOF



# rm "${f%.*}""_mail_parse.txt"
# rm "${f%.*}""_parse.txt"

done



# python Integrated_Code.py <<EOF
# acl1
# EOF


# python Integrated_Code.py <<EOF
# acl2
# EOF

# python Integrated_Code.py <<EOF
# acm_journal1
# EOF


# python Integrated_Code.py <<EOF
# acm_journal2
# EOF


# python Integrated_Code.py <<EOF
# ACM-sig1
# EOF


# python Integrated_Code.py <<EOF
# ACM-sig2
# EOF


# python Integrated_Code.py <<EOF
# ACM-sig3
# EOF


# python Integrated_Code.py <<EOF
# arxiv1
# EOF


# python Integrated_Code.py <<EOF
# arxiv2
# EOF


# python Integrated_Code.py <<EOF
# chi1
# EOF

# python Integrated_Code.py <<EOF
# chi2
# EOF


# python Integrated_Code.py <<EOF
# elsevier1
# EOF


# python Integrated_Code.py <<EOF
# elsevier2
# EOF


# python Integrated_Code.py <<EOF
# ieee1
# EOF


# python Integrated_Code.py <<EOF
# ieee2
# EOF


# python Integrated_Code.py <<EOF
# ieee3
# EOF


# python Integrated_Code.py <<EOF
# ieee_journal1
# EOF


# python Integrated_Code.py <<EOF
# ieee_journal2
# EOF


# python Integrated_Code.py <<EOF
# Springer1
# EOF


# python Integrated_Code.py <<EOF
# Springer2
# EOF

# echo "Parses Done\n"

# rm AllAffiliations.txt

# python printEmail.py <<EOF
# acl1
# EOF
# rm acl1_mail_parse.txt


# python printEmail.py <<EOF
# acl2
# EOF
# rm acl2_mail_parse.txt

# python printEmail.py <<EOF
# acm_journal1
# EOF
# rm acm_journal1_mail_parse.txt

# python printEmail.py <<EOF
# acm_journal2
# EOF
# rm acm_journal2_mail_parse.txt

# python printEmail.py <<EOF
# ACM-sig1
# EOF
# rm ACM-sig1_mail_parse.txt

# python printEmail.py <<EOF
# ACM-sig2
# EOF
# rm ACM-sig2_mail_parse.txt

# python printEmail.py <<EOF
# ACM-sig3
# EOF
# rm ACM-sig3_mail_parse.txt

# python printEmail.py <<EOF
# arxiv1
# EOF
# rm arxiv1_mail_parse.txt

# python printEmail.py <<EOF
# arxiv2
# EOF
# rm arxiv2_mail_parse.txt

# python printEmail.py <<EOF
# chi1
# EOF
# rm chi1_mail_parse.txt

# python printEmail.py <<EOF
# chi2
# EOF
# rm chi2_mail_parse.txt

# python printEmail.py <<EOF
# elsevier1
# EOF
# rm elsevier1_mail_parse.txt

# python printEmail.py <<EOF
# elsevier2
# EOF
# rm elsevier2_mail_parse.txt

# python printEmail.py <<EOF
# ieee1
# EOF
# rm ieee1_mail_parse.txt

# python printEmail.py <<EOF
# ieee2
# EOF
# rm ieee2_mail_parse.txt

# python printEmail.py <<EOF
# ieee3
# EOF
# rm ieee3_mail_parse.txt

# python printEmail.py <<EOF
# ieee_journal1
# EOF
# rm ieee_journal1_mail_parse.txt

# python printEmail.py <<EOF
# ieee_journal2
# EOF
# rm ieee_journal2_mail_parse.txt

# python printEmail.py <<EOF
# Springer1
# EOF
# rm Springer1_mail_parse.txt

# python printEmail.py <<EOF
# Springer2
# EOF
# rm Springer2_mail_parse.txt

# rm Allmails.txt


# python printAff.py <<EOF
# acl1
# EOF
# rm acl1_parse.txt


# python printAff.py <<EOF
# acl2
# EOF
# rm acl2_parse.txt

# python printAff.py <<EOF
# acm_journal1
# EOF
# rm acm_journal1_parse.txt

# python printAff.py <<EOF
# acm_journal2
# EOF
# rm acm_journal2_parse.txt

# python printAff.py <<EOF
# ACM-sig1
# EOF
# rm ACM-sig1_parse.txt

# python printAff.py <<EOF
# ACM-sig2
# EOF
# rm ACM-sig2_parse.txt

# python printAff.py <<EOF
# ACM-sig3
# EOF
# rm ACM-sig3_parse.txt

# python printAff.py <<EOF
# arxiv1
# EOF
# rm arxiv1_parse.txt

# python printAff.py <<EOF
# arxiv2
# EOF
# rm arxiv2_parse.txt

# python printAff.py <<EOF
# chi1
# EOF
# rm chi1_parse.txt

# python printAff.py <<EOF
# chi2
# EOF
# rm chi2_parse.txt

# python printAff.py <<EOF
# elsevier1
# EOF
# rm elsevier1_parse.txt

# python printAff.py <<EOF
# elsevier2
# EOF
# rm elsevier2_parse.txt

# python printAff.py <<EOF
# ieee1
# EOF
# rm ieee1_parse.txt

# python printAff.py <<EOF
# ieee2
# EOF
# rm ieee2_parse.txt

# python printAff.py <<EOF
# ieee3
# EOF
# rm ieee3_parse.txt

# python printAff.py <<EOF
# ieee_journal1
# EOF
# rm ieee_journal1_parse.txt

# python printAff.py <<EOF
# ieee_journal2
# EOF
# rm ieee_journal2_parse.txt

# python printAff.py <<EOF
# Springer1
# EOF
# rm Springer1_parse.txt

# python printAff.py <<EOF
# Springer2
# EOF
# rm Springer2_parse.txt




# echo "Emails printed"
# gedit Allmails.txt &
# gedit AllAffiliations.txt &