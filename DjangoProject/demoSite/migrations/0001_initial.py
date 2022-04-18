# Generated by Django 3.0.14 on 2022-01-24 09:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CellType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdbid', models.SlugField(default='CDBCELL00001')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('dataname', models.CharField(max_length=100)),
                ('cellname', models.CharField(max_length=100)),
                ('tissue', models.CharField(max_length=100)),
                ('biosample', models.CharField(max_length=50)),
                ('disease', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('link', models.TextField()),
            ],
            options={
                'ordering': ('cellname',),
            },
        ),
        migrations.CreateModel(
            name='ExampleGeneModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdbid', models.SlugField(default='CDBG00000001')),
                ('geneID', models.CharField(default=None, max_length=50)),
                ('genesymbol', models.CharField(default=None, max_length=50)),
                ('geneposition', models.CharField(default=None, max_length=50)),
                ('chromosome', models.CharField(default=None, max_length=50)),
                ('start', models.IntegerField(default=None)),
                ('end', models.IntegerField(default=None)),
                ('strand', models.CharField(default=None, max_length=5)),
                ('proteincoding', models.CharField(default=None, max_length=50)),
                ('triplewheter', models.BooleanField(default=None)),
                ('triplecohesin', models.TextField(default=None)),
                ('relatedtype', models.CharField(default=None, max_length=50)),
                ('loopwhether', models.BooleanField(default=None)),
                ('looptype', models.CharField(default=None, max_length=50)),
                ('loopstudy', models.TextField(default=None)),
                ('loopsubunit', models.CharField(default=None, max_length=50)),
                ('degwhether', models.BooleanField(default=None)),
                ('degnumberstudy', models.IntegerField(default=None)),
                ('degstudy', models.TextField(default=None)),
                ('degsubunit', models.CharField(default=None, max_length=50)),
                ('correlationwhether', models.BooleanField(default=None)),
                ('correlationRho', models.FloatField(default=None)),
                ('correlationFDR', models.FloatField(default=None)),
                ('correlationsubunit', models.TextField(default=None)),
            ],
            options={
                'ordering': ('geneposition',),
            },
        ),
        migrations.CreateModel(
            name='ExampleLoopModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdbid', models.SlugField(default='CDBL00000002')),
                ('chrom1', models.CharField(max_length=50)),
                ('start1', models.IntegerField()),
                ('end1', models.IntegerField()),
                ('chrom2', models.CharField(max_length=50)),
                ('start2', models.IntegerField()),
                ('end2', models.IntegerField()),
                ('assay', models.CharField(max_length=100)),
                ('subunit', models.CharField(max_length=100)),
                ('celltype', models.CharField(max_length=1000)),
                ('study', models.TextField()),
                ('looplength', models.IntegerField()),
                ('loopwidth', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ExamplePeakModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdbid', models.SlugField(default='CDBP00000001')),
                ('chromosome', models.CharField(default=None, max_length=50)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('slug', models.SlugField(max_length=100)),
                ('datasource', models.TextField()),
                ('celltype', models.TextField()),
                ('cellspecificity', models.FloatField()),
                ('subunit', models.CharField(max_length=1000)),
                ('CTCFdependent', models.CharField(max_length=20)),
                ('location', models.CharField(default=None, max_length=20)),
                ('boundary', models.CharField(max_length=20)),
                ('hubs', models.CharField(max_length=20)),
                ('hicloop', models.CharField(default=None, max_length=20)),
                ('hicchiploop', models.CharField(default=None, max_length=20)),
                ('chialoop', models.CharField(default=None, max_length=20)),
                ('enhancer', models.CharField(max_length=20)),
                ('cobind', models.TextField()),
                ('targetgene', models.TextField()),
                ('targetgeneID', models.TextField()),
                ('snp', models.TextField()),
                ('codingmut', models.IntegerField(default=None)),
                ('noncodingmut', models.IntegerField(default=None)),
            ],
            options={
                'ordering': ('chromosome', 'start'),
            },
        ),
        migrations.CreateModel(
            name='GeneModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdbid', models.SlugField(default='CDBG00000001')),
                ('geneID', models.CharField(max_length=50)),
                ('genesymbol', models.CharField(max_length=50)),
                ('geneposition', models.CharField(max_length=50)),
                ('chromosome', models.CharField(default=None, max_length=50)),
                ('start', models.IntegerField(default=None)),
                ('end', models.IntegerField(default=None)),
                ('strand', models.CharField(default=None, max_length=5)),
                ('proteincoding', models.CharField(default=None, max_length=50)),
                ('triplewheter', models.BooleanField(default=None)),
                ('triplecohesin', models.TextField(default=None)),
                ('relatedtype', models.CharField(default=None, max_length=50)),
                ('loopwhether', models.BooleanField(default=None)),
                ('looptype', models.CharField(default=None, max_length=50)),
                ('loopstudy', models.TextField(default=None)),
                ('loopsubunit', models.CharField(default=None, max_length=50)),
                ('degwhether', models.BooleanField(default=None)),
                ('degnumberstudy', models.IntegerField(default=None)),
                ('degstudy', models.TextField(default=None)),
                ('degsubunit', models.CharField(default=None, max_length=50)),
                ('correlationwhether', models.BooleanField(default=None)),
                ('correlationRho', models.FloatField(default=None)),
                ('correlationFDR', models.FloatField(default=None)),
                ('correlationsubunit', models.TextField(default=None)),
            ],
            options={
                'ordering': ('geneposition',),
            },
        ),
        migrations.CreateModel(
            name='LoopModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdbid', models.SlugField(default='CDBL00000001')),
                ('chrom1', models.CharField(max_length=50)),
                ('start1', models.IntegerField()),
                ('end1', models.IntegerField()),
                ('chrom2', models.CharField(max_length=50)),
                ('start2', models.IntegerField()),
                ('end2', models.IntegerField()),
                ('assay', models.CharField(default=None, max_length=100)),
                ('subunit', models.CharField(max_length=100)),
                ('celltype', models.CharField(max_length=1000)),
                ('study', models.TextField()),
                ('looplength', models.IntegerField()),
                ('loopwidth', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PeakModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cdbid', models.SlugField(default='CDBP00000001')),
                ('chromosome', models.CharField(default=None, max_length=50)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('slug', models.SlugField(max_length=100)),
                ('datasource', models.TextField()),
                ('celltype', models.TextField()),
                ('cellspecificity', models.FloatField()),
                ('subunit', models.CharField(max_length=1000)),
                ('CTCFdependent', models.CharField(max_length=20)),
                ('location', models.CharField(default=None, max_length=20)),
                ('boundary', models.CharField(max_length=20)),
                ('hubs', models.CharField(max_length=20)),
                ('hicloop', models.CharField(default=None, max_length=20)),
                ('hicchiploop', models.CharField(default=None, max_length=20)),
                ('chialoop', models.CharField(default=None, max_length=20)),
                ('enhancer', models.CharField(max_length=20)),
                ('cobind', models.TextField()),
                ('targetgene', models.TextField()),
                ('targetgeneID', models.TextField()),
                ('snp', models.TextField()),
                ('codingmut', models.IntegerField(default=None)),
                ('noncodingmut', models.IntegerField(default=None)),
            ],
            options={
                'ordering': ('chromosome', 'start'),
            },
        ),
        migrations.CreateModel(
            name='ProcessedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cdbid', models.SlugField(default='CDBD00001')),
                ('experiment', models.CharField(choices=[('ChIPseq', 'ChIP-seq'), ('ChIAPET', 'ChIA-PET'), ('HiChIP', 'Hi-ChIP'), ('HiC', 'Hi-C'), ('RNAseq', 'RNA-seq'), ('Microarray', 'Microarray'), ('PROseq', 'PRO-seq'), ('GROseq', 'GRO-seq')], default='ChIPseq', max_length=10)),
                ('modules', models.CharField(choices=[('Cohesin-Binding', 'Cohesin-Binding'), ('Cohesin-3Dgenome', 'Cohesin-3Dgenome'), ('Cohesin-DEGs', 'Cohesin-DEGs')], default='cohesin-binding', max_length=20)),
                ('antibody', models.CharField(max_length=50, null=True)),
                ('subunit', models.CharField(max_length=50, null=True)),
                ('compareID', models.CharField(max_length=50, null=True)),
                ('restriction', models.CharField(max_length=50, null=True)),
                ('cell', models.CharField(max_length=100)),
                ('tissue', models.CharField(default='Breast', max_length=100)),
                ('biosample', models.CharField(default='Cell line', max_length=100)),
                ('disease', models.CharField(default='Normal', max_length=20)),
                ('access', models.CharField(max_length=100)),
                ('data_date', models.DateField()),
                ('treat1', models.CharField(default='NT', max_length=100)),
                ('treat2', models.CharField(default='NT', max_length=100)),
                ('status', models.CharField(choices=[('highQC', 'HighQC'), ('lowQC', 'LowQC'), ('test', 'ForTest')], default='highQC', max_length=10)),
                ('content1', models.FileField(max_length=200, upload_to='')),
                ('content2', models.FileField(max_length=200, null=True, upload_to='')),
                ('content3', models.FileField(max_length=200, null=True, upload_to='')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='UpdateNew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('publishtime', models.DateTimeField(default=datetime.datetime.now)),
                ('content', models.TextField(max_length=200)),
            ],
            options={
                'ordering': ('-publishtime',),
            },
        ),
    ]
