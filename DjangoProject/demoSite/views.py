from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from demoSite.models import ProcessedData, UpdateNew, GeneModel, PeakModel, ExamplePeakModel, ExampleGeneModel
import os, subprocess, time
import json
import pandas as pd
import numpy as np
from pybedtools import BedTool
from .custom import merge
import gseapy
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def homepage(request):
    queryset = ProcessedData.objects.values_list('experiment',flat=True)
    countexp = pd.value_counts(queryset)
    label_all = list(countexp.index)
    data_all = list(countexp.values)

    #count_target = pd.value_counts(ProcessedData.objects.filter(modules='cohesin-binding').values_list('experiment',flat=True))
    #label_target = list(count_target.index)
    #data_target = list(count_target.values)
    label_target = ['Cohesin-sites','Cohesin-loops','Cohesin-gene-pairs']
    data_target = [751590,957868,2229500]

    #count_dependent = pd.value_counts(ProcessedData.objects.filter(modules='cohesin-knockdown').values_list('experiment',flat=True))
    #label_dependent = list(count_dependent.index)
    #data_dependent = list(count_dependent.values)
    label_dependent = ["Cohesin-binding",'Cohesin-3D-genome','Cohesin-DEGs']
    data_dependent = [935,546,535]


    study_num = ProcessedData.objects.values_list("access").distinct().count()
    sample_num = ProcessedData.objects.values_list("id").distinct().count()
    cell_num = ProcessedData.objects.values_list("cell").distinct().count()

    update_news = UpdateNew.objects.all()
    return render(request,'demoSite/homepage/index.html',{'section':'home',
                                                        'label_all':label_all,'data_all':data_all,
                                                        'label_target':label_target,'data_target':data_target,
                                                        'label_dependent':label_dependent,'data_dependent':data_dependent,
                                                        'update_news':update_news,
                                                        'study_num':study_num,
                                                        'sample_num':sample_num,
                                                        'cell_num':cell_num,})

def datapage(request,module=None,experiment=None):
    # sidebar
    modules = pd.value_counts(list(ProcessedData.objects.values_list("modules",flat=True)))
    modules = zip(modules.index,modules.values)

    experiments = pd.value_counts(list(ProcessedData.objects.values_list("experiment",flat=True)))
    experiments = zip(experiments.index,experiments.values)

    subunits = pd.value_counts(list(ProcessedData.objects.values_list("subunit",flat=True)))
    subunits = zip(subunits.index,subunits.values)

    diseases = pd.value_counts(list(ProcessedData.objects.values_list("disease",flat=True)))
    diseases = zip(diseases.index,diseases.values)

    biosamples = pd.value_counts(list(ProcessedData.objects.values_list("biosample",flat=True)))
    biosamples = zip(biosamples.index,biosamples.values)

    tissues = pd.value_counts(list(ProcessedData.objects.values_list("tissue",flat=True)))
    tissues = zip(tissues.index,tissues.values)
    #main table
    datasets = ProcessedData.objects.all()

    initialfilter={}
    initialfilter['modules']="0"
    initialfilter['experiment']='0'
    initialfilter['subunit']='0'
    initialfilter['disease']='0'
    initialfilter['tissue']='0'
    initialfilter['biosample']='0'
    # return variable
    return render(request,'demoSite/datapage/dataall.html',{'section':'data',
                                                        'modules':modules,'experiments':experiments,
                                                        'subunits':subunits,'diseases':diseases,
                                                        'biosamples':biosamples,'tissues':tissues,
                                                        'datasets':datasets,'currentfilter':initialfilter,})
