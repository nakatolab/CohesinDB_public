from django.db import models
import datetime
from django.urls import reverse

# Create your models here.

class PeakModel(models.Model):
    #basic
    cdbid = models.SlugField(default='CDBP00000001')
    chromosome = models.CharField(max_length=50,default=None)
    start = models.IntegerField()
    end = models.IntegerField()
    slug = models.SlugField(max_length=100)
    datasource = models.TextField()
    celltype = models.TextField()

    #Addition April 2022
    CTCFmotif = models.CharField(max_length=20,default=None)
    superenhancer = models.CharField(max_length=20,default=None)
    compartmentA =  models.DecimalField(max_digits=10,decimal_places=6,default=None)
    HMMtop1name =  models.CharField(max_length=50,default=None)
    HMMtop1percent = models.DecimalField(max_digits=10,decimal_places=6,default=None)
    HMMtop2name =  models.CharField(max_length=50,default=None)
    HMMtop2percent = models.DecimalField(max_digits=10,decimal_places=6,default=None)

    #Category
    peakoccupancy = models.FloatField()
    cellspecificity = models.FloatField()
    subunit = models.CharField(max_length=1000)
    CTCFdependent = models.CharField(max_length=20)
    location = models.CharField(max_length=50,default=None)

    #3D-genome
    boundary = models.CharField(max_length=20)
    hubs = models.CharField(max_length=20)
    hicloop = models.CharField(max_length=20,default=None)
    hicchiploop = models.CharField(max_length=20,default=None)
    chialoop = models.CharField(max_length=20,default=None)

    #Cis
    enhancer = models.CharField(max_length=20)
    cobind = models.TextField()
    targetgene = models.TextField()
    targetgeneID = models.TextField()

    #Function
    snp = models.TextField()
    codingmut = models.IntegerField(default=None)
    noncodingmut = models.IntegerField(default=None)

    class Meta:
        ordering = ('chromosome','start',)

    def __str__(self):
        return str(self.chromosome)+"_"+str(self.start)+"_"+str(self.end)

class GeneModel(models.Model):
    # gene information
    cdbid = models.SlugField(default='CDBG00000001')
    geneID = models.CharField(max_length=50)
    genesymbol = models.CharField(max_length=50)
    geneposition = models.CharField(max_length=50)
    chromosome = models.CharField(max_length=50,default=None)
    start = models.IntegerField(default=None)
    end = models.IntegerField(default=None)
    strand = models.CharField(max_length=5,default=None)
    proteincoding =  models.CharField(max_length=50,default=None)

    # whether triple
    triplewheter = models.BooleanField(default=None)
    triplecohesin = models.TextField(default=None)
    relatedtype = models.CharField(max_length=50,default=None)

    #whether loop
    loopwhether = models.BooleanField(default=None)
    looptype = models.CharField(max_length=50,default=None)
    loopstudy = models.TextField(default=None)
    loopsubunit = models.CharField(max_length=50,default=None)

    #whether DEG
    degwhether = models.BooleanField(default=None)
    degnumberstudy = models.IntegerField(default=None)
    degstudy = models.TextField(default=None)
    degsubunit = models.CharField(max_length=50,default=None)

    #whether co-express
    correlationwhether = models.BooleanField(default=None)
    correlationRho = models.FloatField(default=None)
    correlationFDR = models.FloatField(default=None)
    correlationsubunit = models.TextField(default=None)

    class Meta:
        ordering = ('geneposition',)

    def __str__(self):
        return str(self.genesymbol)


