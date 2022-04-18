from django.core.management.base import BaseCommand
from demoSite.models import ProcessedData
import datetime
import os
import random

def import_raw():
    for i in os.listdir("/Library/WebServer/Documents/CohesinDB/"):
        fields = i.split("_")

        experiment = fields[0]
        modules = random.sample(('cohesin-target'),1)[0],
        if experiment in ['ChIAPET','ChIPseq']:
            antibody = fields[3]
        elif experiment == 'HiC':
            antibody = None
        cell = fields[2]
        biosample = random.sample(('cell line','primary','tissue'),1)[0],
        tissue = random.sample(('testtissue1','testtissue2','testtissue3'),1)[0],
        access = fields[1]
        data_date = datetime.datetime(random.randint(2000,2021),1,1)
        treat = fields[4]
        phenotype = fields[5]
        disease = random.sample(('normal','cancer','normal','cdls'),1)[0]
        status = 'highQC'
        content = "/Library/WebServer/Documents/CohesinDB/"+i

        pdata = ProcessedData(
            experiment=experiment,
            antibody=antibody,
            cell=cell,
            biosample=biosample,
            tissue=tissue,
            access=access,
            data_date=data_date,
            treat=treat,
            phenotype=phenotype,
            disease=disease,
            status=status,
            content=content
        )
        pdata.save()

class Command(BaseCommand):
    help = 'Import real data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin import'))
        import_raw()
        self.stdout.write(self.style.SUCCESS('end import'))
