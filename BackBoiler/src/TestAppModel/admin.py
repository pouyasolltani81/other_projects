from django.contrib import admin
from .models import TestModel

class TestModelAdmin(admin.ModelAdmin):
    list_display=('id', 'test_number',)

    fieldsets = (
        ('Trader', {'fields': ('test_number',)}),
       
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('test_number',)}
         ),
    )
    search_fields = ('test_number',)
    ordering = ('test_number',)

admin.site.register(TestModel, TestModelAdmin)
