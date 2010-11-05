from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db.models.loading import get_models
from django.db.models import signals

from enummodel.models import EnumModel


def bootstrap_choice_model( sender, **kwargs ):
    app = kwargs.pop('app',None)
    created_models = kwargs.pop('created_models',[])
    verbosity = kwargs.pop('verbosity',0)
    interactive = kwargs.pop('interactive',False)

    app_models = get_models( app )
    for model_cls in app_models:
        if not issubclass(model_cls, EnumModel) or model_cls._meta.abstract:
            continue

        value_field = model_cls._enum_meta.value_field
        choices = model_cls._enum_meta.choices
        if not choices:
            raise ImproperlyConfigured( \
                u"Please specify the Meta class option 'choices' on %s" % \
                    (model_cls._meta.verbose_name))

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
