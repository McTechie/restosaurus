from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    featured = models.BooleanField(default=False, db_index=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    inventory_count = models.IntegerField()
    description = models.TextField(default="")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    
    class Meta:
        unique_together = ('user', 'menu_item')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivery_crew', null=True)
    status = models.BooleanField(default=False, db_index=True)
    total_price = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    date = models.DateTimeField(auto_now_add=True, db_index=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)

    class Meta:
        unique_together = ('order', 'menu_item')
