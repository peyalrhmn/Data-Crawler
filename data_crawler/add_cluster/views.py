import json
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import response
from add_cluster.models import Create_cluster
#from add_cluster.models import Search_cluster
from add_cluster.serialize import Create_cluster_serialize
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests
import bs4
from bs4 import BeautifulSoup
import numpy
import pandas
import mysql.connector
import mysql
import urllib.request
from IPython.display import HTML
import re
from django.views.generic import TemplateView
import PyPDF2
from urllib.request import unquote
from PyPDF2 import PdfFileReader
from pathlib import Path
from tika import parser
import pdfminer
import os
from urllib.parse import urljoin
import django.utils

# Create your views here.

#def searchcluster(request):
#    return render(request, 'add_cluster/searchclusters.html')

#def searchresult(request):
    #return render(request, 'add_cluster/searchresult.html')

#class dcrawler(TemplateView):

@api_view(['POST'])
def save_cluster(request):
    if request.method=="POST":
        saveserialize=Create_cluster_serialize(data=request.data)
        if saveserialize.is_valid():
            saveserialize.save()
            return Response(saveserialize.data, status=status.HTTP_201_CREATED)
        return Response(saveserialize.data, status=status.HTTP_400_BAD_REQUEST)

def depth_crawling_html(url, maxdepth, cluster_name):
    dep = 0
    links = []
    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser")
         
    for link in soup.findAll(attrs={'href': re.compile("http")}):
        links.append(link.get('href'))
        print(link.get('href'))
        
        try:
            res = requests.get(link.get('href'))
            soup = BeautifulSoup(res.text, "html.parser")
            allcont = (soup.prettify())
            print(allcont)
                
            db = mysql.connector.connect(user="root", database="data_crawler")
                
            cursor = db.cursor()
                
            addcluster = ("INSERT INTO data (cluster_name, url, data) VALUES (%s, %s, %s);")
                
            insrtclstr = (cluster_name, link.get('href'), allcont)
                
            cursor.execute(addcluster, insrtclstr)
                
            db.commit()
            cursor.close()
            db.close()
        
        except:
            pass
        
    depth = dep +1
    if depth < int(maxdepth):
        for lin in links:
            depth_crawling_html(lin,depth,cluster_name)
            
            
