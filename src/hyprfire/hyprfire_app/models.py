from django.db import models

# Create your models here.


class Data(models.Model):

    filename = models.TextField(primary_key=True)
    algorithm = models.TextField()
    window_size = models.IntegerField()
    data = models.TextField()
