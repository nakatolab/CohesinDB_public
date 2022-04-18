from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from demoSite.models import LoopModel, GeneModel, PeakModel, GTExData, ProcessedData, CellType
import pandas as pd
import numpy as np
import os
from django.db.models import Q

def browse_eachdata(request,cdbid):
    seleteddata = ProcessedData.objects.filter(cdbid=cdbid)[0]

    name1 = os.path.basename(str(seleteddata.content1))
    link1 = str(seleteddata.content1).replace("/mnt/NAS/WangDB","https://cohesindb.iqb.u-tokyo.ac.jp:55535")
    name2 = os.path.basename(str(seleteddata.content2))
    link2 = str(seleteddata.content2).replace("/mnt/NAS/WangDB","https://cohesindb.iqb.u-tokyo.ac.jp:55535")
    name3 = os.path.basename(str(seleteddata.content3))
    link3 = str(seleteddata.content3).replace("/mnt/NAS/WangDB","https://cohesindb.iqb.u-tokyo.ac.jp:55535")


    return render(request,'demoSite/browse_each/browse_eachdata.html',{'section':'data',
                                                            'onedata':seleteddata,'name1':name1,'link1':link1,
                                                            'name2':name2,'link2':link2,'name3':name3,'link3':link3})

def browse_eachcell(request,cellname):
    seleteddata = CellType.objects.filter(cellname=cellname)[0]
    return render(request,'demoSite/browse_each/browse_eachcell.html',{'section':'data','onecell':seleteddata,})



def browse_eachloop(request,cdbid):
    selectedloop = LoopModel.objects.filter(cdbid=cdbid)
    print(selectedloop)
    chr1 = selectedloop[0].chrom1
    start1 = selectedloop[0].start1
    end1 = selectedloop[0].end1
    chr2 = selectedloop[0].chrom2
    start2 = selectedloop[0].start2
    end2 = selectedloop[0].end2
    visualizeRegion = chr1 + ":" + str(start1 - 100000) + "-" + str(end2 + 100000)
    epgg_tracks = []

    #loop
    if not os.path.isfile("/mnt/NAS/WangDB/tmpfile/"+cdbid+".longrange.gz"):
        with open('/mnt/NAS/WangDB/tmpfile/'+cdbid+'.longrange','w') as f:
            f.write(chr1 + "\t" + str(start1) + "\t" + str(end1) + "\t" + chr2 + ":" + str(start2) + "-" + str(end2) + ","+ str(1) + "\n")
            f.write(chr2 + "\t" + str(start2) + "\t" + str(end2) + "\t" + chr1 + ":" + str(start1) + "-" + str(end1) + ","+ str(1) + "\n")
        os.system("bgzip -f /mnt/NAS/WangDB/tmpfile/"+cdbid+".longrange")
        os.system("tabix -p bed /mnt/NAS/WangDB/tmpfile/"+cdbid+".longrange.gz")
        os.system("rm /mnt/NAS/WangDB/tmpfile/"+cdbid+".longrange")
    else:
        pass

    epgg_track1 = {
        "type": 'longrange',
        "name": "Cohesin-interaction " + selectedloop[0].cdbid ,
        "url": "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/" + cdbid + ".longrange.gz",
        "options": { 'color':'#B8008A','displayMode':'arc'},
        "metadata": { "Assay":  "Loop" },
    }
    epgg_tracks.append(epgg_track1)

    #related peak
    relatedpeak = PeakModel.objects.filter(Q(chromosome=chr1,start__lte=end1+5000,end__gte=start1-5000) | Q(chromosome=chr2,start__lte=end2+5000,end__gte=start2-5000))

    if not os.path.isfile("/mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedpeak.sorted.bed.gz"):
        peakDF = pd.DataFrame()
        if relatedpeak:
            peakDF['chr'] = relatedpeak.values_list('chromosome',flat=True)
            peakDF['start'] = relatedpeak.values_list('start',flat=True)
            peakDF['end'] = relatedpeak.values_list('end',flat=True)
        peakDF.to_csv('/mnt/NAS/WangDB/tmpfile/'+cdbid+'_relatedpeak.bed',header=None,index=None,sep="\t")
        os.system("sortBed -i /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedpeak.bed > /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedpeak.sorted.bed")
        os.system("bgzip -f /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedpeak.sorted.bed")
        os.system("tabix -p bed /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedpeak.sorted.bed.gz")
        os.system('rm /mnt/NAS/WangDB/tmpfile/'+cdbid+'_relatedpeak.bed')
        os.system('rm /mnt/NAS/WangDB/tmpfile/'+cdbid+'_relatedpeak.sorted.bed')
    else:
        pass

    epgg_track2 = {
        "type": 'bed',
        "name": "Related cohesin sites",
        "url": "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/"+cdbid+"_relatedpeak.sorted.bed.gz",
        "options": { 'color':'grey',},
        "metadata": { "Assay":  "Peak" },
    }
    epgg_tracks.append(epgg_track2)

    #gene
    relatedgene = GeneModel.objects.filter(Q(chromosome=chr1,start__lte=end1+5000,end__gte=start1-5000) | Q(chromosome=chr2,start__lte=end2+5000,end__gte=start2-5000))

    if not os.path.isfile("/mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.sorted.bed.gz"):
        geneDF = pd.DataFrame()
        if relatedgene:
            geneDF['chr'] = relatedgene.values_list('chromosome',flat=True)
            geneDF['start'] = relatedgene.values_list('start',flat=True)
            geneDF['end'] = relatedgene.values_list('end',flat=True)
            geneDF['name'] = relatedgene.values_list('geneID',flat=True)
            geneDF['other'] = '.'
            geneDF['strand'] = relatedgene.values_list('strand',flat=True)

        geneDF.to_csv('/mnt/NAS/WangDB/tmpfile/'+cdbid+'_relatedgene.bed',header=None,index=None,sep="\t")
        os.system("sortBed -i /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.bed > /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.sorted.bed")
        os.system("bgzip -f /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.sorted.bed")
        os.system("tabix -p bed /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.sorted.bed.gz")
        os.system("rm /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.sorted.bed")
        os.system("rm /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.bed")
    else:
        pass

    epgg_track3 = {
        "type": 'bed',
        "name": "Regulated genes",
        "url": "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/"+cdbid+"_relatedgene.sorted.bed.gz",
        "options": { 'color':'grey',},
        "metadata": { "Assay":  "Gene" },
    }
    epgg_tracks.append(epgg_track3)

    return render(request,'demoSite/browse_each/browse_eachloop.html',{'section':'browse','selectedloop':selectedloop,
                                                "visualizeRegion":visualizeRegion,"epgg_tracks":epgg_tracks,
                                                'relatedgene':relatedgene,'relatedpeak':relatedpeak,})

