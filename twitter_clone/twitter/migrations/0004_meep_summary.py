# Generated by Django 4.2.2 on 2023-06-29 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_meep'),
    ]

    operations = [
        migrations.AddField(
            model_name='meep',
            name='summary',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
