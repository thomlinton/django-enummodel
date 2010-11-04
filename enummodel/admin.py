from django.contrib import admin


class EnumModelAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
