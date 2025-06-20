# Generated by Django 5.2 on 2025-05-11 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_delivery'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryOverride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('new_quantity', models.PositiveIntegerField()),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.subscription')),
            ],
            options={
                'unique_together': {('subscription', 'date')},
            },
        ),
    ]
