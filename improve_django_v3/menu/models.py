from django.conf import settings
from django.db import models
from django.utils import timezone


class Menu(models.Model):
    season = models.CharField(max_length=20)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateTimeField(
            default=timezone.now)
    expiration_date = models.DateTimeField(
            blank=True, null=True)

    class Meta:
        ordering = ['expiration_date',]

    def __str__(self):
        return self.season


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    chef = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(
            default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField(
        'Ingredient', related_name='ingredients'
        )

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
