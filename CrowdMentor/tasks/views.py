import random

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages

from .models import ResearchTasks, TaskUserJunction, Audit

from .forms import AddTaskForm, AnswerForm, AuditForm
from users.profile import Profile

#Controller for View Open tasks
@login_required
def index(request):
    task_list = ResearchTasks.objects.all().exclude(num_workers = 0)
    context = {
        'task_list': task_list,
    }
    return render(request, 'tasks/index.html', context)

#Controller for adding Tasks. If method is post submit form else show the form
@login_required
def add_tasks(request):
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'task_updater':
        messages.info(request, 'Permission Denied!! You do not have permission to access this page')
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator_id = user
            task.save()
            messages.info(request, 'New Task Added')
            return HttpResponseRedirect('/tasks/')
    else:
        form = AddTaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})

#Controller for showing details of task
@login_required
def detail(request, task_id):
    user = User.objects.get(username=request.user.username)
    claim_permission = user.profile.role == 'worker'
    try:
        task = ResearchTasks.objects.get(pk=task_id)
    except ResearchTasks.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'tasks/detail.html', {'task': task, 'claim_permission': claim_permission})

#Controller for adding Claiming Tasks
@login_required
def claim(request, task_id):
    user = User.objects.get(username=request.user.username)
    try:
        task = ResearchTasks.objects.get(pk=task_id)
    except ResearchTasks.DoesNotExist:
        raise Http404("Task does not exist")
    task.num_workers -= 1
    tuj = TaskUserJunction()
    tuj.worker_id = user
    tuj.task_id = task
    tuj.save()
    task.save()
    messages.info(request, 'New Task Claimed')
    return HttpResponseRedirect('/tasks/')

#Controller for adding Viewing Claimed Tasks
@login_required
def claimed_tasks(request):
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'worker':
        messages.info(request, 'Permission Denied!! You do not have permission to access this page')
        return HttpResponseRedirect('/')
    tuj_list =TaskUserJunction.objects.filter(worker_id = user)
    context = {
        'tuj_list': tuj_list,
    }
    return render(request, 'tasks/claimed_task.html', context)

#Controller for adding Answer. If method is post submit form else show the form
@login_required
def answer(request, task_id):
    task = ResearchTasks.objects.get(pk=task_id)
    user = User.objects.get(username=request.user.username)
    try:
        tuj = TaskUserJunction.objects.get(worker_id=user, task_id=task)
    except TaskUserJunction.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance = tuj)
        if form.is_valid():
            temp_tuj = form.save(commit=False)
            temp_tuj.submission_time = datetime.now()
            temp_tuj.save()
            if temp_tuj.task_id.audit_by == 1:
                audit_prob = temp_tuj.task_id.audit_prob
            else:
                audit_prob = user.profile.audit_prob_user
            if random.random() <= audit_prob:
                audit = Audit()
                audit.task_id = task
                audit.save()
            if temp_tuj.task_id.salary_by == 1:
                salary = temp_tuj.task_id.salary_task
            else:
                salary = temp_tuj.worker_id.profile.salary
            user.profile.total_salary += salary
            user.profile.save()
            messages.info(request, 'Answer Added')
            return HttpResponseRedirect('/tasks/claimed/')
    else:
        form = AnswerForm()
    context = {
        'tuj': tuj,
        'form': form,
        'task' : task,
    }
    return render(request, 'tasks/answer.html', context)

@login_required
def open_audits(request):
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'auditor':
        messages.info(request, 'Permission Denied!! You do not have permission to access this page')
        return HttpResponseRedirect('/')
    audit_list = Audit.objects.filter(auditor_id=None)
    context = {
        'audit_list': audit_list,
    }
    return render(request, 'tasks/open_audit.html', context)

@login_required
def detail_audit(request, task_id):
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'auditor':
        messages.info(request, 'Permission Denied!! You do not have permission to access this page')
        return HttpResponseRedirect('/')
    try:
        task = ResearchTasks.objects.get(pk=task_id)
        audit_tasks = Audit.objects.get(task_id = task)
        tuj = TaskUserJunction.objects.get(task_id=task)
    except ResearchTasks.DoesNotExist:
        raise Http404("Task does not exist")
    return render(request, 'tasks/detail_audit.html', {'audit_task': audit_tasks, 'tuj': tuj})

