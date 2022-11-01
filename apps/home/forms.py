from tkinter.tix import Select
from django.db import models
from django.forms import ModelForm
from .models import *
from django import forms


class AddPictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['first_name','last_name','email','address','phone','birthday','comment']




class UpdatePictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'birthday', 'comment']

class AddFinForm(ModelForm):
    class Meta:
        model = Finance
        fields = ['nature','total','name','email','address','phone','comment']

class UpdateFinForm(ModelForm):
    class Meta:
        model = Finance
        fields = ['nature','total','name','email','address','phone','comment']

class AddDepForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class UpdateDepForm(ModelForm):
    class Meta:
        model = Department
        fields = ['name']


