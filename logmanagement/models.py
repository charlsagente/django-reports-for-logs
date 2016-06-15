from __future__ import unicode_literals

from django.db import models

# Create your models here.
class DateFile(models.Model):
    fecha_archivo= models.CharField(max_length=70,primary_key=True)
    fecha=models.DateField(null=True)
    archivo=models.CharField(max_length=50,null=True)



