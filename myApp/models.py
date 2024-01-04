from django.db import models

# Create your models here.
# class Pic(models.Model):
#     picName = models.CharField(max_length=50)

class Image(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return

