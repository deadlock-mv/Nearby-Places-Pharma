# Generated by Django 4.2.1 on 2023-05-15 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base1', '0002_alter_storecompetition_competition_store_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storecompetition',
            name='competition_store_uid',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