def browse_eachpeak(request,cdbid):
    selectedpeak = PeakModel.objects.filter(cdbid=cdbid)
    chr = selectedpeak[0].chromosome
    start = selectedpeak[0].start
    end = selectedpeak[0].end
    visualizeRegion = chr + ":" + str(start - 500000) + "-" + str(end + 500000)
    epgg_tracks = []

    # peak
    if not os.path.isfile("/mnt/NAS/WangDB/tmpfile/"+cdbid+".bed.gz"):
        with open('/mnt/NAS/WangDB/tmpfile/'+cdbid+'.bed','w') as f:
            f.write(chr + "\t" + str(start) + "\t" + str(end) + "\n")
        os.system("bgzip -f /mnt/NAS/WangDB/tmpfile/"+cdbid+".bed")
        os.system("tabix -p bed /mnt/NAS/WangDB/tmpfile/"+cdbid+".bed.gz")
        os.system("rm /mnt/NAS/WangDB/tmpfile/"+cdbid+".bed")

    epgg_track1 = {
        "type": 'bed',
        "name": "Cohesin site "+selectedpeak[0].cdbid,
        "url": "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/"+cdbid+".bed.gz",
        "options": { 'color':'black',},
        "metadata": { "Assay":  "Peak" },
    }
    epgg_tracks.append(epgg_track1)

    # genes
    targetgene  = selectedpeak[0].targetgeneID

    if targetgene == ".":
        targetgeneobjects = None
    else:
        targetgenelist = targetgene.split(",")
        targetgeneobjects = GeneModel.objects.filter(geneID__in = targetgenelist)

    if not os.path.isfile("/mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.sorted.bed.gz"):
        geneDF = pd.DataFrame()
        if targetgeneobjects:
            geneDF['chr'] = targetgeneobjects.values_list('chromosome',flat=True)
            geneDF['start'] = targetgeneobjects.values_list('start',flat=True)
            geneDF['end'] = targetgeneobjects.values_list('end',flat=True)
            geneDF['name'] = targetgeneobjects.values_list('geneID',flat=True)
            geneDF['other'] = '.'
            geneDF['strand'] = targetgeneobjects.values_list('strand',flat=True)

        geneDF.to_csv('/mnt/NAS/WangDB/tmpfile/'+cdbid+'_relatedgene.bed',header=None,index=None,sep="\t")
        os.system("sortBed -i /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.bed > /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.sorted.bed")
        os.system("bgzip -f /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.sorted.bed")
        os.system("tabix -p bed /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.sorted.bed.gz")
        os.system("rm /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.sorted.bed")
        os.system("rm /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedgene.bed")
    else:
        pass

    epgg_track2 = {
        "type": 'bed',
        "name": selectedpeak[0].cdbid + " regulated genes",
        "url": "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/"+cdbid+"_relatedgene.sorted.bed.gz",
        "options": { 'color':'grey',},
        "metadata": { "Assay":  "Gene" },
    }
    epgg_tracks.append(epgg_track2)

    # related loop
    selectedloop = LoopModel.objects.filter(Q(chrom1=chr,start1__lte=end+5000,end1__gte=start-5000) | Q(chrom2=chr,start2__lte=end+5000,end2__gte=start-5000))
    if not os.path.isfile("/mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedloop.sorted.longrange.gz"):
        loopDF = pd.DataFrame()
        loopDF['chr1'] = selectedloop.values_list("chrom1",flat=True)
        loopDF['start1'] = selectedloop.values_list("start1",flat=True)
        loopDF['end1'] = selectedloop.values_list("end1",flat=True)
        loopDF['chr2'] = selectedloop.values_list("chrom2",flat=True)
        loopDF['start2'] = selectedloop.values_list("start2",flat=True)
        loopDF['end2'] = selectedloop.values_list("end2",flat=True)
        loopDF.to_csv('/mnt/NAS/WangDB/tmpfile/'+cdbid+'_relatedloop.bedpe',header=None,index=None,sep="\t")
        os.system('''awk '{print $1"\t"$2"\t"$3"\t"$4":"$5"-"$6","1}' /mnt/NAS/WangDB/tmpfile/'''+cdbid+'''_relatedloop.bedpe > /mnt/NAS/WangDB/tmpfile/'''+cdbid+'''_relatedloop.longrange''')
        os.system('''awk '{print $4"\t"$5"\t"$6"\t"$1":"$2"-"$3","1}' /mnt/NAS/WangDB/tmpfile/'''+cdbid+'''_relatedloop.bedpe >> /mnt/NAS/WangDB/tmpfile/'''+cdbid+'''_relatedloop.longrange''')
        os.system("sortBed -i /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedloop.longrange > /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedloop.sorted.longrange")
        os.system("bgzip -f /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedloop.sorted.longrange")
        os.system("tabix -p bed /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedloop.sorted.longrange.gz")
    else:
        pass

    epgg_track3 = {
        "type": 'longrange',
        "name": "Related cohesin loop",
        "url": "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/"+cdbid+"_relatedloop.sorted.longrange.gz",
        "options": { 'color':'#B8008A','displayMode':'arc'},
        "metadata": { "Assay":  "Loop" },
    }
    epgg_tracks.append(epgg_track3)

    print(targetgeneobjects)


    return render(request,'demoSite/browse_each/browse_eachpeak.html',{'section':'browse','selectedpeak':selectedpeak,
                                                "visualizeRegion":visualizeRegion,"epgg_tracks":epgg_tracks,
                                                'relatedgene':targetgeneobjects,'relatedloop':selectedloop})


