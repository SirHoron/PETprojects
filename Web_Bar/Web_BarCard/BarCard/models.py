from django.db import models

class For_Card_Coctail(models.Model):
    name = models.TextField()
    category = models.TextField()
    type = models.TextField()
    ingredients = models.TextField()
    description = models.TextField()
    glass = models.TextField()
    strength = models.TextField()
    strengthprocent = models.IntegerField()
    image = models.TextField()
    temperature = models.TextField()
    ctime = models.TextField()
    history = models.TextField()
    cooking = models.TextField()
