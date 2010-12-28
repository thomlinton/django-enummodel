================
django-enummodel
================

``django-enummodel`` is a small utility application designed to help bridge the niche use 
case(s?) between defining enumerations for a given field (mutually exclusive options) and 
fully specifying non-exclusive options as instances of a fully specified model type.

In the common case, non-mututally exclusive options configured as a fully specified model
(along with a fixture to store those options) can, in the best case, 'just work'; in the 
worst case, it can provide mild headaches, notably when lazy translations are involved.

In the particular case of the author, the challenge was to avoid having to cope with a 
O(n) growth rate of fixtures to manage, coupled with the desire to avoid encountering 
issues of internationalization and being forced to choose a particular character set 
in which to store these values.

``django-enummodel`` provides a `Django`_ Model object with which the developer may extend 
to provide the functionality sketched above::

  LANGUAGE_CHOICES = (
      (1,_(u'English')),
      (2,_(u'Spanish')),
      (3,_(u'French')),
    
      (255,_(u'other')),
  )

  class Language(EnumModel):
      class EnumMeta:
          choices = LANGUAGE_CHOICES

Please note that that population of any model derived from ``EnumModel`` takes place on
``syncdb``; therefore, changes to the choices basis will need to be rectified by running::

  django-admin.py syncdb

.. _Django: http://djangoproject.org


Release notes
-------------

0.1.2
=====

* Discovered incorrect package spec in setup.py

0.1.1
=====

* Fixed issue with incorrectly registering and populating ``EnumModel`` derivatives.

0.1.0
=====

* Initial release
