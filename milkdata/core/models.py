from django.db import models


class Shed(models.Model):
    name = models.CharField(max_length=255)


class ShedData(models.Model):
    shed = models.ForeignKey(Shed, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.FloatField()


class Pocket(models.Model):
    date = models.DateField()
    half_litre = models.IntegerField(null=True, blank=True)
    quarter_litre = models.IntegerField(null=True, blank=True)


class Shop(models.Model):
    name = models.CharField(max_length=200)

    class CategoryChoices(models.IntegerChoices):
        SHOP = 1
        LINE = 2

    category = models.IntegerField(
        choices=CategoryChoices.choices, default=CategoryChoices.LINE
    )


class ShopData(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    date = models.DateField()
    half_litre = models.IntegerField(null=True, blank=True)
    quarter_litre = models.IntegerField(null=True, blank=True)
    additional = models.IntegerField(null=True, blank=True)
    note = models.CharField(max_length=100, null=True, blank=True)
