# Generated by Django 3.1.2 on 2020-12-01 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mechbot', '0010_auto_20201130_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='key_word',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='origin',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]