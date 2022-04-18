from django.shortcuts import render
from demoSite.models import LoopModel, ProcessedData, ExampleLoopModel
import pandas as pd
from django.db.models import Q

def browselooppage(request):
    allcelltype = sorted(set(ProcessedData.objects.filter(experiment__in=['HiC',"ChIAPET","HiChIP"]).values_list('cell',flat=True)))

    if request.GET and set(request.GET.dict().values()) != {''}:
        datadict = request.GET
        print(set(datadict.dict().values()))

        condition = {}
        regionObjects = None
        filterconditions = "Current Filters: "

        if datadict['one-anchor']:
            chrom = datadict['one-anchor'].split(":")[0]
            start = datadict['one-anchor'].split(":")[1].split("-")[0]
            end = datadict['one-anchor'].split(":")[1].split("-")[1]

            regionObjects = LoopModel.objects.filter(Q(chrom1=chrom,start1__gte=start,end1__lte=end) | Q(chrom2=chrom,start2__gte=start,end2__lte=end))
            filterconditions += datadict['one-anchor'] + ";"
        elif datadict['two-anchor-1'] and datadict['two-anchor-2']:
            chrom1 = datadict['two-anchor-1'].split(":")[0]
            start1 = datadict['two-anchor-1'].split(":")[1].split("-")[0]
            end1 = datadict['two-anchor-1'].split(":")[1].split("-")[1]
            chrom2 = datadict['two-anchor-2'].split(":")[0]
            start2 = datadict['two-anchor-2'].split(":")[1].split("-")[0]
            end2 = datadict['two-anchor-2'].split(":")[1].split("-")[1]

            regionObjects = LoopModel.objects.filter(chrom1=chrom1,start1__gte=start1,end1__lte=end1,chrom2=chrom2,start2__gte=start2,end2__lte=end2)
            filterconditions += datadict['two-anchor-1'] + ";" + datadict['two-anchor-2'] + ";"
        elif datadict['two-anchor-1'] and not datadict['two-anchor-2']:
            return render(request,'demoSite/error.html',{'section':'error'})
        elif datadict['two-anchor-2'] and not datadict['two-anchor-1']:
            return render(request,'demoSite/error.html',{'section':'error'})

        if datadict['assay-type']:
            condition['assay__contains'] = datadict['assay-type']
            filterconditions += datadict['assay-type'] + ";"

        if datadict['cell-type']:
            condition['celltype__contains'] = datadict['cell-type']
            filterconditions += datadict['cell-type'] + ";"

        '''
        if regionObjects:
            selectloop = regionObjects.filter(**condition)
        else:
            information1 = 'Display all cohesin-interactions without specific region will be extremely slow. Please add more filters.'
            information2 = 'If you really want to check all cohesin-interactions, please go to <a href="/download">download</a> page or <a href="/data">data</a> page'
            backlink = "/browseloop/"
            return render(request,'demoSite/error.html',{'section':'error','information1':information1,'information2':information2,
                                                        'backlink':backlink})
        '''
        if regionObjects:
            selectloop = regionObjects.filter(**condition)
        else:
            selectloop = LoopModel.objects.filter(**condition)

        if selectloop.count()>5000:
            information1 = 'Search results exceeded 5,000'
            information2 = 'Too many entities will make the page extremely slow. Alternatively, you can download all cohesin information in <a href="/download/">Download</a> page.'
            backlink = "/browseloop/"
            return render(request,'demoSite/error.html',{'section':'error','information1':information1,'information2':information2,
                                                        'backlink':backlink})

    else:
        selectloop = ExampleLoopModel.objects.all()
        filterconditions = "Default Filters: " + "one-anchor chr21:16000000-16500000;"

    #loopcount
    loopcount = selectloop.count()
    #studycount
    studyquery = set(list(selectloop.values_list("study",flat=True)))
    studyquerylist = []
    for i in studyquery:
        studyquerylist += i.split(",")
    studycount=len(set(studyquerylist))

    #assay
    assayquery = selectloop.values_list('assay',flat=True)
    assayquerylist = []
    for i in assayquery:
        assayquerylist += i.split(",")
    assayquerypd = pd.value_counts(assayquerylist)
    #modifiedindex = ["Non-dependent" if i=="." else i+"-dependent" for i in typequerypd.index]
    assaytypes = {"index":list(assayquerypd.index),"values":list(assayquerypd.values),}

    #subunit
    subunitquery = selectloop.values_list('subunit',flat=True)
    subunitquerylist = []
    for i in subunitquery:
        subunitquerylist += i.split(",")
    subunitquerypd = pd.value_counts(subunitquerylist)
    subunittypes = {"index":list(subunitquerypd.index),"values":list(subunitquerypd.values),}

    #celltype
    lengthquery = selectloop.values_list('looplength',flat=True)
    lengthquerylist = []
    for i in lengthquery:
        if i<=500:
            lengthquerylist.append("<0.2Mb")
        elif i>500 and i<=1000:
            lengthquerylist.append("0.2~1Mb")
        else:
            lengthquerylist.append(">1Mb")
    lengthquerypd = pd.value_counts(lengthquerylist)
    lengthtypes = {"index":list(lengthquerypd.index),"values":list(lengthquerypd.values),}


    return render(request,'demoSite/browsepage/browseloop.html',{'section':'browse','selectloop':selectloop,
                                                                'loopcount':loopcount,'studycount':studycount,
                                                                'assaytypes':assaytypes,'subunittypes':subunittypes,
                                                                'lengthtypes':lengthtypes,'allcelltype':allcelltype,
                                                                'filterconditions':filterconditions,})
