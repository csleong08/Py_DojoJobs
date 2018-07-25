from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from .models import *
import bcrypt

def index(request):
    print('INDEX method')
    return render(request, 'login_app/index.html')

def register(request):
    print('REGISTER method')
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        print('IF REGISTER')
        for key, value in errors.items():
            messages.error(request, value)
        print('IF WORKS!!')
        return redirect('/')
    else: 
        hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print(hashpw)
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashpw
        )
        request.session['first_name'] = request.POST['first_name']
        request.session['user_id'] = User.objects.get(email=request.POST['email']).id
    print('ELSE works!!')
    return redirect('/dash')

def login(request):
    print('LOGIN method')
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        print('FAILED LOGIN')
        for key, value in errors.items():
            messages.error(request, value)
        print('FAILED ELSE WORKS!!')
    else:
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['first_name'] = User.objects.get(email=request.POST['email']).first_name
            request.session['user_id'] = User.objects.get(email=request.POST['email']).id
            print("password match")
            return redirect('/dash')
    return redirect('/')

def logout(request):
    print('LOGOUT method')
    request.session.clear()
    print('LOGOUT works!!!')
    return redirect('/')

def dash(request):
    print('DASH method')
    print(request.session['user_id'])
    me = User.objects.get(id=request.session['user_id'])
    liked_jobs = me.liked_jobs.all()

    context = {
        'all_jobs' : Job.objects.all(),
        'liked_jobs' : liked_jobs,
        'unliked_jobs' : Job.objects.exclude(liked_users = me)
    }
    print('DASH WORKS!')
    return render(request, 'login_app/dash.html', context)

def addJob(request):
    print('ADDJOB HTML')
    context = {
        'all_jobs' : Job.objects.all()
    }
    print('ADDJOB WORKS!!!')
    return render(request, 'login_app/addjob.html', context)

def createJob(request):
    print('CREATEJOB method')
    print(request.session['user_id'])
    errors = Job.objects.job_validator(request.POST)
    if len(errors):
        print('IF CREATEJOB')
        for key, value in errors.items():
            messages.error(request, value)
        print('IF WORKS!!')
        return redirect('/addJob')
    else:
        user = User.objects.get(id=request.session['user_id'])
        job = Job.objects.create(
            desc = request.POST['desc'],
            job_name = request.POST['job_name'],
            location = request.POST['location'],
            creator_id = request.session['user_id'])
        # user.liked_jobs.add(job)
        
        print('CREATEJOB works!!!!')
        return redirect('/dash')

def delete(request):
    print('DELETE method')
    print(request.POST['job_id'])
    Job.objects.get(id=request.POST['job_id']).delete()
    return redirect('/dash')

def add(request, job_id, user_id):
    print('ADD method')
    print(request.session['user_id'])
    user = User.objects.get(id=user_id)
    job = Job.objects.get(id=job_id)
    user.liked_jobs.add(job)
    print('ADD WORKS!!!!')
    return redirect('/dash')

def view(request, job_id):
    print('VIEW method')
    context = {
        'job' : Job.objects.get(id=job_id).__dict__,
        'user' : Job.objects.get(id=job_id).creator.__dict__,
        # 'other_user' : User.objects.filter(liked_trips=id)
    }
    return render(request, 'login_app/view.html', context)

def edit(request, job_id):
    print('EDIT method')
    print(job_id)
    context = {
        'job' : Job.objects.get(id=job_id)
        # 'user' : User.objects.get(id=user_id)
    }
    return render(request, 'login_app/edit.html', context)

def update(request, job_id):
    print('update method')
    errors = Job.objects.job_validator(request.POST)
    print(job_id)
    if len(errors):
        print("IF_UPDATE")
        for key, value in errors.items():
            messages.error(request, value)
        print("IF UPDATE WORKS!")
        # jid = '/update/'+str(job_id)
        return redirect('/edit/'+str(job_id))
        # or return redirect('/update/'+str(user_id)+'/edit')
    else:

        print("ELSE_UPDATE")
        job = Job.objects.get(id=job_id)
        job.job_name = request.POST['job_name']
        job.desc = request.POST['desc']
        job.location = request.POST['location']
        job.save()

        return redirect('/dash')


