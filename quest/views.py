from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Task, ExchangeRequest  # <- добавил ExchangeRequest
from .forms import ChildCreateForm, TaskCreateForm
from django.contrib.auth.models import User


def index(request):
    return render(request, 'quest/index.html')


# =================Child_Side=====================

@login_required
def add_child(request):
    if request.user.profile.role != 'parent':
        return redirect('home')  # детям нельзя

    if request.method == 'POST':
        form = ChildCreateForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('children_list')
    else:
        form = ChildCreateForm()

    return render(request, 'quest/add_child.html', {'form': form})


@login_required
def children_list(request):
    if request.user.profile.role != 'parent':
        return redirect('home')

    # Get all child users of the current parent
    children = User.objects.filter(profile__parent=request.user)

    return render(request, 'quest/children_list.html', {'children': children})


# ======================END======================

# =====================Task_Side=====================

@login_required
def create_task(request):
    if request.user.profile.role != 'parent':
        return redirect('home')

    if request.method == 'POST':
        form = TaskCreateForm(request.POST, parent=request.user)
        if form.is_valid():
            task = form.save(commit=False)
            task.parent = request.user
            task.save()
            return redirect('tasks_list_parent')
    else:
        form = TaskCreateForm(parent=request.user)

    return render(request, 'quest/create_task.html', {'form': form})
    

@login_required
def tasks_list_parent(request):
    tasks = Task.objects.filter(parent=request.user).order_by('-created_at')
    return render(request, 'quest/tasks_list_parent.html', {'tasks': tasks})


@login_required
def tasks_list_child(request):
    if request.user.profile.role != 'child':
        return redirect('home')

    tasks = request.user.tasks.all().order_by('-created_at')
    return render(request, 'quest/tasks_list_child.html', {'tasks': tasks})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user != task.child:
        return redirect('home')

    task.is_completed = True
    task.save()
    return redirect('tasks_list_child')

@login_required
def confirm_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user != task.parent:
        return redirect('home')

    if task.is_completed and not task.is_confirmed:
        task.is_confirmed = True
        profile = task.child.profile
        profile.money += task.reward
        profile.save()
        task.save()

    return redirect('tasks_list_parent')

# ==================END=====================

# ====================EXCHANGE===============

# @login_required
# def request_exchange(request):
#     if request.user.profile.role != 'child':
#         return redirect('home')

#     if request.method == 'POST':
#         try:
#             amount = int(request.POST.get('amount', 0))
#         except (ValueError, TypeError):
#             amount = 0

#         if amount > 0 and amount <= request.user.profile.money:
#             ExchangeRequest.objects.create(child=request.user, amount=amount)
#             # временно вычитаем монеты (если хочешь — можно вычитать только после подтверждения)
#             request.user.profile.money -= amount
#             request.user.profile.save()

#     return redirect('exchange_list_child')

def custom_404(request, exception=None):
    return render(request, 'quest/404.html', status=404)

@login_required
def request_exchange(request):
    if request.user.profile.role != 'child':
        return redirect('home')

    if request.method == 'POST':
        try:
            amount = int(request.POST.get('amount', 0))
        except (ValueError, TypeError):
            amount = 0

        if 0 < amount <= request.user.profile.money:
            # Создаём запрос
            ExchangeRequest.objects.create(child=request.user, amount=amount)
            # Опционально: временно вычитаем монеты
            request.user.profile.money -= amount
            request.user.profile.save()

    return redirect('exchange_list_child')


@login_required
def exchange_list_parent(request):
    if request.user.profile.role != 'parent':
        return redirect('home')

    reqs = ExchangeRequest.objects.filter(child__profile__parent=request.user).order_by('-created_at')
    return render(request, 'quest/exchange_list_parent.html', {'requests': reqs})

@login_required
def exchange_list_child(request):
    if request.user.profile.role != 'child':
        return redirect('home')

    requests = ExchangeRequest.objects.filter(child=request.user).order_by('-created_at')
    return render(request, 'quest/exchange_list_child.html', {'requests': requests})

# ======================END=====================

# ====================DASHBOARD_&_LOGIN&REGISTER===============
@login_required
def dashboard(request):
    user = request.user
    completed_tasks_count = user.tasks.filter(is_completed=True).count()
    pending_tasks_count = user.tasks.filter(is_completed=False).count()
    return render(request, 'quest/child.html', {
        'completed_tasks_count': completed_tasks_count,
        'pending_tasks_count': pending_tasks_count
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        role = request.POST.get('role')  # ожидается 'child' или 'parent'
        if form.is_valid() and role in ('child', 'parent'):
            user = form.save()
            Profile.objects.create(
                user=user,
                role=role
            )
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'quest/register.html', {'form': form})
# ====================END===================
