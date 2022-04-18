from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from demoSite.models import ProcessedData, UpdateNew, GeneModel, PeakModel, LoopModel
import os, subprocess, time, random, string
import json
import pandas as pd
import numpy as np
from pybedtools import BedTool
from .custom import merge
import gseapy
from django.views.decorators.csrf import csrf_exempt
import time

@csrf_exempt
def analyzepage(request):
    userid=''.join(random.sample(string.ascii_letters + string.digits, 8))
    boolanalyze1 = request.POST.get("geneText")
    boolanalyze2 = request.POST.get("peakText")
    boolanalyze3 = request.FILES.get("file4analyze3",None)
    #print(request.FILES['file4cor'])
    if (request.POST.get("geneText") or request.GET.get("geneText")) and not boolanalyze2 and not boolanalyze3:
        if request.POST.get("geneText"):
            geneset = request.POST["geneText"].split("\r\n")
        elif request.GET.get("geneText"):
            geneset = request.GET["geneText"].split("\r\n")
            ####################
            #gene to peak to tfs
        print(len(geneset))
        if len(geneset) > 1000:
            information1 = 'Too many genes, maximum number of genes: 1000'
            information2 = 'Too many genes, maximum number of genes: 1000'
            backlink = "/analyze/"
            return render(request,'demoSite/error.html',{'section':'error','information1':information1,'information2':information2,
                                                        'backlink':backlink})

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

        for i in range(peak2tfCountFilter.shape[0]):
            gene2peak.append({"from":peak2tfCountFilter.iloc[i,0],'to':peak2tfCountFilter.iloc[i,1],'value':peak2tfCountFilter.iloc[i,2]})

        #output file
        outDF = mergeDF[['gene','rawpeak']]
        peak2TFdict = dict(zip(poseach_list,tfseach_list))
        outDF['TFs'] = outDF['rawpeak'].map(peak2TFdict)
        outDF.columns=['Gene','Regulatory-Cohesin','Cobind-TFs']
        outDF.to_csv("/mnt/NAS/WangDB/tmpfile/"+"Analyze1_output_"+userid+".tsv",index=None,)
        linkanalyze1 = "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/Analyze1_output_"+userid+".tsv"

        return render(request,'demoSite/analyzepage/analyze.html',{'section':'analyze','gene2peak':gene2peak,'PartialShow':PartialShow,
                                                                    'matchGeneNum':allgene.count(),'peak2gene':"nodata",
                                                                    'topPeakCorr':'nodata','linkanalyze1':linkanalyze1})

    #elif request.POST.get("peakText") or request.FILES.get("file4analyze2",None):
    elif (request.POST.get("peakText") or request.GET.get("peakText")) and not boolanalyze1 and not boolanalyze3:
        if request.POST.get("peakText"):
            peakset = [i.split(",") for i in request.POST.get("peakText").split("\r\n")]
        elif request.GET.get("peakText"):
            peakset = [i.split(",") for i in request.GET.get("peakText").split("\r\n")]

        if len(peakset) > 1000:
            information1 = 'Too many input regions, maximum number of regions: 1000'
            information2 = 'Too many input regions, maximum number of regions: 1000'
            backlink = "/analyze/"
            return render(request,'demoSite/error.html',{'section':'error','information1':information1,'information2':information2,
                                                        'backlink':backlink})
        peaksetDF = pd.DataFrame(peakset)

        inputbed = BedTool.from_dataframe(peaksetDF)
        allbed = BedTool("../allcohesin.3col.bed")

        intersectBed = inputbed.intersect(allbed).to_dataframe()

        matchPeakNum = intersectBed.shape[0]


        peaksetslug = []
        for i in range(intersectBed.shape[0]):
            peakname = str(intersectBed.iloc[i,0])+"-"+str(intersectBed.iloc[i,1])+"-"+str(intersectBed.iloc[i,2])
            peaksetslug.append(peakname)

        #peak to gene

        targetPeakObjects = PeakModel.objects.filter(slug__in = peaksetslug).exclude(targetgene=".")

        matchPeakWithGeneNum = targetPeakObjects.count()
        if matchPeakWithGeneNum == 0:
            return render(request,'demoSite/error.html',{'section':'error','information1':'No matched object.','information2':'The input sites do not co-localize with cohesin.',
                                                            'backlink':"/analyze/"})

        eachPeak = []
        eachGene = []
        for onePeakObject in targetPeakObjects:
            for i in onePeakObject.targetgene.split(','):
                eachPeak.append(onePeakObject.slug)
                eachGene.append(i)
        peak2geneout = pd.DataFrame({'cohesinPeak':eachPeak,'targetGene':eachGene})


        matchGeneNum = len(set(eachGene))

        print(eachPeak)
        print(eachGene)

        start=time.time()
        mergePeakDF = merge(eachPeak,eachGene)
        print(mergePeakDF)
        end=time.time()
        print(end-start)
        peak2geneDF = mergePeakDF.groupby(["peak",'gene'],as_index=False)[0].count()
        peak2geneDF[0] = peak2geneDF[0]/peak2geneDF[0].sum()


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

        if peak2geneDF.shape[0] <= 15:
            selected_peak2geneDF = peak2geneDF
        else:
            selected_peak2geneDF = peak2geneDF[peak2geneDF['gene'].isin(kegg_geneList)]

        peak2gene = []
        for i in range(selected_peak2geneDF.shape[0]):
            peak2gene.append({"from":selected_peak2geneDF.iloc[i,0],'to':selected_peak2geneDF.iloc[i,1],'value':selected_peak2geneDF.iloc[i,2]})

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
        peak2geneout.to_csv("/mnt/NAS/WangDB/tmpfile/"+"Analyze2_output1_"+userid+".tsv",index=None,)
        keggDF.to_csv("/mnt/NAS/WangDB/tmpfile/"+"Analyze2_output2_"+userid+".tsv",index=None,)
        linkanalyze2_1 = "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/Analyze2_output1_"+userid+".tsv"
        linkanalyze2_2 = "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/Analyze2_output2_"+userid+".tsv"


        return render(request,'demoSite/analyzepage/analyze.html',{'section':'analyze','gene2peak':"nodata",'peak2gene':peak2gene,
                                                                    'matchPeakNum':matchPeakNum,'matchGeneNum':matchGeneNum,
                                                                    'matchPeakWithGeneNum':matchPeakWithGeneNum,'topPeakCorr':'nodata',
                                                                    'linkanalyze2_1':linkanalyze2_1,"linkanalyze2_2":linkanalyze2_2,})
    #else:
    #    blanktype = list(request.GET.dict().keys())[0]
    #    return render(request,'demoSite/analyzepage/analyze.html',{'section':'analyze','gene2peak':"nodata",'submitblank':blanktype,
    #                                                                'peak2gene':"nodata",'topPeakCorr':'nodata'})

    elif (request.FILES.get("file4analyze3",None) or request.GET.get('runexample') == 'runexample3') and not boolanalyze1 and not boolanalyze2:
        def wc_count(file_name):
            import subprocess
            out = subprocess.getoutput("wc -l %s" % file_name)
            return int(out.split()[0])

        userid=''.join(random.sample(string.ascii_letters + string.digits, 8))
        analyze3input = "Analyze3_input_"+userid+".tsv"
        analyze3out1 = "Analyze3_output1_"+userid+".tsv"
        analyze3out2 = "Analyze3_output2_"+userid+".tsv"
        analyze3plot = "Analyze3_plot_"+userid+".tsv"
        if request.method == "POST":
            file_obj = request.FILES.get("file4analyze3",None)
            if not file_obj:
                return HttpResponse("no files for upload!")
            else:
                destination = open('/mnt/NAS/WangDB/tmpfile/'+analyze3input,'wb')    # 打开特定的文件进行二进制的写操作
                for chunk in file_obj.chunks():      # 分块写入文件
                    destination.write(chunk)
                destination.close()
                uploadbed = '/mnt/NAS/WangDB/tmpfile/'+analyze3input
        elif request.GET.get('runexample') == 'runexample3':
            uploadbed =  '../DiscoverLoop.test'

        inputnum = wc_count(uploadbed)
        if inputnum > 5000:
            information1 = 'Too many genomic regions, maximum number of regions: 5000'
            information2 = 'If you want to check more loops, please go to <a href="/download">download</a> page and download "All cohesin-mediated chromatin interactions" to analyze related loops'
            backlink = "/analyze/"
            return render(request,'demoSite/error.html',{'section':'error','information1':information1,'information2':information2,
                                                        'backlink':backlink})

        print("step1 pairToBed")
        os.system("pairToBed -b "+uploadbed+" -a /home/support/wang/Production_data/allloop.minimal.tsv |  sed '1iloop-chr1\tloop-start1\tloop-end1\tloop-chr2\tloop-start2\tloop-end2\tstudies\tInputRegion-chr\tInputRegion-start\tInputRegion-end' > /mnt/NAS/WangDB/tmpfile/"+analyze3out1)

        loopnum = wc_count("/mnt/NAS/WangDB/tmpfile/"+analyze3out1)

        print("step2 sort Study")
        os.system("sed '1d' /mnt/NAS/WangDB/tmpfile/"+analyze3out1+" | cut -f 7 | tr ',' '\n' > /mnt/NAS/WangDB/tmpfile/"+analyze3plot)

        print("step3 other side")
        os.system("sh demoSite/otherAnchor.sh /mnt/NAS/WangDB/tmpfile/"+analyze3out1+" /mnt/NAS/WangDB/tmpfile/"+analyze3out2)

        allStudyDF = pd.read_csv("/mnt/NAS/WangDB/tmpfile/"+analyze3plot,sep="\t",header=None)[0].value_counts()

        topStudyDF = allStudyDF.head(10)
        topStudy = []
        for i in range(topStudyDF.shape[0]):
            topStudy.append({"network":topStudyDF.index[i],"MAU":topStudyDF.values[i],})

        linkanalyze3_1 = "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/"+analyze3out1
        linkanalyze3_2 = "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/"+analyze3out2

        return render(request,'demoSite/analyzepage/analyze.html',{'section':'analyze','gene2peak':"nodata",'peak2gene':"nodata",
                                                                        'topPeakCorr':topStudy,'linkanalyze3_2':linkanalyze3_2,
                                                                        'linkanalyze3_1':linkanalyze3_1, 'studynum':allStudyDF.shape[0],
                                                                        'inputnum':inputnum,'loopnum':loopnum})
    else:
        return render(request,'demoSite/analyzepage/analyze.html',{'section':'analyze','gene2peak':"nodata",'peak2gene':"nodata",
                                                                'topPeakCorr':'nodata'})
