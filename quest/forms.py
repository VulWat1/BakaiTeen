from django import forms
from django.contrib.auth.models import User
from .models import Profile, Task

class ChildCreateForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self, parent_user):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        child_user = User.objects.create_user(username=username, password=password)

        # меняем профиль нового пользователя
        child_profile = child_user.profile
        child_profile.role = 'child'
        child_profile.parent = parent_user
        child_profile.save()

        return child_user



class TaskCreateForm(forms.ModelForm):
    # Явно указываем поле child как User
    child = forms.ModelChoiceField(queryset=User.objects.none())

    class Meta:
        model = Task
        fields = ['child', 'title', 'description', 'reward']

    def __init__(self, *args, **kwargs):
        parent = kwargs.pop('parent')
        super().__init__(*args, **kwargs)
        # Ограничиваем выбор детей только детьми данного родителя
        self.fields['child'].queryset = User.objects.filter(
            profile__parent=parent,
            profile__role='child'
        )