@login_required
def claim_audit(request, task_id):
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'auditor':
        messages.info(request, 'Permission Denied!! You do not have permission to access this page')
        return HttpResponseRedirect('/')
    try:
        task = ResearchTasks.objects.get(pk=task_id)
        audit_tasks = Audit.objects.get(task_id=task)
    except ResearchTasks.DoesNotExist:
        raise Http404("Task does not exist")
    audit_tasks.auditor_id = user
    audit_tasks.start_time = datetime.now()
    audit_tasks.save()
    messages.info(request, 'Task Claimed for Review')
    return HttpResponseRedirect('/tasks/audits/')

@login_required
def audit_tasks(request):
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'auditor':
        messages.info(request, 'Permission Denied!! You do not have permission to access this page')
        return HttpResponseRedirect('/')
    audit_list =Audit.objects.filter(auditor_id = user)
    context = {
        'audit_list': audit_list,
    }
    return render(request, 'tasks/audit_list.html', context)

@login_required
def submit_audit(request, task_id):
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'auditor':
        messages.info(request, 'Permission Denied!! You do not have permission to access this page')
        return HttpResponseRedirect('/')
    task = ResearchTasks.objects.get(pk=task_id)
    try:
        tuj = TaskUserJunction.objects.get(task_id=task)
        audit_task = Audit.objects.get(auditor_id=user, task_id=task)
    except TaskUserJunction.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        form = AuditForm(request.POST, instance = audit_task)
        if form.is_valid():
            temp_audit_task = form.save(commit=False)
            temp_audit_task.finish_time = datetime.now()
            temp_audit_task.save()

            #Salary calculation. Refactor this code
            worker = tuj.worker_id
            if audit_task.task_correct:
                if tuj.task_id.salary_by == 1:
                    bonus = tuj.task_id.bonus_task
                else:
                    bonus = worker.profile.bonus
                worker.profile.total_salary += bonus
                worker.profile.save()
            else:
                if tuj.task_id.salary_by == 1:
                    fine = tuj.task_id.fine_task
                else:
                    fine = worker.profile.fine
                worker.profile.total_salary -= fine
                worker.profile.save()
            messages.info(request, 'Review Submitted')
            return HttpResponseRedirect('/tasks/audits/')
    else:
        form = AuditForm()
    context = {
        'audit_task': audit_task,
        'form': form,
        'tuj' : tuj,
    }
    return render(request, 'tasks/submit_audit.html', context)

@login_required
def all_task_status(request):
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'admin':
        messages.info(request, 'Permission Denied!! You do not have permission to access this page')
        return HttpResponseRedirect('/')

    mentors = Profile.objects.filter(role='mentor')
    mentor_dict = {}
    for usr in mentors:
        username=User.objects.get(id=usr.user_id)
        mentor_dict[username]=str(usr.user_id)

    return render(request, 'tasks/all_task_status.html', {'mentor_dict': mentor_dict})

@login_required
def task_status(request, userid):
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'mentor' and profile != 'admin':
        messages.info(request, 'Permission Denied!! You do not have permission to access this page')
        return HttpResponseRedirect('/')

    participants = Profile.objects.filter(mentor_id=userid)
    user_names = []
    for usr in participants:
        user = User.objects.get(id=usr.user_id)
        tasks_claimed = TaskUserJunction.objects.filter(worker_id_id=usr.user_id)
        for task in tasks_claimed:
            task_summary = ResearchTasks.objects.get(id=task.task_id_id).task_summary
            if_audit = 1
            try:
                task_audit = Audit.objects.get(task_id_id=task.task_id_id)
            except:
                if_audit = 0
            if task.submission_time is None:
                user_names.append([user.username, task_summary, 'claimed', task.task_id_id])
            elif task.submission_time is not None and if_audit == 0:
                user_names.append([user.username, task_summary, 'finished without audit', task.task_id_id])
            elif task.submission_time is not None and if_audit == 1:
                if task_audit.finish_time is None:
                    user_names.append([user.username, task_summary, 'waiting for audit', task.task_id_id])
                elif task_audit.task_correct == 1:
                    user_names.append([user.username, task_summary, 'successful audit', task.task_id_id])
                else:
                    user_names.append([user.username, task_summary, 'failed audit', task.task_id_id])

    return render(request, 'tasks/task_status.html', {'user_names': user_names})
