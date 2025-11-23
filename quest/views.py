from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Profile  # Make sure you have Profile model with account_type field

# Homepage
def index(request):
    return render(request, 'quest/index.html')


# Redirect user to child.html or parent.html after login
@login_required(login_url='login')
def dashboard(request):
    user = request.user
    if hasattr(user, 'profile'):  # Make sure profile exists
        if user.profile.account_type == 'child':
            return render(request, 'quest/child.html')
        elif user.profile.account_type == 'parent':
            return render(request, 'quest/parent.html')
    # Fallback if profile or account_type missing
    return render(request, 'quest/index.html')


# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        role = request.POST.get('role')
        if form.is_valid():
            user = form.save()
            # Create profile automatically
            Profile.objects.create(
                user=user,
                account_type=role  # 'child' or 'parent'
            )
            return redirect('login')  # After registration, redirect to login
    else:
        form = UserCreationForm()
    return render(request, 'quest/register.html', {'form': form})
