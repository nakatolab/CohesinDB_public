from django.core.management.base import BaseCommand
from demoSite.models import ProcessedData, PeakModel, GeneModel, CellType
import pandas as pd
import numpy as np
import os

def importPeak():
    PeakModel.objects.all().delete()
    allpeak = pd.read_csv("/home/support/wang/Production_data/allcohesin.final.tsv.gz",sep="\t")

    for i in range(allpeak.shape[0]):
        if (i/1000) % 1 == 0: print(i)
        onepeak = allpeak.iloc[i,:].copy()

        genomiclocation = onepeak[8].replace("Intra","Intragenic").replace("Inter","Intergenic")

        onepeakdata = PeakModel(
            #basic
            cdbid = "CDBP"+('%08d' % (int(i)+1)),
            chromosome = onepeak[0],
            start = int(onepeak[1]),
            end = int(onepeak[2]),
            slug = str(onepeak[0]) + "-" + str(onepeak[1]) + "-" + str(onepeak[2]),
            datasource = onepeak[3],
            #celltype = onepeak[4],
            celltype = ",".join(list(set(CellType.objects.filter(dataname__in=onepeak[4].split(",")).values_list("cellname",flat=True)))),

            #Category
            peakoccupancy = onepeak[5],
            cellspecificity = 1- (len(onepeak[4].split(",")) / 90) ,
            subunit = onepeak[6],
            CTCFdependent = onepeak[7],
            location = genomiclocation,

            #3D-genome
            boundary = onepeak[9],
            hubs = onepeak[10],
            hicloop = onepeak[11],
            hicchiploop = onepeak[12],
            chialoop = onepeak[13],

            #Cis
            enhancer = onepeak[14],
            cobind = onepeak[15],
            targetgene = onepeak[16],
            targetgeneID = onepeak[17],

            #Function
            snp = onepeak[18],
            codingmut = onepeak[19],
            noncodingmut = onepeak[20],

            #Addition April 2022
            CTCFmotif = onepeak[21],
            superenhancer = onepeak[22],
            compartmentA =  float(onepeak[23]),
            HMMtop1name =  onepeak[24],
            HMMtop1percent = float(onepeak[25]),
            HMMtop2name =  onepeak[26],
            HMMtop2percent = float(onepeak[27]),
        )

        onepeakdata.save()


class Command(BaseCommand):
    help = 'Import PeakModel'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin import'))
        importPeak()
        self.stdout.write(self.style.SUCCESS('end import'))
