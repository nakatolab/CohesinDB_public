from django.core.management.base import BaseCommand
from demoSite.models import ProcessedData
import datetime
import os
import random

def fake_data():
    filename = str(random.random())+".txt"
    os.system("touch /Users/wangjiankang/figureServer/June2021/fakeData/"+filename)
    pdata = ProcessedData(
        experiment = random.sample(('chipseq','rnaseq','chiapet','hic'),1)[0],
        modules = random.sample(('cohesin-target','cohesin-dependent'),1)[0],
        antibody = random.sample(('Rad21','NIPBL','SA1','SA2','CTCF',None,),1)[0],
        cell = random.sample(('MCF-7','Bcell','Fibroblast','A549','293T','FakeCellA','FakeCellB','FakeCellC','FakeCellD','FakeCellF','FakeCellE'),1)[0],
        biosample = random.sample(('cell line','primary','tissue'),1)[0],
        tissue = random.sample(('blood','kidney','brain','lung'),1)[0],
        access = 'GSE0000'+str(random.randint(0,100)),
        data_date = datetime.datetime(random.randint(2000,2021),1,1),
        treat = random.sample(('NT','NT','E2','FBS'),1)[0],
        phenotype =random.sample(('widetype','Rad21KD','CTCFKD','NIPBLKD'),1)[0],
        disease = random.sample(('normal','cancer','normal','cdls'),1)[0],
        status = 'ForTest',
        content = "/Users/wangjiankang/figureServer/June2021/fakeData/"+filename
    )
    pdata.save()

class Command(BaseCommand):
    help = 'Import init data for test'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin import'))
        for i in range(50):
            fake_data()
        self.stdout.write(self.style.SUCCESS('end import'))
