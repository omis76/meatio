# Generated by Django 5.2 on 2025-05-11 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='order_type',
            field=models.CharField(choices=[('one_time', 'One Time'), ('subscription', 'Subscription')], default='subscription', max_length=20),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='days_of_week',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
