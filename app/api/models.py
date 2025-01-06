from django.db import models

# Create your models here.

class Goods(models.Model):
    good_code = models.IntegerField()
    uuid = models.CharField(primary_key=True, max_length=36)
    title_ua = models.CharField(max_length=255)
    description_ua = models.CharField(max_length=255)

    def __str__(self):
        return self.title_ua

    class Meta:
        db_table = "Goods"


class Categories(models.Model):
    uuid = models.CharField(primary_key=True, max_length=36)
    name_ua = models.CharField(max_length=255)

    def __str__(self):
        return self.name_ua

    class Meta:
        db_table = "Categories"
