from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views, downloadview, statistic_view, OtherView, loopview, browse_each_view, view_analyze
from django.contrib.staticfiles.views import serve

app_name = 'demoSite'

urlpatterns =[
    path('',views.homepage, name='homepage'),
    path('data/',views.datapage, name='datapage'),
    path('error/',OtherView.errorpage, name='errorpage'),
    re_path(r'^data/(?P<modules>[\w-]+)\+(?P<experiment>[\w-]+)\+(?P<subunit>[\w-]+)\+(?P<disease>[\w-]+)\+(?P<tissue>[\w-]+)\+(?P<biosample>[\w-]+)/',views.datapagefilter, name='datapage_filter'),
    path('data/download1/<int:dataid>/',downloadview.datadownload1, name='datadownload1'),
    path('data/download2/<int:dataid>/',downloadview.datadownload2, name='datadownload2'),
    re_path(r'data/eachdata/(?P<cdbid>CDBD[0-9]+)/$',browse_each_view.browse_eachdata, name='browse_eachdata'),
    path(r'data/celltype/<str:cellname>/',browse_each_view.browse_eachcell, name='browse_eachcell'),
    path('browse/',views.browsepage, name='browsepage'),
    path('browseloop/',loopview.browselooppage, name='browselooppage'),
    path('browsegene/',views.browsegenepage, name='browsegenepage'),
    re_path(r'browsegene/eachgene/(?P<cdbid>CDBG[0-9]+)/$',browse_each_view.browse_eachgene, name='browse_eachgene'),
    re_path(r'browsepeak/eachpeak/(?P<cdbid>CDBP[0-9]+)/$',browse_each_view.browse_eachpeak, name='browse_eachpeak'),
    re_path(r'browseloop/eachloop/(?P<cdbid>CDBL[0-9]+)/$',browse_each_view.browse_eachloop, name='browse_eachloop'),
    re_path(r'.*1b66e47b7faf825689ad.worker.js',(TemplateView.as_view(template_name="js/1b66e47b7faf825689ad.worker.js",content_type='application/javascript',)),name='EEWB1.worker.js'),
    re_path(r'.*zlib_and_gzip.min.js',(TemplateView.as_view(template_name="js/zlib_and_gzip.min.js",content_type='application/javascript',)),name='EEWB2.worker.js'),
    re_path(r'.*e3ad28a0d8aa2bb710c9.worker.js',(TemplateView.as_view(template_name="js/e3ad28a0d8aa2bb710c9.worker.js",content_type='application/javascript',)),name='EEWB3.worker.js'),
    path('analyze/',view_analyze.analyzepage, name='analyzepage'),
    path('visualize/',views.visualizepage, name='visualizepage'),
    re_path(r'visualize/([CDBD0-9\+]*/?)c91952a9b48f32a8f26a.worker.js',
        (TemplateView.as_view(template_name="demoSite/visualizepage/c91952a9b48f32a8f26a.worker.js",content_type='application/javascript',)),
        name='bw-EEWB.worker.js'),
    re_path(r'visualize/([CDBD0-9\+]*/?)e3ad28a0d8aa2bb710c9.worker.js',
        (TemplateView.as_view(template_name="demoSite/visualizepage/e3ad28a0d8aa2bb710c9.worker.js",content_type='application/javascript',)),
        name='chiA-EEWB.worker.js'),
    re_path(r'visualize/([CDBD0-9\+]*/?)js/zlib_and_gzip.min.js',
        (TemplateView.as_view(template_name="demoSite/visualizepage/js/zlib_and_gzip.min.js",content_type='application/javascript',)),
        name='chiA2-EEWB.worker.js'),
    re_path(r'visualize/(?P<dataid>[CDBD0-9\+]+)/$',views.visualizepage_select,name='visualizepage_select'),
    path('search/',views.searchpage, name='searchpage'),
    path('statistic/',statistic_view.statisticpage, name='statisticpage'),
    path('download/',views.downloadpage, name='downloadpage'),
    path('help/',views.helppage, name='helppage'),
    path('pipeline/',OtherView.pipelinepage, name='pipeline'),
    path('downAnalyze1/',downloadview.analyze1, name='downAnalyze1'),
    path('downAnalyze2/',downloadview.analyze2, name='downAnalyze2'),
    path('downAnalyze2_2/',downloadview.analyze2_2, name='downAnalyze2_2'),
    path('downAnalyze3/',downloadview.analyze3, name='downAnalyze3'),
    path('download/downAllObject/<str:filename>/',downloadview.downAllObject, name='downAllObject'),


    #path('static/(?P<path>.*)$',serve)
]
