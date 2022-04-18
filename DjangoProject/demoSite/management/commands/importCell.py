from django.core.management.base import BaseCommand
from demoSite.models import CellType
import datetime
import os
import random
import pandas as pd
import numpy as np

def import_cell():
    CellType.objects.all().delete()
    allcell = pd.read_csv("../Alldata_celltype.txt", sep="\t")
    for row in range(allcell.shape[0]):
        cp = CellType(
            cdbid = "CDBCELL"+('%05d' % (int(row)+1)),
            dataname = allcell.iloc[row,0],
            cellname = allcell.iloc[row,1],
            tissue = allcell.iloc[row,2],
            biosample = allcell.iloc[row,3],
            disease = allcell.iloc[row,4],
            description = allcell.iloc[row,5],
            link = allcell.iloc[row,6],
        )
        cp.save()

class Command(BaseCommand):
    help = 'Import cell type data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin import cell type'))
        import_cell()
        self.stdout.write(self.style.SUCCESS('end import cell type'))
