from django.core.management.base import BaseCommand
from demoSite.models import ExampleLoopModel, LoopModel, ExamplePeakModel, PeakModel, ExampleGeneModel, GeneModel
import pandas as pd
import numpy as np
import os
import random
from django.db.models import Q

def import_example_object():
    ExampleLoopModel.objects.all().delete()
    examples = LoopModel.objects.filter(Q(chrom1='chr21',start1__gte=16000000,end1__lte=16500000) | Q(chrom2='chr21',start2__gte=16000000,end2__lte=16500000))

    for example in examples:

        oneloopdata = ExampleLoopModel(
            cdbid = example.cdbid,
            chrom1 = example.chrom1,
            start1 = example.start1,
            end1 = example.end1,
            chrom2 = example.chrom2,
            start2 = example.start2,
            end2 = example.end2,
            assay = example.assay,
            subunit = example.subunit,
            celltype = example.celltype,
            study = example.study,
            looplength = example.looplength,
            loopwidth = example.loopwidth,
        )

        oneloopdata.save()

    ExamplePeakModel.objects.all().delete()
    peaks = PeakModel.objects.filter(chromosome="chr21").filter(start__gte=26000000).filter(end__lte=26500000)
    for peak in peaks:
        onepeakdata = ExamplePeakModel(
            #basic
            cdbid = peak.cdbid,
            chromosome = peak.chromosome,
            start = peak.start,
            end = peak.end,
            slug = peak.slug,
            datasource = peak.datasource,
            celltype = peak.celltype,

            #Category
            peakoccupancy = peak.peakoccupancy,
            cellspecificity = peak.cellspecificity,
            subunit = peak.subunit,
            CTCFdependent = peak.CTCFdependent,
            location = peak.location,

            #3D-genome
            boundary = peak.boundary,
            hubs = peak.hubs,
            hicloop = peak.hicloop,
            hicchiploop = peak.hicchiploop,
            chialoop = peak.chialoop,

            #Cis
            enhancer = peak.enhancer,
            cobind = peak.cobind,
            targetgene = peak.targetgene,
            targetgeneID = peak.targetgeneID,

            #Function
            snp = peak.snp,
            codingmut = peak.codingmut,
            noncodingmut = peak.noncodingmut,

            #Addition April 2022
            CTCFmotif = peak.CTCFmotif,
            superenhancer = peak.superenhancer,
            compartmentA =  peak.compartmentA,
            HMMtop1name =  peak.HMMtop1name,
            HMMtop1percent = peak.HMMtop1percent,
            HMMtop2name =  peak.HMMtop2name,
            HMMtop2percent = peak.HMMtop2percent,
        )

        onepeakdata.save()

    ExampleGeneModel.objects.all().delete()
    genes = GeneModel.objects.filter(chromosome="chr21").filter(start__gte=16000000).filter(end__lte=18000000)
    for gene in genes:
        onegenedata = ExampleGeneModel(
            cdbid = gene.cdbid,
            geneID = gene.geneID,
            genesymbol = gene.genesymbol,
            geneposition = gene.geneposition,
            chromosome = gene.chromosome,
            start = gene.start,
            end = gene.end,
            strand = gene.strand,
            proteincoding = gene.proteincoding,

            #whether triple
            triplewheter = gene.triplewheter,
            triplecohesin = gene.triplecohesin,
            relatedtype = gene.relatedtype,

            #whether loop
            loopwhether = gene.loopwhether,
            looptype = gene.looptype,
            loopstudy = gene.loopstudy,
            loopsubunit = gene.loopsubunit,

            #whether DEG
            degwhether = gene.degwhether,
            degnumberstudy = gene.degnumberstudy,
            degstudy = gene.degstudy,
            degsubunit = gene.degsubunit,

            #whether co-express
            correlationwhether = gene.correlationwhether,
            correlationRho = gene.correlationRho,
            correlationFDR = gene.correlationFDR,
            correlationsubunit = gene.correlationsubunit,
        )

        onegenedata.save()

class Command(BaseCommand):
    help = 'Import example data for Browse 1st page'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('begin import'))
        import_example_object()
        self.stdout.write(self.style.SUCCESS('end import'))
