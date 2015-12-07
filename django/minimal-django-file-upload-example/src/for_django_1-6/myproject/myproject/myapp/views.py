# -*- coding: utf-8 -*-
from __future__ import division

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import glob

from myproject.myapp.models import Document
from myproject.myapp.models import Response, UserDetails
from myproject.myapp.forms import DocumentForm
# from myproject.myapp.forms import user
import subprocess
from subprocess import Popen, PIPE

script_dir = "/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/myapp/"

directory = "/var/www/html/OCR++/django/minimal-django-file-upload-example/src/for_django_1-6/myproject/myproject/media/documents/";

def vote(request):
    uemail = request.POST['email'];
    
    noAut = request.POST['noAut'];
    c=0 
    w=0
    for i in range(int(noAut)):
        a = request.POST['author'+str(i+1)]
        if (a=="correct" or a=="partial"):
            c=c+1
        else:
            w=w+1
    c = c/1.0
    w = w/1.0
    if c<1 and w<1:
        aut = 0
    else:
        aut = c/(c+w)

    a = request.POST['title']
    if (a=="correct" or a=="partial"):
        title = 1
    else:
        title = 0

    noEmail = request.POST['noEmail'];
    c=0 
    w=0
    for i in range(int(noEmail)):
        a = request.POST['email'+str(i+1)]
        if (a=="correct" or a=="partial"):
            c=c+1
        else:
            w=w+1
    c = c/1.0
    w = w/1.0
    if c<1 and w<1:
        email = 0
    else:
        email = c/(c+w)

    noAffil = request.POST['noAffil'];
    print noAffil
    c=0 
    w=0
    for i in range(int(noAffil)):
        a = request.POST['affil'+str(i+1)]
        if (a=="correct" or a=="partial"):
            c=c+1
        else:
            w=w+1
    c = c/1.0
    w = w/1.0
    if c<1 and w<1:
        affil = 0
    else:
        affil = c/(c+w)

    noMap = request.POST['noMap'];
    c=0 
    w=0
    for i in range(int(noMap)):
        a = request.POST['map'+str(i+1)]
        if (a=="correct" or a=="partial"):
            c=c+1
        else:
            w=w+1
    c = c/1.0
    w = w/1.0
    if c<1 and w<1:
        mapp = 0
    else:
        mapp = c/(c+w)

    noFig = request.POST['noFig'];
    c=0 
    w=0
    for i in range(int(noFig)):
        a = request.POST['fig'+str(i+1)]
        if (a=="correct" or a=="partial"):
            c=c+1
        else:
            w=w+1
    c = c/1.0
    w = w/1.0
    if c<1 and w<1:
        fig = 0
    else:
        fig = c/(c+w)

    noTab = request.POST['noTab'];
    c=0 
    w=0
    for i in range(int(noTab)):
        a = request.POST['tab'+str(i+1)]
        if (a=="correct" or a=="partial"):
            c=c+1
        else:
            w=w+1
    c = c/1.0
    w = w/1.0
    if c<1 and w<1:
        tab = 0
    else:
        tab = c/(c+w)

    noSec = request.POST['noSec'];
    c=0 
    w=0
    for i in range(int(noSec)):
        a = request.POST['sec'+str(i+1)]
        if (a=="correct" or a=="partial"):
            c=c+1
        else:
            w=w+1
    c = c/1.0
    w = w/1.0
    if c<1 and w<1:
        sec = 0
    else:
        sec = c/(c+w)

    noUrl = request.POST['noUrl'];
    c=0 
    w=0
    for i in range(int(noUrl)):
        a = request.POST['url'+str(i+1)]
        if (a=="correct" or a=="partial"):
            c=c+1
        else:
            w=w+1
    c = c/1.0
    w = w/1.0
    if c<1 and w<1:
        url = 0
    else:
        url = c/(c+w)

    noFn = request.POST['noFn'];
    c=0 
    w=0
    for i in range(int(noFn)):
        a = request.POST['fn'+str(i+1)]
        if (a=="correct" or a=="partial"):
            c=c+1
        else:
            w=w+1
    c = c/1.0
    w = w/1.0
    if c<1 and w<1:
        fn = 0
    else:
        fn = c/(c+w)

        pid = len(all_entries)+1

    p = Response(paperid=pid,user_email=uemail,title=title,authorNames=aut,urls=url,email=email,affiliation=affil,sections=sec,emailAuthMap=mapp,figHeading=fig,Footnotes=fn,TableHeading=tab);
    p.save()
    all_entries = Response.objects.all();
    print len(all_entries);

    subprocess.call("mv " + directory + "input.pdf " + directory + str(len(all_entries))+".pdf", shell=True)
    subprocess.call("mv " + directory + str(len(all_entries)+1) + ".pdf " + directory + "input.pdf", shell=True)

    return HttpResponse("Done")

def runScript(request):
    # subprocess.call("rm " + directory + "input.pdf", shell=True)
    # file_name = glob.glob(directory+'*.pdf')
    # print file_name[0] + "****************************"
    # fn = file_name[0].split('/')
    # fn = fn[-1]
    subprocess.call("clear", shell=True)
    # subprocess.call("mv " + directory + fn + " " + directory + "input.pdf", shell=True)
    subprocess.call(directory + "files/pdftoxml.linux64.exe.1.2_7 " + directory + "input.pdf", shell=True)
    
    # barno
    subprocess.call("python " + directory + "files/TitleAuthor_parse.py", shell=True)
    subprocess.call("python " + directory + "files/extra.py", shell=True)
    subprocess.call("crf_test -m " + directory + "files/model_new.txt " + directory + "test_file.txt > " + directory + "final.txt", shell=True)
    subprocess.call("python " + directory + "files/printNameAuthor.py > " + directory + "TitleAuthor.xml", shell=True)
    # barno

    #samuel
    # subprocess.call("rm " + directory + "input.pdf", shell=True)
    subprocess.call("rm -r " + directory + "input.xml_data", shell=True)
    subprocess.call("python " + directory + "files/Secmapping.py > " + directory + "Secmap.xml", shell=True)
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
   
    subprocess.call(directory + "eval_op.sh",shell = True)

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
