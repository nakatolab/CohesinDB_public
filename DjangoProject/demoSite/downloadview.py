from django.http import HttpResponse
import os
from demoSite.models import ProcessedData
#import pandas as pd

def datadownload1(request,dataid):
    dataset = ProcessedData.objects.get(id=dataid)
    file = open(str(dataset.content1),'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename='+os.path.basename(str(dataset.content1))
    return response

def datadownload2(request,dataid):
    dataset = ProcessedData.objects.get(id=dataid)
    file = open(str(dataset.content2),'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename='+os.path.basename(str(dataset.content2))
    return response

def analyze1(request):
  file = open('tmpfile/Analyze1_output.csv','rb')
  response = HttpResponse(file)
  response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
  response['Content-Disposition'] = 'attachment;filename='+"Gene-Cohesin-TFs.csv"
  return response

def analyze2(request):
  file = open('tmpfile/Analyze2_output.csv','rb')
  response = HttpResponse(file)
  response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
  response['Content-Disposition'] = 'attachment;filename='+"Cohesin-Gene-Pathway.csv"
  return response

def analyze2_2(request):
  file = open('tmpfile/Analyze2_2_output.csv','rb')
  response = HttpResponse(file)
  response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
  response['Content-Disposition'] = 'attachment;filename='+"PathwayDetail.csv"
  return response

def analyze3(request):
  file = open('tmpfile/Analyze3_output.csv','rb')
  response = HttpResponse(file)
  response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
  response['Content-Disposition'] = 'attachment;filename='+"Full_Simpson_list.csv"
  return response

def downAllObject(request,filename):
  file = open('/mnt/NAS/WangDB/Production_data/'+filename,'rb')
  response = HttpResponse(file)
  response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
  response['Content-Disposition'] = 'attachment;filename='+filename
  return response
