from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from profile import Profile
from UserRoles import UserRoles
from changeRolesForm import ChangeRolesForm
from django.contrib import messages
from django.http import HttpResponseRedirect

@login_required
def view(request):
    user_id = User.objects.get(username=request.user.username).id
    profile = Profile.objects.get(user_id=user_id).role
    dict_functs={}
    if profile == UserRoles.TASK_UPDATER.value:
        dict_functs['/tasks/add_tasks']= 'Add task'
        dict_functs['/tasks/'] = 'View task'
        dict_functs['/help/'] = 'Help'

    if profile == UserRoles.ADMIN.value:
        dict_functs['/change_roles'] = 'Change Roles'
        dict_functs['/tasks/all_task_status'] = 'Mentor Status'
        dict_functs['/help/'] = 'Help'

    if profile == UserRoles.WORKER.value:
        dict_functs['/tasks/claimed/'] = 'Claimed tasks'
        dict_functs['/tasks/'] = 'Open tasks'
        dict_functs['/messages/'] = 'Messages'
        dict_functs['/help/'] = 'Help'

    if profile == UserRoles.AUDITOR.value:
        dict_functs['/tasks/open_audits/'] = 'Open Audits'
        dict_functs['/tasks/audits/'] = 'Claimed Audits'
        dict_functs['/help/'] = 'Help'

    if profile == UserRoles.MENTOR.value:
        dict_functs['/messages/'] = 'Messages'
        dict_functs['/tasks/task_status/'+str(user_id)+'/'] = 'Task Status'
        dict_functs['/help/'] = 'Help'

    return render(request, 'home.html', {"profile": profile, "dict_functs" : dict_functs})

@login_required
def change_roles(request):
    user = User.objects.get(username=request.user.username)
    profile = user.profile.role
    if profile != 'admin':
        messages.warning(request, 'Permission Denied!! You do not have permission to access this page')
        return HttpResponseRedirect('/')

    users = User.objects.all()
    if request.method == 'POST':
        for user in users:
            id = 'role_'+str(user.id)
            if 'Select' != request.POST.get(id):
                user.profile.role = request.POST.get(id)
                user.save()
        return redirect('/')
    user_dict=dict()
    for usr in users:
        prf = Profile.objects.get(user_id=usr.id)
        user_dict[usr.id] = [usr.username, usr.email, prf.role]
    form = ChangeRolesForm(users=user_dict)
    return render(request, 'changeRoles.html', {'form': form, 'user_dict':user_dict})