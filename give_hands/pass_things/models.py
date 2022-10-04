from django.db import models
from django.conf import settings


TYPE = (
    (1, "fundacja"),
    (2, "organizacja pozarządowa"),
    (3, "zbiórka lokalna"),
)

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)


class Institution(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    type = models.IntegerField(default=1, choices=TYPE)
    category = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.IntegerField()
    category = models.ManyToManyField(Category)
    institution = models.ForeignKey()
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateTimeField()
    pick_up_time = models.DateTimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