class ExampleGeneModel(models.Model):
    # gene information
    cdbid = models.SlugField(default='CDBG00000001')
    geneID = models.CharField(max_length=50,default=None)
    genesymbol = models.CharField(max_length=50,default=None)
    geneposition = models.CharField(max_length=50,default=None)
    chromosome = models.CharField(max_length=50,default=None)
    start = models.IntegerField(default=None)
    end = models.IntegerField(default=None)
    strand = models.CharField(max_length=5,default=None)
    proteincoding =  models.CharField(max_length=50,default=None)

    # whether triple
    triplewheter = models.BooleanField(default=None)
    triplecohesin = models.TextField(default=None)
    relatedtype = models.CharField(max_length=50,default=None)

    #whether loop
    loopwhether = models.BooleanField(default=None)
    looptype = models.CharField(max_length=50,default=None)
    loopstudy = models.TextField(default=None)
    loopsubunit = models.CharField(max_length=50,default=None)

    #whether DEG
    degwhether = models.BooleanField(default=None)
    degnumberstudy = models.IntegerField(default=None)
    degstudy = models.TextField(default=None)
    degsubunit = models.CharField(max_length=50,default=None)

    #whether co-express
    correlationwhether = models.BooleanField(default=None)
    correlationRho = models.FloatField(default=None)
    correlationFDR = models.FloatField(default=None)
    correlationsubunit = models.TextField(default=None)

    class Meta:
        ordering = ('geneposition',)

    def __str__(self):
        return str(self.genesymbol)

class ExamplePeakModel(models.Model):
    #Addition April 2022
    CTCFmotif = models.CharField(max_length=20,default=None)
    superenhancer = models.CharField(max_length=20,default=None)
    compartmentA =  models.DecimalField(max_digits=10,decimal_places=6,default=None)
    HMMtop1name =  models.CharField(max_length=50,default=None)
    HMMtop1percent = models.DecimalField(max_digits=10,decimal_places=6,default=None)
    HMMtop2name =  models.CharField(max_length=50,default=None)
    HMMtop2percent = models.DecimalField(max_digits=10,decimal_places=6,default=None)

    #basic
    cdbid = models.SlugField(default='CDBP00000001')
    chromosome = models.CharField(max_length=50,default=None)
    start = models.IntegerField()
    end = models.IntegerField()
    slug = models.SlugField(max_length=100)
    datasource = models.TextField()
    celltype = models.TextField()

    #Category
    peakoccupancy = models.FloatField()
    cellspecificity = models.FloatField()
    subunit = models.CharField(max_length=1000)
    CTCFdependent = models.CharField(max_length=20)
    location = models.CharField(max_length=50,default=None)

    #3D-genome
    boundary = models.CharField(max_length=20)
    hubs = models.CharField(max_length=20)
    hicloop = models.CharField(max_length=20,default=None)
    hicchiploop = models.CharField(max_length=20,default=None)
    chialoop = models.CharField(max_length=20,default=None)

    #Cis
    enhancer = models.CharField(max_length=20)
    cobind = models.TextField()
    targetgene = models.TextField()
    targetgeneID = models.TextField()

    #Function
    snp = models.TextField()
    codingmut = models.IntegerField(default=None)
    noncodingmut = models.IntegerField(default=None)

    class Meta:
        ordering = ('chromosome','start',)

    def __str__(self):
        return str(self.chromosome)+"_"+str(self.start)+"_"+str(self.end)


class LoopModel(models.Model):
    cdbid = models.SlugField(default='CDBL00000001')
    chrom1 = models.CharField(max_length=50)
    start1 = models.IntegerField()
    end1 = models.IntegerField()
    chrom2 = models.CharField(max_length=50)
    start2 = models.IntegerField()
    end2 = models.IntegerField()
    assay = models.CharField(max_length=100,default=None)
    subunit = models.CharField(max_length=100)
    celltype = models.CharField(max_length=1000)
    study = models.TextField()
    looplength = models.IntegerField()
    loopwidth = models.IntegerField()

class ExampleLoopModel(models.Model):
    cdbid = models.SlugField(default='CDBL00000002')
    chrom1 = models.CharField(max_length=50)
    start1 = models.IntegerField()
    end1 = models.IntegerField()
    chrom2 = models.CharField(max_length=50)
    start2 = models.IntegerField()
    end2 = models.IntegerField()
    assay = models.CharField(max_length=100)
    subunit = models.CharField(max_length=100)
    celltype = models.CharField(max_length=1000)
    study = models.TextField()
    looplength = models.IntegerField()
    loopwidth = models.IntegerField()

