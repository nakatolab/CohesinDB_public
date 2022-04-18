from django.contrib import admin
from .models import ProcessedData,UpdateNew, PeakModel, GeneModel, CellType, LoopModel, GTExData


@admin.register(ProcessedData)
class ProcessedDataAdmin(admin.ModelAdmin):
    list_display = ('cdbid','experiment','modules','antibody','access')
    list_filter = ('experiment','modules','subunit')
    search_fields = ('antibody','access','subunit')
    #date_hierarchy = 'created'
    ordering = ('cdbid',)

admin.site.register(UpdateNew)

admin.site.register(PeakModel)

admin.site.register(GeneModel)

admin.site.register(CellType)

admin.site.register(LoopModel)

admin.site.register(GTExData)
