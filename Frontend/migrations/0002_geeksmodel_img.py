# Generated by Django 4.0.3 on 2022-03-16 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Frontend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='geeksmodel',
            name='img',
            field=models.ImageField(default=' ', upload_to='images/'),
        ),
    ]
