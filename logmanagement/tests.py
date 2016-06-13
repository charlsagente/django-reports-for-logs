from django.test import TestCase
from parser.LogsParser import LogsParser
from parser.Statistics import Statistics
from models import DateFile


class TestPath(TestCase):

    def test_get_paths(self):
       pk=DateFile.objects.create(fecha_archivo="2015-02-11_archivo1.log", fecha="2015-02-11",archivo="pt-midd.log")
       pk.save()
       pk=DateFile.objects.create(fecha_archivo="2015-02-11_archivo2.log", fecha="2015-02-11",archivo="pt-midd.log")
       pk.save()
       pk=DateFile.objects.create(fecha_archivo="2015-02-11_archivo3.log", fecha="2015-02-11",archivo="pt-midd.log")
       pk.save()
       print DateFile.objects.values_list('fecha_archivo',flat=True)
       print DateFile.objects.all()
