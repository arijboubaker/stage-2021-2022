# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from apps.home.views import AddPicture, ListPicture

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('', views.button),
    path('new_picture/', views.new_picture, name='new_picture'),

    path('external/', views.external),
    path('external_pdf/', views.external_pdf),
    path('AddPicture',views.AddPicture,name='AddPicture'),
    path('delete_picture/<int:id>', views.delete_picture, name = 'delete_picture'),
    path('pictures', views.ListPicture, name='ListPicture'),
    path('update_picture/<int:id>', views.update_picture, name='update_picture'),
    path('view_picture/<int:id>', views.view_picture, name='view_picture'),
    path('check_picture/<int:id>', views.check_picture, name='check_picture'),

    path('AddFin', views.AddFin, name='AddFin'),
    path('delete_Fin/<int:id>', views.delete_Fin, name='delete_Fin'),
    path('Fins', views.ListFin, name='ListFin'),
    path('update_Fin/<int:id>', views.update_Fin, name='update_Fin'),
    path('view_Fin/<int:id>', views.view_Fin, name='view_Fin'),
    path('check_Fin/<int:id>', views.check_Fin, name='check_Fin'),

    path('deps', views.ListDep, name='ListDep'),
    path('new_department/', views.new_department, name='new_department'),
    path('department/', views.department),
    path('AddDep', views.AddDep, name='AddDep'),
    path('new_department_pdf/', views.new_department_pdf),
    path('view_Dep/<int:id>', views.view_Dep, name='view_Dep'),
    path('update_Dep/<int:id>', views.update_Dep, name='update_Dep'),
    path('delete_Dep/<int:id>', views.delete_Dep, name='delete_Dep'),
    path(r'^export/csv/$', views.export_users_csv, name='export_users_csv'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
