from django.db import models

# Create your models here.

class Goods(models.Model):
    good_code = models.IntegerField()
    uuid = models.CharField(max_length=36)
    title = models.CharField(max_length=150)
    price = models.FloatField()

    def __str__(self):
        return self.title
