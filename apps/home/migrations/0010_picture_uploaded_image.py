# Generated by Django 3.2.13 on 2022-07-26 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20220726_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='uploaded_image',
            field=models.ImageField(blank=True, upload_to='raw'),
        ),
    ]