def datapagefilter(request,*args,**kwargs):
    modules = pd.value_counts(list(ProcessedData.objects.values_list("modules",flat=True)))
    modules = zip(modules.index,modules.values)

    experiments = pd.value_counts(list(ProcessedData.objects.values_list("experiment",flat=True)))
    experiments = zip(experiments.index,experiments.values)

    subunits = pd.value_counts(list(ProcessedData.objects.values_list("subunit",flat=True)))
    subunits = zip(subunits.index,subunits.values)

    diseases = pd.value_counts(list(ProcessedData.objects.values_list("disease",flat=True)))
    diseases = zip(diseases.index,diseases.values)

    biosamples = pd.value_counts(list(ProcessedData.objects.values_list("biosample",flat=True)))
    biosamples = zip(biosamples.index,biosamples.values)

    tissues = pd.value_counts(list(ProcessedData.objects.values_list("tissue",flat=True)))
    tissues = zip(tissues.index,tissues.values)

    condition={}
    for k,v in kwargs.items():
        kwargs[k]=v  #模板if判断row.id是数字，所以这里需要转换
        if v=="0": #当条件为0代表所选的是全部，那么就不必要加入到过滤条件中
            pass
        else:
            condition[k]=str(v)
    print(kwargs)

    datasets = ProcessedData.objects.filter(**condition)
    return render(request,'demoSite/datapage/dataall.html',{'section':'data',
                                                        'modules':modules,'experiments':experiments,
                                                        'subunits':subunits,'diseases':diseases,
                                                        'biosamples':biosamples,'tissues':tissues,
                                                        'datasets':datasets,'currentfilter':kwargs,})

#def download(request,dataid):
#    dataset = ProcessedData.objects.get(id=dataid)
#    file = open(str(dataset.content1),'rb')
#    response = HttpResponse(file)
#    response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
#    response['Content-Disposition'] = 'attachment;filename='+os.path.basename(str(dataset.content1))
#    return response

