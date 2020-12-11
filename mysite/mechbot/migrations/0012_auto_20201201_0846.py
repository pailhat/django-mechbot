# Generated by Django 3.1.2 on 2020-12-01 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mechbot', '0011_auto_20201201_0402'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='key_word',
            new_name='has',
        ),
        migrations.RemoveField(
            model_name='alert',
            name='tag',
        ),
        migrations.AddField(
            model_name='alert',
            name='wants',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
