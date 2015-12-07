# -*- coding: utf-8 -*-
from django.db import models

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/')

class UserDetails(models.Model):
	"""docstring for rPapers"""
	paperid = models.IntegerField()
	userid = models.CharField(max_length= 100)
	user_email = models.EmailField()
	def __str__(self):
		return self.paperid

class Response(models.Model):
	"""docstring for response"""
	userdetails = models.ForeignKey(UserDetails)
	title = models.IntegerField()
	authorNames = models.IntegerField()
	urls = models.IntegerField()
	email = models.IntegerField()
	affiliation = models.IntegerField()
	references = models.IntegerField()
	sections = models.IntegerField()
	emailAuthMap = models.IntegerField()
	figHeading = models.IntegerField()
	Footnotes = models.IntegerField()
	TableHeading = models.IntegerField()
	citToRef = models.IntegerField()

	def __str__(self):
		return self.title
