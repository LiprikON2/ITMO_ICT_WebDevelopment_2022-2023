# Generated by Django 4.1.5 on 2023-03-10 17:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_readingroombookuser_borrow_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readingroombookuser',
            name='borrow_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 10, 20, 42, 16, 21928)),
        ),
    ]
