# Generated by Django 5.0.3 on 2024-03-26 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_orderitem_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='customer',
        ),
    ]
