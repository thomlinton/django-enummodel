from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db.models.loading import get_models, get_app
from django.db.models import signals

from enummodel.models import EnumModel


def bootstrap_choice_model( sender, **kwargs ):
    app = kwargs.pop('app',None)
    created_models = kwargs.pop('created_models',[])
    verbosity = kwargs.pop('verbosity',0)
    interactive = kwargs.pop('interactive',False)

    # XXX: South compatibility
    if type(app) == str:
        app = get_app(app)

    app_models = get_models(app)
    for model_cls in app_models:
        if not issubclass(model_cls, EnumModel) or model_cls._meta.abstract:
            continue

        value_field = model_cls._enum_meta.value_field
        choices = model_cls._enum_meta.choices
        if not choices:
            raise ImproperlyConfigured( \
                u"Please specify the Meta class option 'choices' on %s" % \
                    (model_cls._meta.verbose_name))

        # XXX: Prune enumeration values that no longer exist
        choice_mapping = dict(choices)
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

        for choice in choices:
            try:
                model_cls.objects.get(key=int(choice[0]))
            except ObjectDoesNotExist:
                model_cls.objects.create(key=int(choice[0]))

            if value_field:
                update_kwargs = {value_field:u"%s"%choice[1]}
                model_cls.objects \
                    .filter(key=int(choice[0])) \
                    .update(**update_kwargs)

signals.post_syncdb.connect(bootstrap_choice_model)

# XXX: South compatibility
try:
    from south import signals
    signals.post_migrate.connect(bootstrap_choice_model)
except ImportError:
    pass