'''
@csrf_exempt
def analyzepage(request):
    #print(request.FILES['file4cor'])
    if (request.GET or request.FILES.get("file4analyze2",None)) and not request.GET.get('runexample'):
        if request.GET.get("geneText"):
            ####################
            #gene to peak to tfs
            geneset = request.GET["geneText"].split("\r\n")

            allgene = GeneModel.objects.filter(genesymbol__in = geneset).exclude(triplecohesin=".")
            genelist = []
            regulatorycohesinlist = []
            for onegene in allgene:
                for i in onegene.triplecohesin.split(","):
                    genelist.append(onegene.genesymbol)
                    regulatorycohesinlist.append(i)
            #gene to peak

            if len(regulatorycohesinlist) > 10:
                mergeDF = merge(regulatorycohesinlist,genelist)
                PartialShow = True
            else:
                mergeDF = pd.DataFrame()
                mergeDF["gene"]=genelist
                mergeDF["peak"]=regulatorycohesinlist
                mergeDF[0]=1
                mergeDF["rawpeak"]=regulatorycohesinlist
                PartialShow = False

            gene2peakdf = mergeDF.groupby(["gene",'peak'],as_index=False)[0].count()

            gene2peakdf[0] = gene2peakdf[0] / gene2peakdf[0].sum()
            gene2peakdf = gene2peakdf.sort_values(0,ascending=False).head(10)
            print(gene2peakdf)
            gene2peak = []
            for i in range(gene2peakdf.shape[0]):
                gene2peak.append({"from":gene2peakdf.iloc[i,0],'to':gene2peakdf.iloc[i,1],'value':gene2peakdf.iloc[i,2]})
            #peak to tfs
            rawpeakobject = PeakModel.objects.filter(slug__in=list(mergeDF["rawpeak"]))
            pos_list=[]
            tfs_list=[]
            tfseach_list=[]
            poseach_list=[]
            for onepeak in rawpeakobject:
                tfs = onepeak.cobind
                tfs_list += (tfs.split(','))
                tfseach_list.append(tfs)

                pos = onepeak.slug
                pos_list += ([pos]*len(tfs.split(',')))
                poseach_list.append(pos)

            tfclass = pd.read_csv("./demoSite/static/other/alltf.unique.csv",header=None)
            tfMergeDic = dict(zip(tfclass[0],tfclass[1]))
            tfmerge_list = pd.Series(tfs_list).map(tfMergeDic)
            peakMergeDict = dict(zip(mergeDF['rawpeak'],mergeDF['peak']))
            posmerge_list = list(pd.Series(pos_list).map(peakMergeDict))

            peak2tfDF = pd.DataFrame()
            peak2tfDF['posmerge'] = posmerge_list
            peak2tfDF['tfmerge'] = tfmerge_list
            peak2tfDF.dropna(axis=0,how='any',inplace=True)
            peak2tfDF['count'] = 1

            top15tfs = peak2tfDF.groupby(['tfmerge'],as_index=False)['count'].count().sort_values("count",ascending=False).head(10)['tfmerge']
            peak2tfCount = peak2tfDF.groupby(["posmerge",'tfmerge'],as_index=False)['count'].count()

            peak2tfCount['count'] = peak2tfCount['count']/peak2tfCount['count'].sum()
            #peak2tfCountFilter = peak2tfCount.sort_values("count",ascending=False).head(15).sample(frac=1)
            peak2tfCountFilter = peak2tfCount[peak2tfCount['tfmerge'].isin(list(top15tfs))]
            peak2tfCountFilter = peak2tfCountFilter[peak2tfCountFilter['posmerge'].isin(list(gene2peakdf["peak"]))]
            print(peak2tfCountFilter)

            for i in range(peak2tfCountFilter.shape[0]):
                gene2peak.append({"from":peak2tfCountFilter.iloc[i,0],'to':peak2tfCountFilter.iloc[i,1],'value':peak2tfCountFilter.iloc[i,2]})

            #output file
            outDF = mergeDF[['gene','rawpeak']]
            peak2TFdict = dict(zip(poseach_list,tfseach_list))
            outDF['TFs'] = outDF['rawpeak'].map(peak2TFdict)
            outDF.columns=['Gene','Regulatory-Cohesin','Cobind-TFs']
            outDF.to_csv("tmpfile/Analyze1_output.csv",index=None,)

            return render(request,'demoSite/analyzepage/analyze.html',{'section':'analyze','gene2peak':gene2peak,'PartialShow':PartialShow,
                                                                        'matchGeneNum':allgene.count(),'peak2gene':"nodata",'topPeakCorr':'nodata'})
        elif request.GET.get("peakText") or request.FILES.get("file4analyze2",None):
            if request.GET.get("peakText"):
                peakset = [i.split(",") for i in request.GET.get("peakText").split("\r\n")]
                peaksetDF = pd.DataFrame(peakset)
            elif request.FILES.get("file4analyze2",None):
                pass
            inputbed = BedTool.from_dataframe(peaksetDF)
            allbed = BedTool("../allcohesin.3col.bed")
            intersectBed = inputbed.intersect(allbed).to_dataframe()
            matchPeakNum = intersectBed.shape[0]
            peakset = []
            for i in range(intersectBed.shape[0]):
                peakname = str(intersectBed.iloc[i,0])+"-"+str(intersectBed.iloc[i,1])+"-"+str(intersectBed.iloc[i,2])
                peakset.append(peakname)

            #peak to gene
            targetPeakObjects = PeakModel.objects.filter(slug__in = peakset).exclude(targetgene=".")
            matchPeakWithGeneNum = targetPeakObjects.count()

            eachPeak = []
            eachGene = []
            for onePeakObject in targetPeakObjects:
                for i in onePeakObject.targetgene.split(','):
                    eachPeak.append(onePeakObject.slug)
                    eachGene.append(i)
            peak2geneout = pd.DataFrame({'cohesinPeak':eachPeak,'targetGene':eachGene})

            matchGeneNum = len(set(eachGene))

            mergePeakDF = merge(eachPeak,eachGene)
            peak2geneDF = mergePeakDF.groupby(["peak",'gene'],as_index=False)[0].count()
            peak2geneDF[0] = peak2geneDF[0]/peak2geneDF[0].sum()
            peak2gene = []
            for i in range(peak2geneDF.shape[0]):
                peak2gene.append({"from":peak2geneDF.iloc[i,0],'to':peak2geneDF.iloc[i,1],'value':peak2geneDF.iloc[i,2]})

            #kegg
            keggDF = gseapy.enrichr(gene_list=list(set(eachGene)), gene_sets='KEGG_2021_Human').results
            keggDFtop10 = keggDF.head(10)
            kegg_geneList = []
            kegg_pathway = []
            kegg_score = []
            kegg_pvalue = []
            for i in range(keggDFtop10.shape[0]):
                for j in keggDFtop10.iloc[i,9].split(";"):
                    kegg_geneList.append(j)
                    kegg_pathway.append(keggDFtop10.iloc[i,1])
                    kegg_score.append(keggDFtop10.iloc[i,8])
                    kegg_pvalue.append(keggDFtop10.iloc[i,3])
            kegg_score = kegg_score/ sum(kegg_score)
            for i in range(len(kegg_geneList)):
                peak2gene.append({"from":kegg_geneList[i],'to':str(kegg_pathway[i]) + " (p=" + "%1.1e"%(kegg_pvalue[i])+") ",'value':kegg_score[i]})

            gene2pathDict = {}
            keggDFsig = keggDF[keggDF['P-value']<0.05]
            for i in range(keggDFsig.shape[0]):
                for j in keggDFsig.iloc[i,9].split(";"):
                    if j in gene2pathDict:
                        gene2pathDict[j] = gene2pathDict[j] + ", " + keggDFsig.iloc[i,1]
                    else:
                        gene2pathDict[j] = keggDFsig.iloc[i,1]

            peak2geneout['Significant_enriched_pathway'] = peak2geneout['targetGene'].map(gene2pathDict).fillna(".")
            peak2geneout.to_csv("tmpfile/Analyze2_output.csv",index=None,)
            keggDF.to_csv("tmpfile/Analyze2_2_output.csv",index=None,)

            return render(request,'demoSite/analyzepage/analyze.html',{'section':'analyze','gene2peak':"nodata",'peak2gene':peak2gene,
                                                                    'matchPeakNum':matchPeakNum,'matchGeneNum':matchGeneNum,
                                                                    'matchPeakWithGeneNum':matchPeakWithGeneNum,'topPeakCorr':'nodata',})
        else:
            blanktype = list(request.GET.dict().keys())[0]
            return render(request,'demoSite/analyzepage/analyze.html',{'section':'analyze','gene2peak':"nodata",'submitblank':blanktype,
                                                                    'peak2gene':"nodata",'topPeakCorr':'nodata'})
    elif request.FILES.get("file4cor",None) or request.GET.get('runexample') == 'runexample3':
        if request.method == "POST":
            file_obj = request.FILES.get("file4cor",None)
            if not file_obj:
                return HttpResponse("no files for upload!")
            else:
                destination = open('tmpfile/file4cor.bed','wb')    # 打开特定的文件进行二进制的写操作
                for chunk in file_obj.chunks():      # 分块写入文件
                    destination.write(chunk)
                destination.close()
                uploadbed = BedTool('tmpfile/file4cor.bed')
        elif request.GET.get('runexample') == 'runexample3':
            uploadbed = BedTool('../testcorr.bed')

        uploadpeaknum = uploadbed.count()
        namelist = []
        jaccardlist = []

        s=time.time()
        #for i in os.listdir("/mnt/NAS/WangDB/allpeak3col"):
        dirname = "/home/support/wang/CohesinDB_production/allpeak3col/"
        for i in os.listdir(dirname):
            print(i)
            filename = dirname + i
            namelist.append(('-'.join(i.split("_")[1:7]).split(".")[0]))
            eachbed = BedTool(dirname+i)
            eachNum = int(subprocess.getoutput("wc -l %s" % filename).split()[0])
            interNum = uploadbed.intersect(eachbed,u=True).count()
            unionNum = eachNum + uploadpeaknum - interNum
            jaccardlist.append(interNum / unionNum)
        e = time.time()
        print(e-s)
        interAllpeak = pd.DataFrame({"dataname":namelist,'jaccard':jaccardlist})
        interAllpeak.to_csv("tmpfile/Analyze3_output.csv",index=None,)
        #interAllpeak.sort_values('jaccard',inplace=True,ascending=False)
        topCorrDF = interAllpeak.head(20)
        print(topCorrDF)
        topPeakCorr = []
        for i in range(topCorrDF.shape[0]):
            topPeakCorr.append({"network":topCorrDF.iloc[i,0],"MAU":float(topCorrDF.iloc[i,1]),})

        return render(request,'demoSite/analyzepage/analyze.html',{'section':'analyze','gene2peak':"nodata",'peak2gene':"nodata",
                                                                        'topPeakCorr':topPeakCorr})
    else:
        print("ccc")
        return render(request,'demoSite/analyzepage/analyze.html',{'section':'analyze','gene2peak':"nodata",'peak2gene':"nodata",
                                                                'topPeakCorr':'nodata'})
'''

