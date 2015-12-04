# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import glob

from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm
import subprocess
from subprocess import Popen, PIPE

script_dir = "/home/priyank/Desktop/SNLP_Project/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/myapp/"

directory = "/home/priyank/Desktop/SNLP_Project/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/";

def runScript(request):
    file_name = glob.glob(directory+'*.pdf')
    # print file_name[0] + "****************************"
    fn = file_name[0].split('/')
    fn = fn[-1]
    subprocess.call("clear", shell=True)
    subprocess.call("mv " + directory + fn + " " + directory + "input.pdf", shell=True)
    subprocess.call(directory + "files/pdftoxml.linux64.exe.1.2_7 " + directory + "input.pdf", shell=True)
    
    # barno
    subprocess.call("python " + directory + "files/TitleAuthor_parse.py", shell=True)
    subprocess.call("python " + directory + "files/extra.py", shell=True)
    subprocess.call("crf_test -m " + directory + "files/model_new.txt " + directory + "test_file.txt > " + directory + "final.txt", shell=True)
    subprocess.call("python " + directory + "files/printNameAuthor.py > " + directory + "TitleAuthor.txt", shell=True)
    # barno

    #samuel
    subprocess.call("rm " + directory + "input.pdf", shell=True)
    subprocess.call("rm -r " + directory + "input.xml_data", shell=True)
    subprocess.call("python " + directory + "files/Secmapping.py > " + directory + "Secmap.txt", shell=True)
    #samuel

    #integrated
    subprocess.call(directory + "IntegratedShellScript.sh ", shell=True)
    #integrated

    
    subprocess.call(directory + "Mapping.sh",shell = True)

    #ayush
    subprocess.call("python " + directory + "url.py > " + directory + "URLop.txt", shell=True)
    subprocess.call("python " + directory + "footnotes.py > " + directory + "FOOTNOTEop.txt", shell=True)
    subprocess.call("python " + directory + "tables_figures.py > " + directory + "TABFIGop.txt", shell=True)
    subprocess.call("rm " + directory + "input.xml", shell=True)
    
    # subprocess.call(directory + "Clean.sh",shell = True)

    return HttpResponse("Done")
    
def list(request):
    if request.method == 'GET':
        # return HttpResponse('This page shows a list of most recent posts.')
        pass
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('myproject.myapp.views.list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # print len(documents)
    # print
    # print
    # print Document.objects.values()

    


    # Render list page with the documents and the form
    return render_to_response(
        'myapp/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
