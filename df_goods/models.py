from django.db import models
from tinymce.models import HTMLField

# Create your models here.


class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return self.ttitle




class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='goods')
    gprice = models.DecimalField(max_digits=5,decimal_places=2)
    isDelete = models.BooleanField(default=False)
    gunit = models.CharField(max_length=20, default='500g')
    gclick = models.IntegerField()
    gdescription = models.CharField(max_length=300)
    ginventory = models.IntegerField()
    gcontent= HTMLField()
    gtype = models.ForeignKey(TypeInfo,default='')

    def __str__(self):
        return self.gtitle
