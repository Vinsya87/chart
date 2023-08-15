from django.contrib import admin
from .models import DataPoint

class DataPointAdmin(admin.ModelAdmin):
    list_display = ('formatted_date', 'number')
    list_display_links = ('formatted_date', 'number')
    list_filter = ('number',)
    search_fields = ('number',)

    def formatted_date(self, obj):
        return obj.date.strftime('%Y-%m-%d %H:%M:%S')
    formatted_date.short_description = 'Date'

admin.site.register(DataPoint, DataPointAdmin)
