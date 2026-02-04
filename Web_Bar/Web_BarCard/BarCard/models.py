from django.db import models

class CardCoctail(models.Model):
    name = models.TextField()
    category = models.TextField()
    type = models.TextField()
    ingredients = models.TextField()
    description = models.TextField()
    glass = models.TextField()
    strength = models.CharField(max_length=8)
    strengthprocent = models.IntegerField()
    image = models.TextField()
    badge = models.TextField()
    temperature = models.TextField()
    ctime = models.TextField()
    history = models.TextField()
    cooking = models.TextField()
