# Generated by Django 2.1.4 on 2025-12-29 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_app', '0003_auto_20181229_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Email'),
        ),
    ]

# Updated: February 2025
