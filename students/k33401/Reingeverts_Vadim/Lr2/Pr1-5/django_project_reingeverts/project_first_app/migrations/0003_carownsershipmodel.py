# Generated by Django 4.1.5 on 2023-01-14 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_first_app', '0002_remove_ownership_start_end_date_correct_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarOwnsershipModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
