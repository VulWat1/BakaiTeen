from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import create_task, tasks_list_child, tasks_list_parent, confirm_task, complete_task, request_exchange, exchange_list_parent


urlpatterns = [
    path('', views.index, name='Home'),
    path('child', views.dashboard, name='childD'),
    path('login/', auth_views.LoginView.as_view(template_name='quest/login.html', next_page='/'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # Children
    path('children/', views.children_list, name='children_list'),
    path('children/add/', views.add_child, name='add_child'),
    # Tasks
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/parent/', tasks_list_parent, name='tasks_list_parent'),
    path('tasks/child/', tasks_list_child, name='tasks_list_child'),
    path('tasks/complete/<int:task_id>/', complete_task, name='complete_task'),
    path('tasks/confirm/<int:task_id>/', confirm_task, name='confirm_task'),

    # Exchange
    path('exchange/request/', request_exchange, name='request_exchange'),
    path('exchange/parent/', exchange_list_parent, name='exchange_list_parent'),
    path('exchange/child/', views.exchange_list_child, name='exchange_list_child'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

