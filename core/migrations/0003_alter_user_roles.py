# Generated by Django 5.0 on 2023-12-22 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_user_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(related_name='role', to='core.role'),
        ),
    ]
