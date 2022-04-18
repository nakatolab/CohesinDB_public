# Generated by Django 3.0.14 on 2022-04-14 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demoSite', '0010_processeddata_content3'),
    ]

    operations = [
        migrations.AddField(
            model_name='peakmodel',
            name='CTCFmotif',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AddField(
            model_name='peakmodel',
            name='HMMtop1name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='peakmodel',
            name='HMMtop1percent',
            field=models.DecimalField(decimal_places=6, default=None, max_digits=10),
        ),
        migrations.AddField(
            model_name='peakmodel',
            name='HMMtop2name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AddField(
            model_name='peakmodel',
            name='HMMtop2percent',
            field=models.DecimalField(decimal_places=6, default=None, max_digits=10),
        ),
        migrations.AddField(
            model_name='peakmodel',
            name='compartmentA',
            field=models.DecimalField(decimal_places=6, default=None, max_digits=10),
        ),
        migrations.AddField(
            model_name='peakmodel',
            name='superenhancer',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