def visualizepage(request,*args,**kwargs):
    datasets = ProcessedData.objects.exclude(experiment__in=['RNAseq','Microarray','PROseq','GROseq']).exclude(cdbid__in=['CDBD01446','CDBD01406','CDBD01407','CDBD01324','CDBD01325','CDBD01446','CDBD01447','CDBD01408','CDBD01409','CDBD01410','CDBD01324','CDBD01325']).exclude(access__in=["GSE155380",'GSE118716','ENCSR244BBG','ENCSR393LOP','ENCSR499RVD','ENCSR662QKG','ENCSR123UVP','ENCSR194SRI','ENCSR410MDC','ENCSR545YBD','ENCSR637QCS','ENCSR852KQC'])

    return render(request,'demoSite/visualizepage/visualize.html',{'section':'visualize','datasets':datasets,})

def visualizepage_select(request,dataid):
    datasets = ProcessedData.objects.exclude(experiment__in=['RNAseq','Microarray','PROseq','GROseq']).exclude(cdbid__in=['CDBD01446','CDBD01406','CDBD01407','CDBD01324','CDBD01325','CDBD01446','CDBD01447','CDBD01408','CDBD01409','CDBD01410','CDBD01324','CDBD01325']).exclude(access__in=["GSE155380",'GSE118716','ENCSR244BBG','ENCSR393LOP','ENCSR499RVD','ENCSR662QKG','ENCSR123UVP','ENCSR194SRI','ENCSR410MDC','ENCSR545YBD','ENCSR637QCS','ENCSR852KQC'])
    id_list = [str(x) for x in dataid.split("+")]
    selected_objects = ProcessedData.objects.filter(cdbid__in=id_list)

    epgg_tracks = []
    for selected_object in selected_objects:
        if selected_object.experiment == 'ChIPseq':
            type = 'bigwig'
            option = { "color": "#4169E1",'height':40 }
        elif selected_object.experiment == 'HiC':
            type = 'hic'
            option = { 'displayMode':'heatmap',"height": 100, "binSize": 100000,}
        elif selected_object.experiment == 'HiChIP':
            type = 'hic'
            option = { 'color':'black','displayMode':'arc'}
        elif selected_object.experiment == 'ChIAPET':
            type = 'longrange'
            option = { 'color':'orange','displayMode':'arc'}

        print(selected_object.content1)

        epgg_track = {
            "type": type,
            "name": str(selected_object.experiment)+"_"+str(selected_object.cell)+"_"+str(selected_object.cdbid),
            "url": str(selected_object.content1).replace("/mnt/NAS/WangDB","https://cohesindb.iqb.u-tokyo.ac.jp:55535"),
            "options": option,
            "metadata": { "Assay":  selected_object.experiment },
        }

        epgg_tracks.append(epgg_track)
    print(epgg_tracks)

    return render(request,'demoSite/visualizepage/visualize.html',{'section':'visualize','datasets':datasets,
                                                                'selected_objects':selected_objects,
                                                                'epgg_tracks':json.dumps(epgg_tracks),})

