from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random
from .models import Task, Step
from django.db.models import Q
from django.contrib.auth.models import User
import datetime


@login_required(login_url="/login")
def task_done(request, pk):
    user = request.user
    my_task_id = user.userprofile.daily_task
    if my_task_id == pk:
        task = get_object_or_404(Task, id=pk)
        return render(request, 'dailytask/task_done.html', {'task': task})
    else:
        task = get_object_or_404(Task, id=my_task_id)
        return redirect('detail', pk=my_task_id)


@login_required(login_url="/login")
def traffic_task(request):
    user = request.user
    if user.userprofile.daily_task == 0:
        tasks_traffic = Task.objects.filter(category="traffic")

        random_task = random.choice(tasks_traffic)
        task_id = random_task.pk
        user = request.user
        user.userprofile.daily_task = task_id
        user.userprofile.save()
        return task_detail(request=request, pk=task_id)
    else:
        user = request.user
        task_id = user.userprofile.daily_task
        return task_done(request, pk=task_id)


@login_required(login_url="/login")
def conversion_rate_task(request):
    user = request.user
    if user.userprofile.daily_task == 0:
        all_tasks_category = Task.objects.filter(category="conversion_rate")
        random_task = random.choice(all_tasks_category)
        task_id = random_task.pk
        user = request.user
        user.userprofile.daily_task = task_id
        user.userprofile.save()
        return task_detail(request=request, pk=task_id)
    else:
        user = request.user
        task_id = user.userprofile.daily_task
        return task_done(request, pk=task_id)


@login_required(login_url="/login")
def marketing_task(request):
    user = request.user
    if user.userprofile.daily_task == 0:
        all_tasks_category = Task.objects.filter(category="marketing")
        random_task = random.choice(all_tasks_category)
        task_id = random_task.pk
        user = request.user
        user.userprofile.daily_task = task_id
        user.userprofile.save()
        return task_detail(request=request, pk=task_id)
    else:
        user = request.user
        task_id = user.userprofile.daily_task
        return task_done(request, pk=task_id)


@login_required(login_url="/login")
def task_detail(request, pk):
    user = request.user
    my_task_id = user.userprofile.daily_task
    if my_task_id == pk:
        task = get_object_or_404(Task, id=pk)
        return render(request, 'dailytask/task_detail.html', {'task': task})
    else:
        return redirect('detail', pk=my_task_id)


@login_required(login_url="/login")
def step_detail(request, task_pk, step_pk):
    user = request.user
    my_task_id = user.userprofile.daily_task

    print("item step_detail function")
    print(my_task_id)

    if task_pk != my_task_id:
        task = get_object_or_404(Task, id=my_task_id)
        return redirect('detail', pk=my_task_id)
    else:
        step_list = Step.objects.filter(Q(task_id=task_pk) & Q(step_number=step_pk))
        if step_list.count() > 0:
            step = step_list[0]
        else:
            step = None
        next_step_pk = step_pk + 1
        next_step = Step.objects.filter(step_number=next_step_pk)
        if next_step.count() == 0:
            next_step_pk = None

        return render(request, 'dailytask/step_detail.html', {'step': step,
                                                              'next_step_pk': next_step_pk,
                                                              })