class UpdateNew(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    publishtime = models.DateTimeField(default=datetime.datetime.now)
    content = models.TextField(max_length=200)

    class Meta:
        ordering = ('-publishtime',)

    def __str__(self):
        return self.title


class CellType(models.Model):
    cdbid = models.SlugField(default='CDBCELL00001')
    created = models.DateTimeField(auto_now_add=True)
    dataname = models.CharField(max_length=100)
    cellname = models.CharField(max_length=100)
    tissue = models.CharField(max_length=100)
    biosample = models.CharField(max_length=50)
    disease = models.CharField(max_length=100)
    description = models.TextField()
    link = models.TextField()

    class Meta:
        ordering = ('cellname',)

    def __str__(self):
        return self.dataname

class GTExData(models.Model):
    cdbid = models.SlugField(default='CDBGTEX00001')
    geneID = models.CharField(max_length=50,default=None)
    genesymbol = models.CharField(max_length=50,default=None)
    gini = models.FloatField(default=None)
    tissuename = models.TextField()
    tissuemedian = models.TextField()

class ProcessedData(models.Model):
    STATUS_CHOICES =(
        ('highQC','HighQC'),
        ('lowQC','LowQC'),
        ('test','ForTest'),
    )

    MODULES_TYPE = (
        ('Cohesin-Binding','Cohesin-Binding'),
        ('Cohesin-3Dgenome','Cohesin-3Dgenome'),
        ('Cohesin-DEGs','Cohesin-DEGs'),
    )

    DATA_CHOICES =(
        ('ChIPseq','ChIP-seq'),
        ('ChIAPET','ChIA-PET'),
        ('HiChIP','Hi-ChIP'),
        ('HiC','Hi-C'),
        ('RNAseq','RNA-seq'),
        ('Microarray','Microarray'),
        ('PROseq','PRO-seq'),
        ('GROseq','GRO-seq'),
    )

    #created = models.DateTimeField(auto_now_add=True)
    #updated = models.DateTimeField(auto_now=True)
    cdbid = models.SlugField(default='CDBD00001')
    experiment = models.CharField(max_length=10, choices=DATA_CHOICES, default='ChIPseq')
    modules = models.CharField(max_length=20, choices=MODULES_TYPE,default='cohesin-binding')
    antibody = models.CharField(max_length=50,null=True)
    subunit = models.CharField(max_length=50,null=True) #for ChIP-seq, ChIA, Hi-ChIP means antibody; for cohesin-KD means subunit
    compareID = models.CharField(max_length=50,null=True) #for RNAseq,Microarray
    restriction = models.CharField(max_length=50,null=True) #for Hi-C
    cell = models.CharField(max_length=100)
    tissue = models.CharField(max_length=100,default="Breast")
    biosample = models.CharField(max_length=100,default="Cell line")
    disease = models.CharField(max_length=20,default="Normal")
    access = models.CharField(max_length=100)
    link = models.CharField(max_length=1000)
    #data_date = models.DateField()
    treat1 = models.CharField(max_length=100,default="NT")
    treat2 = models.CharField(max_length=100,default="NT")
    #status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='highQC')
    content1 = models.FileField(max_length=200)
    content2 = models.FileField(max_length=200,null=True)
    content3 = models.FileField(max_length=200,null=True)

    class Meta:
        ordering = ("-cdbid",)

    def __str__(self):
        return str(self.access)+"_"+str(self.antibody)+"_"+str(self.treat1)+"_"+str(self.treat2)+"_"+str(self.cdbid)

    def get_absolute_url(self):
        if self.experiment == None: self.experiment= "0"
        if self.modules == None: pass
        return reverse('demoSite:datapage_filter',args=[self.modules,self.experiment])