def browsepage(request):
    allcelltype = sorted(set(ProcessedData.objects.filter(experiment__in=['ChIPseq',]).values_list('cell',flat=True)))

    if request.GET and set(request.GET.dict().values()) != {''}:
        datadict = request.GET
        print(datadict)
        condition = {}
        filterconditions = "Current Filters: "
        
        if datadict['region']:
            chromosome = datadict['region'].split(":")[0]
            start = datadict['region'].split(":")[1].split("-")[0]
            end = datadict['region'].split(":")[1].split("-")[1]
            condition["chromosome"] = chromosome.strip()
            condition['start__gte'] = start.strip()
            condition['end__lte'] = end.strip()
            filterconditions += datadict['region'] + ";"
        #else:
        #    information1 = 'Display all cohesin sites without specific region will be extremely slow. Please add more filters.'
        #    information2 = 'If you really want to check all cohesin sites, please go to <a href="/download">download</a> page or <a href="/data">data</a> page'
        #    backlink = "/browse/"
        #    return render(request,'demoSite/error.html',{'section':'error','information1':information1,'information2':information2,
        #                                                'backlink':backlink})

        if datadict['gene']:
            condition['targetgene__contains'] = datadict['gene'].strip()
            filterconditions += datadict['gene'] + ";"
        if datadict['tf']:
            condition['cobind__contains'] = datadict['tf'].strip()
            filterconditions += datadict['tf'] + ";"
        if datadict['study']:
            condition['datasource__contains'] = datadict['study'].strip()
            filterconditions += datadict['study'] + ";"
        if datadict['cell']:
            condition['celltype__contains'] = datadict['cell'].strip()
            filterconditions += datadict['cell'] + ";"
        if datadict['ctcf']:
            condition['CTCFdependent'] = datadict['ctcf']
            filterconditions += datadict['ctcf'] + ";"
        if datadict['boundary']:
            condition['boundary'] = datadict['boundary']
            filterconditions += datadict['boundary'] + ";"
        if datadict['enhancer']:
            condition['enhancer'] = datadict['enhancer']
            filterconditions += datadict['enhancer'] + ";"
        if datadict['hicloop']:
            condition['hicloop'] = datadict['hicloop']
            filterconditions += datadict['hicloop'] + ";"
        if datadict['hub']:
            condition['hubs'] = datadict['hub']
            filterconditions += datadict['hub'] + ";"

        if not condition:
            return render(request,'demoSite/error.html',{'section':'error'})

        allpeak = PeakModel.objects.filter(**condition)
        if allpeak.count()>5000:
            information1 = 'Search results exceeded 5,000'
            information2 = 'Too many entities will make the page extremely slow. Alternatively, you can download all cohesin information in <a href="/download/">Download</a> page.'
            backlink = "/browse/"
            return render(request,'demoSite/error.html',{'section':'error','information1':information1,'information2':information2,
                                                        'backlink':backlink})

    else:
        allpeak = ExamplePeakModel.objects.all()
        filterconditions = "Current Filters: " + "chr21:26000000-26500000;"

    #peakcount
    peakcount = allpeak.count()
    #targetgene count
    targetgene = set(list(allpeak.values_list("targetgene",flat=True)))
    peakTargetGene = []
    for i in targetgene:
        peakTargetGene += i.split(",")

    #Location
    locationquery = allpeak.values_list('location',flat=True)
    locationquerylist = []
    for i in locationquery:
        locationquerylist += i.split(",")
    locationquerypd = pd.value_counts(locationquerylist)
    peaklocations = {"index":list(locationquerypd.index),"values":list(locationquerypd.values),}

    #submits
    subunitquery = allpeak.values_list('subunit',flat=True)
    subunitquerylist = []
    for i in subunitquery:
        subunitquerylist += i.split(",")
    subunitquerypd = pd.value_counts(subunitquerylist)
    peaksubunits = {"index":list(subunitquerypd.index),"values":list(subunitquerypd.values),}

    #Specificity
    cellquery = allpeak.values_list('cellspecificity',flat=True)
    cellquerylist = []
    for i in cellquery:
        if i<=0.8:
            cellquerylist.append("<0.1 (conserved)")
        elif i>0.8 and i<=0.9:
            cellquerylist.append("0.8~0.9")
        else:
            cellquerylist.append(">0.9 (cell-specific)")
    cellquerypd = pd.value_counts(cellquerylist)
    peakcells = {"index":list(cellquerypd.index),"values":list(cellquerypd.values),}

    #Boundary
    boundaryquery = allpeak.values_list('boundary',flat=True)
    boundaryquerypd = pd.value_counts(boundaryquery)
    peakboundaries = {"index":list(boundaryquerypd.index),"values":list(boundaryquerypd.values),}

    #loop
    ctcfquery = allpeak.values_list('CTCFdependent',flat=True)
    ctcfquerypd = pd.value_counts(ctcfquery)
    peakctcf = {"index":list(ctcfquerypd.index),"values":list(ctcfquerypd.values),}

    #Enhancer
    enhancerquery = allpeak.values_list('enhancer',flat=True)
    enhancerquerypd = pd.value_counts(enhancerquery)
    peakenhancers = {"index":list(enhancerquerypd.index),"values":list(enhancerquerypd.values),}

    return render(request,'demoSite/browsepage/browse.html',{'section':'browse','filterconditions':filterconditions,
                                                            'allpeak':allpeak,'peakcount':peakcount,
                                                            'peakTargetGeneCount':len(peakTargetGene),
                                                            'peaklocations':peaklocations,'peaksubunits':peaksubunits,
                                                            'peakcells':peakcells,"peakboundaries":peakboundaries,
                                                            'peakctcf':peakctcf,'peakenhancers':peakenhancers,
                                                            'allcelltype':allcelltype,})

