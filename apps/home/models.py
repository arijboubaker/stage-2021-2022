# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Picture(models.Model):
    first_name = models.CharField(max_length=200,null=True, blank=True)
    last_name = models.CharField(max_length=200,null=True, blank=True)
    birthday = models.CharField(max_length=200,null=True, blank=True)
    email = models.CharField(max_length=200,null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    phone = models.CharField(max_length=200,null=True, blank=True)
    comment = models.CharField(max_length=200,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Finance(models.Model):
    nature = models.CharField(max_length=200,null=True, blank=True)
    total = models.CharField(max_length=200,null=True, blank=True)
    name = models.CharField(max_length=200,null=True, blank=True)
    email = models.CharField(max_length=200,null=True, blank=True)
    address = models.CharField(max_length=200,null=True, blank=True)
    phone = models.CharField(max_length=200,null=True, blank=True)
    comment = models.CharField(max_length=200,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Department(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)