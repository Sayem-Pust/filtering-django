# Generated by Django 3.1.7 on 2021-03-25 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210325_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='publish_date',
            field=models.DateTimeField(),
        ),
    ]
