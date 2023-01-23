# Generated by Django 4.1.5 on 2023-01-23 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_review_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='reviews',
        ),
        migrations.AddField(
            model_name='review',
            name='flight_pk',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.flight'),
            preserve_default=False,
        ),
    ]