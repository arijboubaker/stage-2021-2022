# Generated by Django 3.2.13 on 2022-07-15 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('birthday', models.DateTimeField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('address', models.CharField(blank=True, default='None', max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('uploaded_image', models.ImageField(blank=True, upload_to='raw')),
                ('comment', models.CharField(default='None', max_length=200)),
            ],
        ),
    ]
