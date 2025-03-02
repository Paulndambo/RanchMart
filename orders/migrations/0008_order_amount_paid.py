# Generated by Django 5.1 on 2025-03-02 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=100),
        ),
    ]
