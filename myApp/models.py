from django.db import models

# Create your models here.
class Pic(models.Model):
    picName = models.CharField(max_length=50)

