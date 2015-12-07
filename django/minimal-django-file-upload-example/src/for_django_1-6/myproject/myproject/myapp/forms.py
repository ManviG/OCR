# -*- coding: utf-8 -*-
from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
class user(forms.Form):
	paperid = forms.IntegerField()
	email = forms.EmailField()
	title = forms.IntegerField()
	authorNames = forms.IntegerField()
	urls = forms.IntegerField()
	email = forms.IntegerField()
	affiliation = forms.IntegerField()
	references = forms.IntegerField()
	sections = forms.IntegerField()
	emailAuthMap = forms.IntegerField()
	figHeading = forms.IntegerField()
	Footnotes = forms.IntegerField()
	TableHeading = forms.IntegerField()
	citToRef = forms.IntegerField()

