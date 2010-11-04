from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from enummodel.tests.models import Language, Acronym


class NaiveTest(TestCase):
    def testLanguageTestModel(self):
        self.assertEquals( Language.objects.count(), 4 )
    
    def testAcronymTestModel(self):
        self.assertEquals( Acronym.objects.count(), 3 )

    def testLinkedModelTestModel(self):
        pass

__tests__ = {}
