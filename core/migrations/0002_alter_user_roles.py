# Generated by Django 5.0 on 2023-12-22 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(to='core.role'),
        ),
    ]