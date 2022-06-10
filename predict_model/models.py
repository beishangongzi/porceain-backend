import django.utils.timezone
from django.db import models
import django

# Create your models here.
from user.models import User




class Dynasty(models.Model):
    dynasty = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.dynasty


class EmperorYear(models.Model):
    dynasty = models.ForeignKey(to=Dynasty, on_delete=models.CASCADE, to_field="dynasty")
    year = models.CharField(max_length=5)

    def __str__(self):
        return self.dynasty.dynasty + "_" + self.year


def upload_porcelain_image(instance, filename):
    name = instance.name + "." + filename.split(".")[-1]
    return "procelain/" + name

class Porcelain(models.Model):
    name = models.CharField(max_length=10, null=False, unique=True)
    year = models.ForeignKey(to=EmperorYear, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_porcelain_image)
    introduce = models.TextField()
    uploader = models.ForeignKey(to=User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=django.utils.timezone.now)
