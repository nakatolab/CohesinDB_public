from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from demoSite.models import ProcessedData, UpdateNew, GeneModel, PeakModel
import pandas as pd
import numpy as np

def errorpage(request):
    return render(request,'demoSite/error.html',{'section':'error'})

def pipelinepage(request):
    return render(request,'demoSite/helppage/pipeline.html',{'section':'help'})
