# Generated by Django 4.0.3 on 2022-04-06 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]