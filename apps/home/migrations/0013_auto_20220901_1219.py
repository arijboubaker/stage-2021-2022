# Generated by Django 3.2.13 on 2022-09-01 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0012_alter_picture_uploaded_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='uploaded_image',
        ),
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nature', models.CharField(blank=True, max_length=200, null=True)),
                ('total', models.CharField(blank=True, max_length=200, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('comment', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]