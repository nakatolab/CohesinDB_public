from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from demoSite.models import ProcessedData, UpdateNew, GeneModel, PeakModel
import pandas as pd
import numpy as np

def statisticpage(request):
    # Data1 Plot1
    def make_string(label, number, assay):
        datastring = ""
        for i in range(len(label)):
            datastring = datastring + "{x: '" + str(label[i]) + "',y: '" + str(assay) + "',r: " + str(round(np.log2(number[i]+1),2)) + "},"
        return datastring

    def make_string_each(assay,outname):
        if assay == 'HiC':
            hicnum = ProcessedData.objects.filter(experiment=assay).count()
            data_out = "{x: 'Other',y: 'Hi-C',r: "+ str(round(np.log2(hicnum+1),2)) +"},"
        else:
            data_object = ProcessedData.objects.filter(experiment=assay).values_list('subunit',flat=True)
            data_df = pd.value_counts(data_object)
            data_subunit = data_df.index
            data_num = data_df.values

            data_modify = {}
            data_modify['Other'] = 0
            for i in range(len(data_df)):
                if data_subunit[i] in ['Rad21','CTCF','NIPBL','Input','SA1','SA2','SMC1','SMC3']:
                    data_modify[data_subunit[i]] = data_num[i]
                else:
                    data_modify['Other'] = data_modify['Other'] + data_num[i]

            data_out = make_string(list(data_modify.keys()),list(data_modify.values()),outname)
        return data_out

    data1_chipseq = make_string_each("ChIPseq","ChIP-seq")
    data1_chia = make_string_each("ChIAPET","ChIA-PET")
    data1_hichip = make_string_each("HiChIP","Hi-ChIP")
    data1_hic = make_string_each("HiC","Hi-C")
    data1_rnaseq = make_string_each("RNAseq","RNA-seq")
    data1_microarray = make_string_each("Microarray","Microarray")
    data1_proseq= make_string_each("PROseq","PRO-seq")
    data1_groseq= make_string_each("GROseq","GRO-seq")

    chart1data = '''[
                        {
                            label: 'ChIP-seq',
                            data: [
                                ''' + data1_chipseq + '''
                            ],
                            backgroundColor: 'rgb(255, 99, 132)'
                        },
                        {
                            label: 'ChIA-PET',
                            data: [
                                ''' + data1_chia + '''
                            ],
                            backgroundColor: '#712F79'
                        },
                        {
                            label: 'Hi-ChIP',
                            data: [
                                ''' + data1_hichip + '''
                            ],
                            backgroundColor: '#F7996E'
                        },
                        {
                            label: 'Hi-C',
                            data: [
                                ''' + data1_hic + '''
                            ],
                            backgroundColor: '#976391',
                        },
                        {
                            label: 'RNA-seq',
                            data: [
                                ''' + data1_rnaseq + '''
                            ],
                            backgroundColor: 'green'
                        },
                        {
                            label: 'Microarray',
                            data: [
                                ''' + data1_microarray + '''
                            ],
                            backgroundColor: '#4C4C9D'
                        },
                        {
                            label: 'PRO-seq',
                            data: [
                                ''' + data1_proseq + '''
                            ],
                            backgroundColor: '#48639C'
                        },
                        {
                            label: 'GRO-seq',
                            data: [
                                ''' + data1_groseq + '''
                            ],
                            backgroundColor: '#orange',
                        },
                ]'''



    allcell = pd.value_counts(ProcessedData.objects.values_list('cell',flat=True))
    topcount = 0
    data2_label = []
    data2_chip = []
    data2_chia = []
    data2_hichip = []
    data2_hic = []
    data2_rnaseq = []
    data2_micro = []
    data2_pro = []
    data2_gro = []

    for i in allcell.index:
        if topcount < 20:
            data2_chip.append(ProcessedData.objects.filter(experiment='ChIPseq',cell=i).count())
            data2_chia.append(ProcessedData.objects.filter(experiment='ChIAPET',cell=i).count())
            data2_hichip.append(ProcessedData.objects.filter(experiment='HiChIP',cell=i).count())
            data2_hic.append(ProcessedData.objects.filter(experiment='HiC',cell=i).count())
            data2_rnaseq.append(ProcessedData.objects.filter(experiment='RNAseq',cell=i).count())
            data2_micro.append(ProcessedData.objects.filter(experiment='Microarray',cell=i).count())
            data2_pro.append(ProcessedData.objects.filter(experiment='PROseq',cell=i).count())
            data2_gro.append(ProcessedData.objects.filter(experiment='GROseq',cell=i).count())
            data2_label.append(i)
            topcount += 1
        else:
            othercell = set(allcell.index)-set(data2_label)
            data2_chip.append(ProcessedData.objects.filter(experiment='ChIPseq',cell__in=othercell).count())
            data2_chia.append(ProcessedData.objects.filter(experiment='ChIAPET',cell__in=othercell).count())
            data2_hichip.append(ProcessedData.objects.filter(experiment='HiChIP',cell__in=othercell).count())
            data2_hic.append(ProcessedData.objects.filter(experiment='HiC',cell__in=othercell).count())
            data2_rnaseq.append(ProcessedData.objects.filter(experiment='RNAseq',cell__in=othercell).count())
            data2_micro.append(ProcessedData.objects.filter(experiment='Microarray',cell__in=othercell).count())
            data2_pro.append(ProcessedData.objects.filter(experiment='PROseq',cell__in=othercell).count())
            data2_gro.append(ProcessedData.objects.filter(experiment='GROseq',cell__in=othercell).count())
            data2_label.append("Other")
            break

    chart2data = '''[
                    {
                      label:"ChIP-seq",
                      data: ''' + str(data2_chip) + ''',
                      backgroundColor: 'rgb(255, 99, 132)',
                      stack: 'Stack 0',
                    },
                    {
                      label:"ChIA-PET",
                      data: ''' + str(data2_chia) + ''',
                      backgroundColor: '#712F79',
                      stack: 'Stack 0',
                    },
                    {
                      label:"Hi-ChIP",
                      data: ''' + str(data2_hichip) + ''',
                      backgroundColor: '#F7996E',
                      stack: 'Stack 0',
                    },
                    {
                      label:"Hi-C",
                      data: ''' + str(data2_hic) + ''',
                      backgroundColor: '#976391',
                      stack: 'Stack 0',
                    },
                    {
                      label:"RNA-seq",
                      data: ''' + str(data2_rnaseq) + ''',
                      backgroundColor: 'green',
                      stack: 'Stack 0',
                    },
                    {
                      label:"Microarray",
                      data: ''' + str(data2_micro) + ''',
                      backgroundColor: '#4C4C9D',
                      stack: 'Stack 0',
                    },
                    {
                      label:"PRO-seq",
                      data: ''' + str(data2_pro) + ''',
                      backgroundColor: '#48639C',
                      stack: 'Stack 0',
                    },
                    {
                      label:"GRO-seq",
                      data: ''' + str(data2_gro) + ''',
                      backgroundColor: '#orange',
                      stack: 'Stack 0',
                    },
                ]'''

    #-----------Plot3-------------#
    # 减少读取
    allpeaknum = 751590
    #ctcfnum = PeakModel.objects.filter(CTCFdependent="CTCF").count()
    #ctcf_non_num = allpeaknum - ctcfnum
    #data3_ctcf = [ctcfnum, ctcf_non_num]
    data3_promoter = [148152,allpeaknum-148152]

    #enhancer_num = PeakModel.objects.filter(enhancer="Enhancer").count()
    #enhancer_non_num = allpeaknum - enhancer_num
    #data3_enhancer = [enhancer_num,enhancer_non_num]
    data3_enhancer = [36722,allpeaknum-36722]

    #boundary_num = PeakModel.objects.filter(boundary="Boundary").count()
    #boundary_non_num = allpeaknum - boundary_num
    #data3_boundary = [boundary_num, boundary_non_num]
    data3_boundary = [513931,allpeaknum-513931]

    #taget_non_num = PeakModel.objects.filter(subunit="Rad21").count() #临时的，正式版一定要改
    #taget_num = allpeaknum - taget_non_num
    #data3_targetgene = [taget_num,taget_non_num]
    data3_targetgene = [allpeaknum-398325,398325]

    chart3data = '''[
                  {
                    backgroundColor: ['#006d77', '#83c5be'],
                    data:''' + str(data3_promoter) + ''',
                  },
                  {
                    backgroundColor: ['#cc5803', '#ffc971'],
                    data: ''' + str(data3_boundary) + ''',
                  },
                  {
                    backgroundColor: ['#90a955', '#ecf39e'],
                    data: ''' + str(data3_targetgene) + ''',
                  },
                  {
                    backgroundColor: ['#ff4d6d','#ffccd5'],
                    data: ''' + str(data3_enhancer) + ''',
                  },
                ]'''

    chart3label = ['Promoter', 'Non_Promoter','Boundary', 'Non_boundary','Has_target_gene','No_target_gene','Enhancer', 'Non_enhancer',]

    #-----------Plot4-------------#
    allpeaknum = 60607
    dependent_num = GeneModel.objects.filter(triplewheter=True).count()
    data4_dependent = [dependent_num, allpeaknum - dependent_num]

    type_num = GeneModel.objects.filter(looptype__contains="HiC").count()
    data4_type = [type_num, allpeaknum-type_num]

    protein_num = GeneModel.objects.filter(proteincoding="protein_coding").count()
    data4_protein = [protein_num, allpeaknum-protein_num]

    chart4data = '''[
                  {
                    backgroundColor: ['#006d77', '#83c5be'],
                    data:''' + str(data4_dependent) + ''',
                  },
                  {
                    backgroundColor: ['#cc5803', '#ffc971'],
                    data: ''' + str(data4_type) + ''',
                  },
                  {
                    backgroundColor: ['#90a955', '#ecf39e'],
                    data: ''' + str(data4_protein) + ''',
                  },
                ]'''
    chart4label = ['Double-evidence',"Non-Double",'Chromatin loop', 'No loop', 'Protein_coding','Non_coding']

    #-------------Plot5--------------#
    allstudy = pd.value_counts(ProcessedData.objects.values_list('access',flat=True))
    chart5data = []
    for i in range(len(allstudy)):
        if i < 40:
            chart5data.append(
                {
                    'name': allstudy.index[i],
                    'children': [ { 'name': allstudy.index[i], 'value': allstudy.values[i]},],
                }
            )
            topcount += 1
        else:
            chart5data.append(
                {
                    'name': allstudy.index[i],
                    'children': [ { 'name': "Other", 'value': sum(allstudy.values[i:])},],
                }
            )
            break



    return render(request,'demoSite/statisticpage/statistic.html',{'section':'statistic','chart1data':chart1data,
                                                            'chart2data':chart2data,'chart2label':data2_label,
                                                            'chart3data':chart3data,'chart3label':chart3label,
                                                            'chart4data':chart4data,'chart4label':chart4label,
                                                            'chart5data':chart5data, })
