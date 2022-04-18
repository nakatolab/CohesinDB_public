from django.core.management.base import BaseCommand
from demoSite.models import ProcessedData, CellType
import datetime
import os
import random

treat2SubunitDic = {'SMC1-KO':'SMC1', 'Rad21mock':'Rad21', 'SA2-CRISPR-homozygous':'SA2', 'SMC3-CRISPR':'SMC3', 'shSMC3':'SMC3',
                    'Rad21-auxin':'Rad21', 'SA2-KO':'SA2', 'NT':None, 'siSMC3':'SMC3', 'WAPL-AID':'WAPL', 'mutSA2':'SA2', 'shSMC1':'SMC1',
                    'shRad21':'Rad21', 'Rad21mut':'Rad21', 'CHOP':'AFF4', 'shNIPBL':'NIPBL', 'shSA2':'SA2', 'shCTCF':'CTCF', 'SA1-AID':'SA1',
                    'overSMC1':'SMC1', 'siRad21-6h':'Rad21', 'siRad21-3h':'Rad21', 'siRad21':'Rad21', 'Rad21-CRISPR':'Rad21',
                    'SA2-CRISPR':'SA2', 'SMC1mut':'SMC1', 'shBORIS':'Other', 'SA2-CRISPR-heterozygous':'SA2',
                    'siESCO1':'ESCO1', 'siSA2':'SA2', 'siSA1':'SA1', 'siCTCF':'CTCF', 'CdLS':'NIPBL', 'JQ1':'Other', 'Auxin':'Rad21',
                    'CTCF-CRISPR':'CTCF', 'SA2KO':'SA2', 'SA2-AID':'SA2', 'shSA1':'SA1'}

def importPostProcess():
    namelist = sorted(os.listdir("/mnt/NAS/WangDB/CohesinDB_processed_Post2021Dec"))
    prefixlist = sorted(set([".".join(i.split(".")[0:-1]) for i in namelist]))
    CDB_id = 1971

    for eachfile in prefixlist:
        print(eachfile)
        datacell = eachfile.split("_")[2]
        dataassay = eachfile.split("_")[0]


        eachstudy = eachfile.split("_")[1]
        if eachstudy[:3] == "GSE":
            weblink = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc="+eachstudy
        elif eachstudy[:3] == "4DN":
            weblink = "https://data.4dnucleome.org/experiment-set-replicates/"+eachstudy
        elif eachstudy[:3] == "ENC":
            weblink = "https://www.encodeproject.org/experiments/"+eachstudy
        else:
            weblink = "#"

        if dataassay in ["HiC"]:
            pdata = ProcessedData(
                cdbid = "CDBD"+('%05d' % CDB_id),
                experiment = eachfile.split("_")[0],
                modules = "Cohesin-3Dgenome",
                restriction = eachfile.split("_")[3],
                cell = CellType.objects.get(dataname=datacell).cellname,
                tissue = CellType.objects.get(dataname=datacell).tissue,
                biosample = CellType.objects.get(dataname=datacell).biosample.replace(" ","-"),
                disease = CellType.objects.get(dataname=datacell).disease,
                access = eachstudy,
                link = weblink,
                treat1 = eachfile.split("_")[4],
                treat2 = eachfile.split("_")[5],
                content1 = "/mnt/NAS/WangDB/CohesinDB_processed_Post2021Dec/"+eachfile+".hic",
                content2 = "/mnt/NAS/WangDB/CohesinDB_processed_Post2021Dec/"+eachfile+".tad",
            )
            pdata.save()
            CDB_id += 1