def browse_eachgene(request,cdbid):
    selectedgene = GeneModel.objects.filter(cdbid=cdbid)
    chr = selectedgene[0].chromosome
    start = selectedgene[0].start
    end = selectedgene[0].end
    visualizeRegion = chr + ":" + str(start - 500000) + "-" + str(end + 500000)

    # gene
    if not os.path.isfile("/mnt/NAS/WangDB/tmpfile/"+cdbid+".bed.gz"):
        print("first time")
        with open('/mnt/NAS/WangDB/tmpfile/'+cdbid+'.bed','w') as f:
            f.write(selectedgene[0].chromosome + "\t" + str(selectedgene[0].start) + "\t" + str(selectedgene[0].end) + "\t" + selectedgene[0].geneID + "\t.\t"+ selectedgene[0].strand+"\n")
        os.system("bgzip -f /mnt/NAS/WangDB/tmpfile/"+cdbid+".bed")
        os.system("tabix -p bed /mnt/NAS/WangDB/tmpfile/"+cdbid+".bed.gz")
    else:
        pass

    # related cohesin
    relatedpeaklist = selectedgene[0].triplecohesin.split(",")
    relatedpeak = PeakModel.objects.filter(slug__in = relatedpeaklist)

    if not os.path.isfile("/mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedpeak.sorted.bed.gz"):
        peakDF = pd.DataFrame()
        if selectedgene[0].triplewheter:
            peakDF['chr'] = [i.split("-")[0] for i in selectedgene[0].triplecohesin.split(",")]
            peakDF['start'] = [i.split("-")[1] for i in selectedgene[0].triplecohesin.split(",")]
            peakDF['end'] = [i.split("-")[2] for i in selectedgene[0].triplecohesin.split(",")]
        peakDF.to_csv('/mnt/NAS/WangDB/tmpfile/'+cdbid+'_relatedpeak.bed',header=None,index=None,sep="\t")
        os.system("sortBed -i /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedpeak.bed > /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedpeak.sorted.bed")
        os.system("bgzip -f /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedpeak.sorted.bed")
        os.system("tabix -p bed /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedpeak.sorted.bed.gz")
        os.system("rm /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedpeak.bed")
    else:
        pass

    # related loop
    selectedloop = LoopModel.objects.filter(Q(chrom1=chr,start1__lte=end+5000,end1__gte=start-5000) | Q(chrom2=chr,start2__lte=end+5000,end2__gte=start-5000))
    if not os.path.isfile("/mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedloop.sorted.longrange.gz"):
        loopDF = pd.DataFrame()
        loopDF['chr1'] = selectedloop.values_list("chrom1",flat=True)
        loopDF['start1'] = selectedloop.values_list("start1",flat=True)
        loopDF['end1'] = selectedloop.values_list("end1",flat=True)
        loopDF['chr2'] = selectedloop.values_list("chrom2",flat=True)
        loopDF['start2'] = selectedloop.values_list("start2",flat=True)
        loopDF['end2'] = selectedloop.values_list("end2",flat=True)
        loopDF['width'] = selectedloop.values_list("loopwidth",flat=True)
        loopDF.to_csv('/mnt/NAS/WangDB/tmpfile/'+cdbid+'_relatedloop.bedpe',header=None,index=None,sep="\t")
        os.system('''awk '{print $1"\t"$2"\t"$3"\t"$4":"$5"-"$6","1}' /mnt/NAS/WangDB/tmpfile/'''+cdbid+'''_relatedloop.bedpe > /mnt/NAS/WangDB/tmpfile/'''+cdbid+'''_relatedloop.longrange''')
        os.system('''awk '{print $4"\t"$5"\t"$6"\t"$1":"$2"-"$3","1}' /mnt/NAS/WangDB/tmpfile/'''+cdbid+'''_relatedloop.bedpe >> /mnt/NAS/WangDB/tmpfile/'''+cdbid+'''_relatedloop.longrange''')
        os.system("sortBed -i /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedloop.longrange > /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedloop.sorted.longrange")
        os.system("bgzip -f /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedloop.sorted.longrange")
        os.system("tabix -p bed /mnt/NAS/WangDB/tmpfile/"+cdbid+"_relatedloop.sorted.longrange.gz")
        os.system("rm /mnt/NAS/WangDB/tmpfile/"+cdbid+"*bedpe")
        os.system("rm /mnt/NAS/WangDB/tmpfile/"+cdbid+"*longrange")
    else:
        pass

    epgg_tracks = []
    epgg_track1 = {
        "type": 'bed',
        "name": selectedgene[0].genesymbol + " gene locus",
        "url": "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/"+cdbid+".bed.gz",
        "options": { 'color':'red',},
        "metadata": { "Assay":  "Gene" },
    }
    epgg_tracks.append(epgg_track1)

    epgg_track3 = {
        "type": 'bed',
        "name": selectedgene[0].genesymbol + " related cohesin sites",
        "url": "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/"+cdbid+"_relatedpeak.sorted.bed.gz",
        "options": { 'color':'black',},
        "metadata": { "Assay":  "Gene" },
    }
    epgg_tracks.append(epgg_track3)

    epgg_track2 = {
        "type": 'longrange',
        "name": selectedgene[0].genesymbol + " related cohesin loop",
        "url": "https://cohesindb.iqb.u-tokyo.ac.jp:55535/tmpfile/"+cdbid+"_relatedloop.sorted.longrange.gz",
        "options": { 'color':'#B8008A','displayMode':'arc'},
        "metadata": { "Assay":  "Loop" },
    }
    epgg_tracks.append(epgg_track2)

    gtex_objects = GTExData.objects.filter(geneID = selectedgene[0].geneID)[0]
    tissue_name = gtex_objects.tissuename
    tissue_median = gtex_objects.tissuemedian

    # relatedpeakspecific = pd.Series(relatedpeak.values_list("cellspecificity",flat=True)).describe()
    #relatedpeakspecific_dict = {'Median':round(relatedpeakspecific[5],3),'quantile-25%':round(relatedpeakspecific[4],3),'quantile-75%':round(relatedpeakspecific[6],3)}
    relatedpeakspecific_dict = pd.Series(relatedpeak.values_list("cellspecificity",flat=True)).mean()

    return render(request,'demoSite/browse_each/browse_eachgene.html',{'section':'browse','selectedgene':selectedgene,
                                                "visualizeRegion":visualizeRegion,"epgg_tracks":epgg_tracks,
                                                'relatedpeak':relatedpeak,'relatedloop':selectedloop,
                                                'tissue_name':tissue_name,'tissue_median':tissue_median,
                                                'gtex_objects':gtex_objects,'relatedpeakspecific_dict':relatedpeakspecific_dict,})
