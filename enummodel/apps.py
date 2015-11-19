from __future__ import unicode_literals
from __future__ import absolute_import

import logging

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db.models.signals import post_migrate
from django.apps import AppConfig as BaseAppConfig

logger = logging.getLogger(__name__)


class AppConfig(BaseAppConfig):
    """
    """
    name = 'enummodel'

    def sync_enumerations(self, model_cls, choices):
        """
        Ensures all defined enumeration values exist.
        """
        value_field = model_cls._enum_meta.value_field
        for choice in choices:
            try:
                model_cls.objects.get(key=int(choice[0]))
            except ObjectDoesNotExist:
                model_cls.objects.create(key=int(choice[0]))

                if value_field:
                    update_kwargs = {value_field:"%s"%choice[1]}
                    model_cls.objects \
                        .filter(key=int(choice[0])) \
                        .update(**update_kwargs)

    def prune_enumerations(self, model_cls, choice_mapping):
        """
        Prunes enumeration values that no longer exist.
        """
        for instance in model_cls.objects.all():
            if instance.key not in choice_mapping.keys():
                response = raw_input("""
The model '%s' is managed by 'django-enummodel' and a key ('%s') is present in the datastore
but not the enumeration.

Pruning unused keys is recommended; however, depending on the data model, this action may
cascade on distinct objects, having frustrating and/or undesireable consequences.

Prune this key? [y/N] """ % (model_cls._meta.verbose_name, instance.key))
                if response not in ['y','Y']:
                    continue
                instance.delete()

    def bootstrap_models(self, sender, **kwargs):
        # EnumModel = self.get_model('enummodel.EnumModel')
        from .models import EnumModel

        for model_cls in sender.get_models():
            if not issubclass(model_cls, EnumModel) or model_cls._meta.abstract:
                continue

            choices = model_cls._enum_meta.choices
            if not choices:
                raise ImproperlyConfigured( \
                    "Please specify the Meta class option 'choices' on %s" % \
                        (model_cls._meta.verbose_name))

            choice_mapping = dict(choices)
            if kwargs.pop('interactive', False):
                self.prune_enumerations(model_cls, choice_mapping)
            self.sync_enumerations(model_cls, choices)

    def ready(self):
        post_migrate.connect(self.bootstrap_models)