def depth_crawling_text(url, maxdepth, cluster_name):
    dep = 0
    links = []
    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser")
         
    for link in soup.findAll(attrs={'href': re.compile("http")}):
        links.append(link.get('href'))
        print(link.get('href'))
        
        try:
            r = urllib.request.urlopen(link.get('href')).read()

            soup = BeautifulSoup(r, "lxml")
            [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
            visible_text = soup.getText()
            print(visible_text)         
            
            db = mysql.connector.connect(user="root", database="data_crawler")
            cursor = db.cursor()
            
            addcluster = ("INSERT INTO data (cluster_name, url, data) VALUES (%s, %s, %s)")
            
            insrtclstr = (cluster_name, url, visible_text)
            
            cursor.execute(addcluster, insrtclstr)
            
            db.commit()
            cursor.close()
            db.close()
        
        except:
            pass
        
    depth = dep +1
    if depth < int(maxdepth):
        for lin in links:
            depth_crawling_text(lin,depth,cluster_name)
            
            
def depth_crawling_pdf(url, maxdepth, cluster_name):
    dep = 0
    links = []
    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser")
         
    for link in soup.findAll(attrs={'href': re.compile("http")}):
        links.append(link.get('href'))
        print(link.get('href'))
        
        #try:
        #pdftxt = ''
            
        #If there is no such folder, the script will create one automatically
        folder_location = r'./pdf/'
        if not os.path.exists(folder_location):os.mkdir(folder_location)

        resp = requests.get(link.get('href'))
        soup1 = BeautifulSoup(resp.text, "html.parser")     
        for l in soup1.select("a[href$='.pdf']"):
            pt = ''
            li = str(l)
            #Name the pdf files using the last portion of each link which are unique in this case
            filename = os.path.join(folder_location,l['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(url,l['href'])).content)
                raw = parser.from_file(filename)
                pt = str(raw['content'])
                print(pt)
                db = mysql.connector.connect(user="root", database="data_crawler")
                
                cursor = db.cursor()
                    
                addcluster = ("INSERT INTO data (cluster_name, url, data) VALUES (%s, %s, %s)")
                    
                insrtclstr = (cluster_name, li, pt)
                    
                cursor.execute(addcluster, insrtclstr)
                    
                db.commit()
                cursor.close()
                db.close()
            #pdftxt += pt
      
        #except:
            #pass

    depth = dep +1
    if depth < int(maxdepth):
        for lin in links:
            depth_crawling_pdf(lin,depth,cluster_name)
            
            
def depth_crawling_doc(url, maxdepth, cluster_name):
    dep = 0
    links = []
    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser")
         
    for link in soup.findAll(attrs={'href': re.compile("http")}):
        links.append(link.get('href'))
        print(link.get('href'))
        
        #try:
        #pdftxt = ''
            
        #If there is no such folder, the script will create one automatically
        folder_location = r'./doc/'
        if not os.path.exists(folder_location):os.mkdir(folder_location)

        resp = requests.get(link.get('href'))
        soup1 = BeautifulSoup(resp.text, "html.parser")
             
        for l in soup1.select("a[href$='.doc']"):
            pt = ''
            li = str(l)
            #Name the pdf files using the last portion of each link which are unique in this case
            filename = os.path.join(folder_location,l['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(url,l['href'])).content)
                raw = parser.from_file(filename)
                pt = str(raw['content'])
                print(pt)
                db = mysql.connector.connect(user="root", database="data_crawler")
                
                cursor = db.cursor()
                    
                addcluster = ("INSERT INTO data (cluster_name, url, data) VALUES (%s, %s, %s)")
                    
                insrtclstr = (cluster_name, li, pt)
                    
                cursor.execute(addcluster, insrtclstr)
                    
                db.commit()
                cursor.close()
                db.close()
                
        for l in soup1.select("a[href$='.docx']"):
            ptt = ''
            li = str(l)
            #Name the pdf files using the last portion of each link which are unique in this case
            filename = os.path.join(folder_location,l['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(url,l['href'])).content)
                raw = parser.from_file(filename)
                ptt = str(raw['content'])
                print(ptt)
                db = mysql.connector.connect(user="root", database="data_crawler")
                
                cursor = db.cursor()
                    
                addcluster = ("INSERT INTO data (cluster_name, url, data) VALUES (%s, %s, %s)")
                    
                insrtclstr = (cluster_name, li, ptt)
                    
                cursor.execute(addcluster, insrtclstr)
                    
                db.commit()
                cursor.close()
                db.close()
            #pdftxt += pt
      
        #except:
            #pass

    depth = dep +1
    if depth < int(maxdepth):
        for lin in links:
            depth_crawling_doc(lin,depth,cluster_name)
            
            
            
def depth_crawling_all(url, maxdepth, cluster_name):
    dep = 0
    links = []
    response = requests.get(url)
    soup= BeautifulSoup(response.text, "html.parser")
         
    for link in soup.findAll(attrs={'href': re.compile("http")}):
        links.append(link.get('href'))
        print(link.get('href'))
        
        #try:
        #pdftxt = ''
            
        #If there is no such folder, the script will create one automatically
        folder_location = r'./doc/'
        if not os.path.exists(folder_location):os.mkdir(folder_location)

        resp = requests.get(link.get('href'))
        soup1 = BeautifulSoup(resp.text, "html.parser")
        
        for l in soup1.select("a[href$='.pdf']"):
            st = ''
            li = str(l)
            #Name the pdf files using the last portion of each link which are unique in this case
            filename = os.path.join(folder_location,l['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(url,l['href'])).content)
                raw = parser.from_file(filename)
                st = str(raw['content'])
                print(st)
                db = mysql.connector.connect(user="root", database="data_crawler")
                
                cursor = db.cursor()
                    
                addcluster = ("INSERT INTO data (cluster_name, url, data) VALUES (%s, %s, %s)")
                    
                insrtclstr = (cluster_name, li, st)
                    
                cursor.execute(addcluster, insrtclstr)
                    
                db.commit()
                cursor.close()
                db.close()
             
        for l in soup1.select("a[href$='.doc']"):
            pt = ''
            li = str(l)
            #Name the pdf files using the last portion of each link which are unique in this case
            filename = os.path.join(folder_location,l['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(url,l['href'])).content)
                raw = parser.from_file(filename)
                pt = str(raw['content'])
                print(pt)
                db = mysql.connector.connect(user="root", database="data_crawler")
                
                cursor = db.cursor()
                    
                addcluster = ("INSERT INTO data (cluster_name, url, data) VALUES (%s, %s, %s)")
                    
                insrtclstr = (cluster_name, li, pt)
                    
                cursor.execute(addcluster, insrtclstr)
                    
                db.commit()
                cursor.close()
                db.close()
                
        for l in soup1.select("a[href$='.docx']"):
            ptt = ''
            li = str(l)
            #Name the pdf files using the last portion of each link which are unique in this case
            filename = os.path.join(folder_location,l['href'].split('/')[-1])
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin(url,l['href'])).content)
                raw = parser.from_file(filename)
                ptt = str(raw['content'])
                print(ptt)
                db = mysql.connector.connect(user="root", database="data_crawler")
                
                cursor = db.cursor()
                    
                addcluster = ("INSERT INTO data (cluster_name, url, data) VALUES (%s, %s, %s)")
                    
                insrtclstr = (cluster_name, li, ptt)
                    
                cursor.execute(addcluster, insrtclstr)
                    
                db.commit()
                cursor.close()
                db.close()
            #pdftxt += pt
      
        #except:
            #pass

    depth = dep +1
    if depth < int(maxdepth):
        for lin in links:
            depth_crawling_all(lin,depth,cluster_name)    
             

@login_required()
def insert_clusters(request):
    
    if request.method == "POST":
        cluster_name = request.POST.get('cluster_name')
        depth = request.POST.get('depth')
        strategy = request.POST.get('strategy')
        user_name = request.POST.get('user_name')
        url = request.POST.get('url')
        data = {'cluster_name':cluster_name, 'depth':depth, 'strategy':strategy, 'user_name':user_name, 'url':url}
        headers = {'Content-Type': 'application/json'}
        read = requests.post('http://127.0.0.1:8000/Createclusterapi', json=data, headers=headers)
        
        #print(strategy)

        if strategy == "txtonly":
            depth_crawling_text(url, depth, cluster_name)
            return render(request, 'add_cluster/searchclusters.html')
        
        elif strategy == "html":
            depth_crawling_html(url, depth, cluster_name)
            return render(request, 'add_cluster/searchclusters.html')
        
        elif strategy == "pdfonly":
            depth_crawling_pdf(url, depth, cluster_name)
            return render(request, 'add_cluster/searchclusters.html')
        
        elif strategy == "doconly":
            depth_crawling_doc(url, depth, cluster_name)
            return render(request, 'add_cluster/searchclusters.html')
        
        elif strategy == "all":
            depth_crawling_all(url, depth, cluster_name)
            return render(request, 'add_cluster/searchclusters.html')         
    
    else:
        return render(request, 'add_cluster/searchclusters.html')
    
@login_required()
def new_url(request):
    
    if request.method == "POST":
        
        cluster_name_n = request.POST.get('cluster_name_n')
        url_n = request.POST.get('url_n')
        depth_n = request.POST.get('depth_n')
                        
        db = mysql.connector.connect(user="root", database="data_crawler")
        cursor = db.cursor(buffered=True)
                        
        #rslt_qry = ("SELECT data FROM htmldata WHERE url=%s;")
                                
        #get_rslt = (cluster_name_n)
                                
        cursor.execute("SELECT strategy FROM clusters WHERE cluster_name=%s", (cluster_name_n,))
                        
        re = ""
        res = ""
                        
        re = (cursor.fetchall())

        for row in re:
            res = row[0]
            print(row[0])
                        
        db.commit()
        cursor.close()
        db.close()
           
        if res == "txtonly":
            depth_crawling_text(url_n, depth_n, cluster_name_n)
            return render(request, 'add_cluster/searchclusters.html')
        
        elif res == "html":
            depth_crawling_html(url_n, depth_n, cluster_name_n)
            return render(request, 'add_cluster/searchclusters.html')
        
        elif res == "pdfonly":
            depth_crawling_pdf(url_n, depth_n, cluster_name_n)
            return render(request, 'add_cluster/searchclusters.html')
        
        elif res == "doconly":
            depth_crawling_doc(url_n, depth_n, cluster_name_n)
            return render(request, 'add_cluster/searchclusters.html')
        
        elif res == "all":
            depth_crawling_all(url_n, depth_n, cluster_name_n)
            return render(request, 'add_cluster/searchclusters.html')
        
        return render(request, 'add_cluster/newurl.html')
        
    else:
        return render(request, 'add_cluster/newurl.html')
        
@login_required()       
def search(request):
    
    if request.method == "POST":
        try:
            cluster_name = request.POST.get('cluster_name')
            keyword = request.POST.get('keyword')

            db = mysql.connector.connect(user="root", database="data_crawler")
            cursor = db.cursor(buffered=True)
            cursor_2 = db.cursor(buffered=True)
            
            rslt_qry_1 = ("SELECT data FROM data WHERE cluster_name=%s AND MATCH(cluster_name, data, url) AGAINST (%s IN NATURAL LANGUAGE MODE);")
                
            get_rslt = (cluster_name, keyword)
                
            cursor.execute(rslt_qry_1, get_rslt)
            
            rslt_qry_2 = ("SELECT url FROM data WHERE cluster_name=%s AND MATCH(cluster_name, data, url) AGAINST (%s IN NATURAL LANGUAGE MODE);")
            
            cursor_2.execute(rslt_qry_2, get_rslt)
            
            myresult_2 = ''
            
            myresult_2 = (cursor_2.fetchall())
            
            for row in myresult_2:
                u = row[0]
            print(row[0])
            
            #print(myresult_2)
            
            #cursor.execute("SELECT data FROM data WHERE cluster_name='Test10' AND MATCH(cluster_name, data, url) AGAINST ('Carrick' IN NATURAL LANGUAGE MODE);")
            
            myresult = ''
            
            myresult = str(cursor.fetchall())
            
            result = ''
            
            result = (myresult.index(keyword))
            fin_rslt = (myresult[(result -50):result+50])
            
            #print(fin_rslt)
            
            #print(myresult[(result -100):result+100])
            
            #print(myresult)
            
            #for x in myresult:
            #    print(x)
            
            db.commit()
            cursor.close()
            db.close()
            
            context = {}
            
            context['srch_rslt'] = fin_rslt
            context['rslt_url'] = u
            
            return render(request, 'add_cluster/searchresult.html', context)
        
        except:
            pass
        
        return render(request, 'add_cluster/searchresult.html')
        
    else:
        return render(request, 'add_cluster/searchresult.html')

"""

def search_result(request):
    
    if request.method == "POST":
        
        cluster_name = request.POST.get('cluster_name')
        keyword = request.POST.get('keyword')
        
        db = mysql.connector.connect(user="root", database="data_crawler")
        cursor = db.cursor()
        
        rslt_qry = ("SELECT data FROM data WHERE cluster_name=%s AND MATCH(cluster_name, data, url) AGAINST (%s IN NATURAL LANGUAGE MODE);")
            
        get_rslt = (cluster_name, keyword)
            
        cursor.execute(rslt_qry, get_rslt)
        
        #cursor.execute("SELECT data FROM data WHERE MATCH(cluster_name, data, url) AGAINST (keyword IN NATURAL LANGUAGE MODE);")
        
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)
            
        return render(request, 'add_cluster/searchresult.html')
    
    else:
        return render(request, 'add_cluster/searchresult.html')
"""


def home(request):
    return render(request, 'add_cluster/home.html')


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'add_cluster/register.html', {'form': form})


@login_required()
def profile(request):
    return render(request, 'add_cluster/profile.html')


@login_required()
def add_cluster(request):
    return render(request, 'add_cluster/searchclusters.html')
