from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Institution(models.Model):
    TYPE_CHOICES = (
        ('fundacja', 'Fundacja'),
        ('organizacja', 'Organizacja pozarządowa'),
        ('zbiórka', 'Zbiórka lokalna'),
    )

    name = models.CharField(max_length=128)
    description = models.TextField()
    type = models.CharField(choices=TYPE_CHOICES, default='fundacja')
    categories = models.ManyToManyField('Category')

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField('Category')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # czy lepiej taki zapis jak poniżej (taki był w dokumentacji)
    # user = models.ForeignKey(User, models.SET_NULL, blank=True,null=True)


    def __str__(self):
        return f"Donation {self.id}"
