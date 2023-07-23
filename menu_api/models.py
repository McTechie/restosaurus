from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.title

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    inventory_count = models.IntegerField()
    description = models.TextField(default="")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.title
