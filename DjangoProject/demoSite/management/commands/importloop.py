from django.core.management.base import BaseCommand
from demoSite.models import LoopModel, CellType
import pandas as pd
import numpy as np
import os
import random

def importLoop():
    LoopModel.objects.all().delete()
    allloop = pd.read_csv("/home/support/wang/Production_data/allloop.final.tsv.gz",sep="\t")

    for i in range(allloop.shape[0]):
        oneloop = allloop.iloc[i,:].copy()
        if (i/10000) % 1 == 0: print(i)

        oneloopdata = LoopModel(
            cdbid = "CDBL"+('%08d' % (int(i)+1)),
            chrom1 = oneloop[0],
            start1 = oneloop[1],
            end1 = oneloop[2],
            chrom2 = oneloop[3],
            start2 = oneloop[4],
            end2 = oneloop[5],
            assay = oneloop[6],
            subunit = oneloop[7],
            celltype = ",".join(list(set(CellType.objects.filter(dataname__in=oneloop[8].split(",")).values_list("cellname",flat=True)))),
            study = oneloop[9],
            looplength = oneloop[10],
            loopwidth = int(oneloop[2]) - int(oneloop[1]),
        )

        oneloopdata.save()

class Command(BaseCommand):
    help = 'Import LoopModel'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin import'))
        importLoop()
        self.stdout.write(self.style.SUCCESS('end import'))