def importProcessed():
    CDB_id = 1
    ProcessedData.objects.all().delete()
    namelist = sorted(os.listdir("/mnt/NAS/WangDB/CohesinDB_processed_file"))
    prefixlist = sorted(set([".".join(i.split(".")[0:-1]) for i in namelist]))


    compare2SubunitDic = {}
    for i in prefixlist:
        if i.split("_")[0] in ["RNAseq","PROseq","GROseq"] and i.split("_")[4] != 'NT':
            compare2SubunitDic[i.split("_")[3]] = treat2SubunitDic[i.split("_")[4]]

    for eachfile in prefixlist:
        datacell = eachfile.split("_")[2]
        dataassay = eachfile.split("_")[0]
        eachstudy = eachfile.split("_")[1].replace("ShirahigeLab-NatGen2015","SRP050576-ShirahigeLab").replace("ShirahigeLab-GSE177045","GSE177045-ShirahigeLab")
        if eachstudy == "SRP050576-ShirahigeLab":
            weblink = "https://www.ncbi.nlm.nih.gov/sra?term=SRP050576"
        elif eachstudy == "GSE177045-ShirahigeLab":
            weblink = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE177045"
        elif eachstudy == "SRP050576-ShirahigeLab":
            weblink = "https://www.ncbi.nlm.nih.gov/sra?term=SRP050576"
        elif eachstudy[:3] == "GSE":
            weblink = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc="+eachstudy
        elif eachstudy[:3] == "4DN":
            weblink = "https://data.4dnucleome.org/experiment-set-replicates/"+eachstudy
        elif eachstudy[:3] == "ENC":
            weblink = "https://www.encodeproject.org/experiments/"+eachstudy
        else:
            weblink = "#"

        if dataassay == "Microarray":
            print(eachfile)
            sample_num = eachfile.split("_")[-1][:-7]
            print(sample_num)

            if eachfile.split("_")[4] == 'CHOP':
                disease = 'CHOP'
            elif eachfile.split("_")[4] == 'CdLS':
                disease = 'CdLS'
            else:
                disease = CellType.objects.get(dataname=datacell).disease

            for i in range(int(sample_num)):
                pdata = ProcessedData(
                    cdbid = "CDBD"+('%05d' % CDB_id),
                    experiment = "Microarray",
                    modules = "Cohesin-DEGs",
                    compareID = eachfile.split("_")[3].replace("compare", "group"),
                    cell = CellType.objects.get(dataname=datacell).cellname,
                    tissue = CellType.objects.get(dataname=datacell).tissue,
                    biosample = CellType.objects.get(dataname=datacell).biosample.replace(" ","-"),
                    disease = disease,
                    access = eachstudy,
                    link = weblink,
                    subunit = treat2SubunitDic[eachfile.split("_")[4]],
                    treat1 = eachfile.split("_")[4]+"_vs_Control",
                    content1 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile+".tsv",
                    content2 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile+".tsv",
                )
                pdata.save()
                CDB_id += 1
        elif dataassay in ["RNAseq","PROseq","GROseq"]:
            if eachfile[-4:] in ['STAR',]:
                pass
            else:
                print(eachfile)
                if eachfile.split("_")[4] == 'CHOP':
                    disease = 'CHOP'
                elif eachfile.split("_")[4] == 'CdLS':
                    disease = 'CdLS'
                else:
                    disease = CellType.objects.get(dataname=datacell).disease

                if eachfile.split("_")[4] == "NT":
                    print(eachfile.split("_")[3])

                pdata = ProcessedData(
                    cdbid = "CDBD"+('%05d' % CDB_id),
                    experiment = eachfile.split("_")[0],
                    modules = "Cohesin-DEGs",
                    compareID = eachfile.split("_")[3].replace("compare", "group"),
                    cell = CellType.objects.get(dataname=datacell).cellname,
                    tissue = CellType.objects.get(dataname=datacell).tissue,
                    biosample = CellType.objects.get(dataname=datacell).biosample.replace(" ","-"),
                    disease = disease,
                    access = eachstudy,
                    link = weblink,
                    treat1 = eachfile.split("_")[4],
                    subunit = compare2SubunitDic[eachfile.split("_")[3]],
                    content1 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile+".tsv",
                    content2 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile.replace("edgeR",'STAR')+".tsv",
                )
                pdata.save()
                CDB_id += 1

        elif dataassay in ["ChIAPET"]:
            print(eachfile)
            if eachfile[-3:] in ['nge','.gz']:
                pass
            else:
                pdata = ProcessedData(
                    cdbid = "CDBD"+('%05d' % CDB_id),
                    experiment = eachfile.split("_")[0],
                    modules = "Cohesin-3Dgenome",
                    antibody = eachfile.split("_")[3],
                    subunit = eachfile.split("_")[3],
                    cell = CellType.objects.get(dataname=datacell).cellname,
                    tissue = CellType.objects.get(dataname=datacell).tissue,
                    biosample = CellType.objects.get(dataname=datacell).biosample.replace(" ","-"),
                    disease = CellType.objects.get(dataname=datacell).disease,
                    access = eachstudy,
                    link = weblink,
                    treat1 = eachfile.split("_")[4],
                    treat2 = eachfile.split("_")[5],
                    content1 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile+".longrange.gz",
                    content2 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile+".bedpe",
                )
                pdata.save()
                CDB_id += 1

        elif dataassay in ["HiC"]:
            print(eachfile)
            pdata = ProcessedData(
                cdbid = "CDBD"+('%05d' % CDB_id),
                experiment = eachfile.split("_")[0],
                modules = "Cohesin-3Dgenome",
                restriction = eachfile.split("_")[3],
                cell = CellType.objects.get(dataname=datacell).cellname,
                tissue = CellType.objects.get(dataname=datacell).tissue,
                biosample = CellType.objects.get(dataname=datacell).biosample.replace(" ","-"),
                disease = CellType.objects.get(dataname=datacell).disease,
                access = eachstudy,
                link = weblink,
                treat1 = eachfile.split("_")[4],
                treat2 = eachfile.split("_")[5],
                content1 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile+".hic",
                content2 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile+".loop",
                content3 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile+".tad",
            )
            pdata.save()
            CDB_id += 1

        elif dataassay in ["ChIPseq",'HiChIP']:
            print(eachfile)
            if eachfile[-3:] in ['aks',]:
                pass
            else:
                if dataassay == "ChIPseq":
                    content1 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile+".bw"
                    content2 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile.replace("-bowtie2-hg38-raw-GR.100","_peaks")+".narrowPeak"
                    module = "Cohesin-Binding"
                elif dataassay == "HiChIP":
                    content1 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile+".hic"
                    content2 = "/mnt/NAS/WangDB/CohesinDB_processed_file/"+eachfile+".loop"
                    module = "Cohesin-3Dgenome"

                if eachfile.split("_")[3] in ['NIPBL-antibody1','NIPBL-antibody2','NIPBL-antibody3','NIPBL-antibody4']:
                    antibody = 'NIPBL'
                    subunit = 'NIPBL'
                else:
                    antibody = eachfile.split("_")[3]
                    subunit = eachfile.split("_")[3]

                if eachfile.split("_")[4] == 'CdLS' or eachfile.split("_")[5] == 'CdLS':
                    disease = 'CdLS'
                elif eachfile.split("_")[4] == 'CHOP' or eachfile.split("_")[5] == 'CHOP':
                    disease = 'CHOP'
                else:
                    disease = CellType.objects.get(dataname=datacell).disease

                pdata = ProcessedData(
                    cdbid = "CDBD"+('%05d' % CDB_id),
                    experiment = eachfile.split("_")[0],
                    modules = module,
                    antibody = antibody,
                    subunit = subunit,
                    cell = CellType.objects.get(dataname=datacell).cellname,
                    tissue = CellType.objects.get(dataname=datacell).tissue,
                    biosample = CellType.objects.get(dataname=datacell).biosample.replace(" ","-"),
                    disease = disease,
                    access = eachstudy,
                    link = weblink,
                    treat1 = eachfile.split("_")[4],
                    treat2 = eachfile.split("_")[5],
                    content1 = content1,
                    content2 = content2,
                )
                pdata.save()
                CDB_id += 1


class Command(BaseCommand):
    help = 'Import PeakModel and GeneModel'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin import'))
        importProcessed()
        importPostProcess()
        self.stdout.write(self.style.SUCCESS('end import'))
