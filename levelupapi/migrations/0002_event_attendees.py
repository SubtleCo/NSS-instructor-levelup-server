# Generated by Django 4.0.4 on 2022-06-22 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(related_name='attending', to='levelupapi.gamer'),
        ),
    ]
