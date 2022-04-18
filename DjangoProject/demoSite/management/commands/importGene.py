from django.core.management.base import BaseCommand
from demoSite.models import GeneModel
import pandas as pd
import numpy as np
import os

def importGene():
    GeneModel.objects.all().delete()
    allgene = pd.read_csv("/home/support/wang/Production_data/allgene.final.tsv.gz",sep="\t")

    for i in range(allgene.shape[0]):
        onegene = allgene.iloc[i,:].copy()
        if (i/1000) % 1 == 0:
            print(i)

        if not onegene[9] and not onegene[13] and not onegene[17]:
            relatedtype = '.'
        else:
            relatedtype = ''
            if onegene[9]: relatedtype += "Interaction"+","
            if onegene[13]: relatedtype += "DEGs"+","
            if onegene[17]: relatedtype += "Coexpression"+","
            relatedtype = relatedtype[:-1]

        onegenedata = GeneModel(
            cdbid = "CDBG"+('%08d' % (int(i)+1)),
            geneID = onegene[0],
            genesymbol = onegene[1],
            geneposition = onegene[2]+":"+ str(onegene[3])+"-"+str(onegene[4]),
            chromosome = onegene[2],
            start = onegene[3],
            end = onegene[4],
            strand = onegene[5],
            proteincoding = onegene[6],

            #whether triple
            triplewheter = onegene[7],
            triplecohesin = onegene[8],
            relatedtype = relatedtype.replace("Coexpression",""),

            #whether loop
            loopwhether = onegene[9],
            looptype = onegene[10],
            loopstudy = onegene[11],
            loopsubunit = onegene[12],

            #whether DEG
            degwhether = onegene[13],
            degnumberstudy = onegene[14],
            degstudy = onegene[15],
            degsubunit = onegene[16],

            #whether co-express
            correlationwhether = onegene[17],
            correlationRho = onegene[18],
            correlationFDR = onegene[19],
            correlationsubunit = onegene[20],
        )

        onegenedata.save()

class Command(BaseCommand):
    help = 'Import PeakModel and GeneModel'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin import'))
        importGene()
        self.stdout.write(self.style.SUCCESS('end import'))
