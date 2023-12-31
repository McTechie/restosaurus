# Generated by Django 4.2.3 on 2023-08-05 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("menu_api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(default=1)),
                (
                    "unit_price",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=5),
                ),
                (
                    "price",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=5),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(db_index=True, max_length=100)),
                ("featured", models.BooleanField(db_index=True, default=False)),
                (
                    "price",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=5),
                ),
                ("inventory_count", models.IntegerField()),
                ("description", models.TextField(default="")),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.BooleanField(db_index=True, default=False)),
                (
                    "total_price",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=5),
                ),
                ("date", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "delivery_crew",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="delivery_crew",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField(default=1)),
                (
                    "unit_price",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=5),
                ),
                (
                    "price",
                    models.DecimalField(db_index=True, decimal_places=2, max_digits=5),
                ),
                (
                    "menu_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="menu_api.menuitem",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="menu_api.order"
                    ),
                ),
            ],
            options={
                "unique_together": {("order", "menu_item")},
            },
        ),
        migrations.AlterField(
            model_name="category",
            name="title",
            field=models.CharField(db_index=True, max_length=100),
        ),
        migrations.DeleteModel(
            name="Item",
        ),
        migrations.AddField(
            model_name="menuitem",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="menu_api.category",
            ),
        ),
        migrations.AddField(
            model_name="cart",
            name="menu_item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="menu_api.menuitem"
            ),
        ),
        migrations.AddField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterUniqueTogether(
            name="cart",
            unique_together={("user", "menu_item")},
        ),
    ]
