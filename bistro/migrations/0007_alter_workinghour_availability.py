# Generated by Django 5.1.5 on 2025-02-21 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bistro', '0006_workinghour_availability'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workinghour',
            name='availability',
            field=models.IntegerField(choices=[(0, 'Yes'), (1, 'No')], default=0),
        ),
    ]
