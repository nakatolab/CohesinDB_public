from django.core.management.base import BaseCommand
from demoSite.models import GTExData
import datetime
import os
import random
import pandas as pd
import numpy as np

def gini_func(array):
    """Calculate the Gini coefficient of a numpy array."""
    # based on bottom eq:
    # http://www.statsdirect.com/help/generatedimages/equations/equation154.svg
    # from:
    # http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    # All values are treated equally, arrays must be 1d:
    array = array.flatten()
    if np.amin(array) < 0:
        # Values cannot be negative:
        array -= np.amin(array)
    # Values cannot be 0:
    array += 0.0000001
    # Values must be sorted:
    array = np.sort(array)
    # Index per array element:
    index = np.arange(1,array.shape[0]+1)
    # Number of array elements:
    n = array.shape[0]
    # Gini coefficient:
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))

def import_GTEx():
    GTExData.objects.all().delete()
    alldf = pd.read_csv("/home/support/wang/Production_data/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct.gz", sep="\t",skiprows=2)
    for row in range(alldf.shape[0]):
        if (row/1000) % 1 == 0: print(row)
        gd = GTExData(
            cdbid = "CDBGTEX"+('%05d' % (int(row)+1)),
            geneID = alldf.iloc[row,0].split(".")[0],
            genesymbol = alldf.iloc[row,1],
            tissuename = list(alldf.iloc[row,2:].index),
            tissuemedian = list(alldf.iloc[row,2:].values),
            gini = gini_func(alldf.iloc[row,2:].values),
        )
        gd.save()

class Command(BaseCommand):
    help = 'Import GTEx data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin import GTEx'))
        import_GTEx()
        self.stdout.write(self.style.SUCCESS('end import GTEx'))
