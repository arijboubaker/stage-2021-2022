# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import sys , re
from multiprocessing import process
from subprocess import PIPE, run
import csv

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView

from apps.home.forms import AddPictureForm, AddDepForm, UpdatePictureForm, UpdateDepForm, AddFinForm, UpdateFinForm
from apps.home.models import Picture, Department, Finance
from django.core.files.storage import FileSystemStorage

@login_required(login_url="/login/")
def index(request):

    count_pic = Picture.objects.filter(user=request.user).count()
    count_dep = Department.objects.filter(user=request.user).count()
    HR = Department.objects.filter(name__contains="HR").count()
    Acc = Department.objects.filter(name__contains="Accounting").count()
    Mkg = Department.objects.filter(name__contains="Marketing").count()
    bj = Picture.objects.all().order_by('-created_at')[:5]


    context = {'segment': 'index', 'count_pic': count_pic,'count_dep':count_dep,'HR':HR,'Acc':Acc,'Mkg':Mkg,'bj':bj}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def new_picture(request):
    context = {'segment': 'new_picture'}

    html_template = loader.get_template('home/new_picture.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def button(request):
    return render((request) ,'home.html')

@login_required(login_url="/login/")
def external(request):
    inp = request.POST.get('paramImg')
    out = run([sys.executable, 'scanner.py', inp], shell=False, stdout=PIPE)
    outt = run([sys.executable, 'scannpy.py', inp], shell=False, stdout=PIPE)
    print(out)
    print(outt)
    if("HR Department" in re.sub("\[|\]|\'", "", out.stdout.decode('unicode_escape'))):
        return render(request, 'home/image_scanned.html',{'img_scan': re.sub("\[|\]|\'", "", outt.stdout.decode('unicode_escape')).split(",")})

    elif("Finance Department" in re.sub("\[|\]|\'", "", out.stdout.decode('unicode_escape'))):
        return render(request, 'home/fin_scanned.html',{'img_scan': re.sub("\[|\]|\'", "", outt.stdout.decode('unicode_escape')).split(",")})
    else:
        return render(request, 'home/new_picture.html',{'img_scan': re.sub("\[|\]|\'", "", outt.stdout.decode('unicode_escape')).split(",")})



@login_required(login_url="/login/")
def external_pdf(request):
    inp=request.POST.get('InputPDF')
    out = run([sys.executable,'pdfscan.py' ,inp],shell=False,stdout=PIPE)
    outt = run([sys.executable, 'scanpdf.py', inp], shell=False, stdout=PIPE)
    print(out)
    print(outt)
    if ("HR Department" in re.sub("\[|\]|\'", "", out.stdout.decode('unicode_escape'))):
        return render(request, 'home/image_scanned.html',
                      {'img_scan': re.sub("\[|\]|\'", "", outt.stdout.decode('unicode_escape')).split(",")})

    elif ("Finance Department" in re.sub("\[|\]|\'", "", out.stdout.decode('unicode_escape'))):
        return render(request, 'home/fin_scanned.html',
                      {'img_scan': re.sub("\[|\]|\'", "", outt.stdout.decode('unicode_escape')).split(",")})
    else:
        return render(request, 'home/new_picture.html',
                      {'img_scan': re.sub("\[|\]|\'", "", outt.stdout.decode('unicode_escape')).split(",")})


@login_required(login_url="/login/")
def AddPicture(request):
    context = {'segment': 'AddPicture'}
    if request.method == 'POST':
        form = AddPictureForm(request.POST)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.user = request.user
            picture.save()
            return redirect('check_picture',picture.id)
        else:
             return render(request,'home/image_scanned.html',{'form': form,'segment': 'AddPicture'})

    else:
        form = AddPictureForm()
    return render(request,'home/image_scanned.html',{'form': form,'segment': 'AddPicture'})

@login_required(login_url="/login/")
def check_picture(request,id):
    picture = get_object_or_404(Picture, pk=id)
    if request.method == 'GET':
        form = UpdatePictureForm(instance=picture)
        return render(request, 'home/check_picture.html', {'form': form , 'picture':picture})
    if request.method == 'POST':
        form = UpdatePictureForm(request.POST,instance=picture)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ListPicture'))
        else:
            return render(request, 'home/check_picture.html', {'form': form, 'msg_erreur': 'Erreur d ajout'})

@login_required(login_url="/login/")
def delete_picture(request,id):
    picture = get_object_or_404(Picture, pk=id)
    picture.delete()
    return HttpResponseRedirect(reverse('ListPicture'))


@login_required(login_url="/login/")
def update_picture(request,id):
    picture = get_object_or_404(Picture, pk=id)
    if request.method == 'GET':
        form = UpdatePictureForm(instance=picture)
        return render(request, 'home/update_picture.html', {'form': form , 'picture':picture})
    if request.method == 'POST':
        form = UpdatePictureForm(request.POST,instance=picture)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ListPicture'))
        else:
            return render(request, 'home/update_picture.html', {'form': form, 'msg_erreur': 'Erreur d ajout'})



@login_required(login_url="/login/")
def view_picture(request, id):
    # retrieve patient details
    picture = Picture.objects.get(pk=int(id))

    context = {'segment': 'view_picture', 'picture': picture}

    html_template = loader.get_template('home/view_picture.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def ListPicture(request):
    pictures = Picture.objects.all()

    context = {'segment': 'ListPicture', 'pictures':pictures }

    html_template = loader.get_template('home/ListPicture.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def new_department(request):
    context = {'segment': 'new_department'}

    html_template = loader.get_template('home/new_department.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def department(request):
    inp=request.POST.get('paramImg')
    out = run([sys.executable,'perc.py' ,inp],shell=False,stdout=PIPE)
    print(out)
    return render(request,'home/department.html',{'img_scan':re.sub("\[|\]|\?","",out.stdout.decode('unicode_escape'))})


@login_required(login_url="/login/")
def new_department_pdf(request):
    inp=request.POST.get('InputPDF')
    out = run([sys.executable,'percpdf.py' ,inp],shell=False,stdout=PIPE)
    print(out)
    return render(request,'home/pdf_department.html',{'pdf_scan':re.sub("\[|\]|\?","",out.stdout.decode('unicode_escape'))})


@login_required(login_url="/login/")
def AddDep(request):
    context = {'segment': 'AddDep'}
    if request.method == 'POST' :
        form = AddDepForm(request.POST)
        if form.is_valid():
            dep = form.save(commit=False)
            dep.user = request.user
            dep.save()
            return redirect('ListDep')
        else:
             return render(request,'home/department.html',{'form': form,'segment': 'AddDep'})

    else:
        form = AddDepForm()
    return render(request,'home/department.html',{'form': form,'segment': 'AddDep'})



@login_required(login_url="/login/")
def ListDep(request):
    deps = Department.objects.all()

    context = {'segment': 'ListDep', 'deps':deps }

    html_template = loader.get_template('home/ListDep.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def delete_Dep(request,id):
    dep = get_object_or_404(Department, pk=id)
    dep.delete()
    return HttpResponseRedirect(reverse('ListDep'))


@login_required(login_url="/login/")
def update_Dep(request,id):
    dep = get_object_or_404(Department, pk=id)
    if request.method == 'GET':
        form = UpdateDepForm(instance=dep)
        return render(request, 'home/update_dep.html', {'form': form , 'dep':dep})
    if request.method == 'POST':
        form = UpdateDepForm(request.POST,instance=dep)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ListDep'))
        else:
            return render(request, 'home/update_dep.html', {'form': form, 'msg_erreur': 'Erreur d ajout'})



@login_required(login_url="/login/")
def view_Dep(request, id):
    # retrieve patient details
    dep = Department.objects.get(pk=int(id))

    context = {'segment': 'view_Dep', 'dep': dep}

    html_template = loader.get_template('home/view_dep.html')
    return HttpResponse(html_template.render(context, request))






@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="list.csv"'

    writer = csv.writer(response)
    writer.writerow(['first_name', 'last_name', 'email', 'address', 'phone', 'birthday', 'comment'])

    users = Picture.objects.all().values_list('first_name', 'last_name', 'email', 'address', 'phone', 'birthday', 'comment')
    for user in users:
        writer.writerow(user)

    return response




@login_required(login_url="/login/")
def AddFin(request):
    context = {'segment': 'AddFin'}
    if request.method == 'POST':
        form = AddFinForm(request.POST)
        if form.is_valid():
            fin = form.save(commit=False)
            fin.user = request.user
            fin.save()
            return redirect('check_Fin',fin.id)
        else:
             return render(request,'home/image_scanned.html',{'form': form,'segment': 'AddFin'})

    else:
        form = AddFinForm()
    return render(request,'home/fin_scanned.html',{'form': form,'segment': 'AddFin'})

@login_required(login_url="/login/")
def check_Fin(request,id):
    fin = get_object_or_404(Finance, pk=id)
    if request.method == 'GET':
        form = UpdateFinForm(instance=fin)
        return render(request, 'home/check_Fin.html', {'form': form , 'fin':fin})
    if request.method == 'POST':
        form = UpdateFinForm(request.POST,instance=fin)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ListFin'))
        else:
            return render(request, 'home/check_Fin.html', {'form': form, 'msg_erreur': 'Erreur d ajout'})

@login_required(login_url="/login/")
def delete_Fin(request,id):
    fin = get_object_or_404(Finance, pk=id)
    fin.delete()
    return HttpResponseRedirect(reverse('ListFin'))


@login_required(login_url="/login/")
def update_Fin(request,id):
    fin = get_object_or_404(Finance, pk=id)
    if request.method == 'GET':
        form = UpdateFinForm(instance=fin)
        return render(request, 'home/update_Fin.html', {'form': form , 'fin':fin})
    if request.method == 'POST':
        form = UpdateFinForm(request.POST,instance=fin)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ListFin'))
        else:
            return render(request, 'home/update_Fin.html', {'form': form, 'msg_erreur': 'Erreur d ajout'})



@login_required(login_url="/login/")
def view_Fin(request, id):
    # retrieve patient details
    fin = Finance.objects.get(pk=int(id))

    context = {'segment': 'view_Fin', 'fin': fin}

    html_template = loader.get_template('home/view_Fin.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def ListFin(request):
    fins = Finance.objects.all()

    context = {'segment': 'ListFin', 'fins':fins }

    html_template = loader.get_template('home/ListFin.html')
    return HttpResponse(html_template.render(context, request))