def browsegenepage(request):
    if request.GET and set(request.GET.dict().values()) != {''}:
        datadict = request.GET
        print(set(datadict.dict().values()))

        condition = {}
        filterconditions = "Current Filters: "

        if datadict['region']:
            chromosome = datadict['region'].split(":")[0]
            start = datadict['region'].split(":")[1].split("-")[0]
            end = datadict['region'].split(":")[1].split("-")[1]
            condition["chromosome"] = chromosome.strip()
            condition['start__gte'] = start.strip()
            condition['end__lte'] = end.strip()
            filterconditions += datadict['region'] + ";"
        if datadict['genename']:
            condition['genesymbol'] = datadict['genename']
            filterconditions += datadict['genename'] + ";"
        if datadict['geneid']:
            condition['geneID'] = datadict['geneid']
            filterconditions += datadict['geneid'] + ";"
        if datadict['dependent']:
            if datadict['dependent'] == 'Triple-evidenced':
                condition['triplewheter'] = True
            elif datadict['dependent'] == 'Loop-evidenced':
                condition['loopwhether'] = True
            elif datadict['dependent'] == 'Deg-evidenced':
                condition['degwhether'] = True
            elif datadict['dependent'] == 'Coexpression-evidenced':
                condition['correlationwhether'] = True
            filterconditions += datadict['dependent'] + ";"

        allgene = GeneModel.objects.filter(**condition)
    else:
        allgene = ExampleGeneModel.objects.all()
        filterconditions = "Default Filters: " + "chr21:16000000-18000000;"

    #genecount
    genecount = allgene.count()
    #peakcount
    regulatePeak = set(list(allgene.values_list("triplecohesin",flat=True)))
    regulatePeakList = []
    for i in regulatePeak:
        regulatePeakList += i.split(",")
    peakcount=len(regulatePeakList)

    #triple evidence
    triplequery = allgene.values_list('triplewheter',flat=True)
    triplequerypd = pd.value_counts(triplequery)
    modifiedindex = ["Non-triple" if i==False else "Cohesin-regulated" for i in triplequerypd.index]
    genetypes = {"index":list(modifiedindex),"values":list(triplequerypd.values),}

    #related type
    subunitquery = allgene.values_list('relatedtype',flat=True)
    subunitquerypd = pd.value_counts(subunitquery)
    genesubunits = {"index":list(subunitquerypd.index),"values":list(subunitquerypd.values),}
    print(genesubunits)

    #Protein coding
    studyquery = allgene.values_list('proteincoding',flat=True)
    studyquerypd = pd.value_counts(studyquery)
    genestudies = {"index":list(studyquerypd.index),"values":list(studyquerypd.values),}


    return render(request,'demoSite/browsepage/browsegene.html',{'section':'browse','allgene':allgene,
                                                                'filterconditions':filterconditions,
                                                                'genecount':genecount,'peakcount':peakcount,
                                                                'genetypes':genetypes,'genestudies':genestudies,
                                                                'genesubunits':genesubunits,})

def searchpage(request):
    return render(request,'demoSite/searchpage/search.html',{'section':'search'})

REMOTE_HOST = "https://pyecharts.github.io/assets/js"

def helppage(request):
    return render(request,'demoSite/helppage/help.html',{'section':'help'})

def downloadpage(request):
    return render(request,'demoSite/downloadpage/download.html',{'section':'download'})


#from django.http import JsonResponse
#import json
