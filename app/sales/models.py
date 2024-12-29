from django.db import models

class Goods_daily_stat(models.Model):
    good_code = models.IntegerField()
    uuid = models.CharField(max_length=36)
    title = models.CharField(max_length=150)
    leftover = models.IntegerField()
    sold = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.title
