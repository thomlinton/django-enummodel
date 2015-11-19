from __future__ import unicode_literals
from __future__ import absolute_import

import logging
import six

from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db.models.base import ModelBase
from django.db import models

logger = logging.getLogger(__name__)


class EnumModelOptions(object):
    choices = ()
    value_field = ''

    def __init__(self, opts):
        if opts:       
            for key, value in six.iteritems(opts.__dict__):
                if not key.startswith('__'):
                    setattr(self, key, value)

class EnumModelBase(ModelBase):
    def __new__(cls, name, bases, attrs):
        new_class = super(EnumModelBase,cls).__new__(cls,name,bases,attrs)
        attr_enum_meta = attrs.pop('EnumMeta', None)
        if not attr_enum_meta:
            enum_meta = getattr(new_class,'EnumMeta',None)
        else:
            enum_meta = attr_enum_meta

        new_class.add_to_class('_enum_meta', EnumModelOptions(enum_meta))
        return new_class

@python_2_unicode_compatible
class EnumModel(six.with_metaclass(EnumModelBase, models.Model)):
    """
    An abstract base class designed to provided an the flexibility of
    a ``ChoiceField`` yet within a normalized (record-type) context.

    ``EnumModel`` should typically define one, or perhaps two, fields
    and exposes a convenient means of defining a ``ManyToMany`` relation 
    that's bootstrapped from a choices tuple.

    The choices tuple is selected by specifying the EnumMeta option ``choices``.

    The value-carrying field is selected by specifying the EnumMeta option
    ``value_field``.

    """
    key = models.PositiveIntegerField(_(u'key'), primary_key=True, db_index=True)

    class Meta:
        ordering = ('key',)
        abstract = True

    def __str__(self):
        try:
            if self._enum_meta.value_field:
                return u'%s' % (getattr(self,self._enum_meta.value_field))
            return u'%s' % (dict(self._enum_meta.choices)[self.key])
        except (AttributeError, KeyError):
            return u'%s' % ("<Value could not be mapped>")
