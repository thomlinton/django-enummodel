from django.utils.translation import ugettext_lazy as _
from django.db import models

from enummodel.models import EnumModel


LANGUAGE_CHOICES = (
    (1,_(u'English')),
    (2,_(u'Spanish')),
    (3,_(u'French')),
    
    (255,_(u'other')),
)

class Language(EnumModel):
    class EnumMeta:
        choices = LANGUAGE_CHOICES


ACRONYM_CHOICES = (
    (1,u'NOAA'),
    (2,u'NASA'),
    (3,u'NAACP'),
)

class Acronym(EnumModel):
    expanded_name = models.CharField( \
        _(u'expanded name'), max_length=64, db_index=True)

    class EnumMeta:
        choices = ACRONYM_CHOICES
        value_field = 'expanded_name'

class LinkedModel(models.Model):
    first_name = models.CharField(_(u'first name'), max_length=64)
    last_name = models.CharField(_(u'last name'), max_length=64)

    languages = models.ManyToManyField(Language)
    acronyms = models.ManyToManyField(Acronym)

    def __unicode__(self):
        return u"%s, %s" % (self.last_name,self.first_name)
