from django.db import models

# Create your models here.
class MeituanInfo(models.Model):
    name = models.TextField()
    region = models.CharField(max_length=50)
    price = models.FloatField()
    originalPrice = models.FloatField()
    discount = models.FloatField()
    saveMoney = models.FloatField()
    soldNumber = models.IntegerField()
    sevenOrNot = models.IntegerField()
    expireOrNot = models.IntegerField()
    validStartTime = models.CharField(max_length=50)
    validEndTime = models.CharField(max_length=50)
    tips = models.TextField()
    greatness = models.TextField()
    mainImage = models.CharField(max_length=50)

