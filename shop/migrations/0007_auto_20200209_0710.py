# Generated by Django 3.0.2 on 2020-02-09 07:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200105_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='contact',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 9, 7, 10, 27, 122391, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='dateTime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 9, 7, 10, 27, 122812, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
