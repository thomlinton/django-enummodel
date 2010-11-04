from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django import forms

from enummodel.tests.models import Language, Acronym, LinkedModel
from enummodel.admin import EnumModelAdmin


admin.site.register(Language,EnumModelAdmin)
admin.site.register(Acronym,EnumModelAdmin)

class LinkedModelAdminForm(forms.ModelForm):
    languages = forms.ModelMultipleChoiceField( \
        queryset=Language.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        help_text=_(u"Please select from the following the languages those in which you are fluent.")
        )

    acronyms = forms.ModelMultipleChoiceField( \
        queryset=Acronym.objects.all(),
        widget=forms.CheckboxSelectMultiple
        )

    class Meta:
        model = LinkedModel

    class Media:
        css = {
            'screen': ('/static/css/admin_extensions.css',)
        }

class LinkedModelAdmin(admin.ModelAdmin):
    list_display = ('id','first_name','last_name',)
    list_display_links = ('id',)
    list_filter = ('languages','acronyms',)

    form = LinkedModelAdminForm
    fieldsets = (
        (_('Personal information'), {
                'fields':('first_name','last_name',)
                }),
        (_('Qualifications'), {
                'fields':('languages','acronyms')
                }),
        )

admin.site.register(LinkedModel,LinkedModelAdmin)
