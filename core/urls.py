from operator import index
from django.urls import path, include
from . import views

from core.views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView


urlpatterns = [
  path('', views.index, name='index'),
  path('settings', views.settings, name='settings'),
  path('upload', views.upload, name='upload'),
  path('follow', views.follow, name='follow'),
  path('search', views.search, name='search'),
  path('like-post', views.like_post, name='like-post'),
  path('profile/<str:pk>', views.profile, name='profile'),
  path('signup', views.signup, name='signup'),
  path('signin', views.signin, name='signin'),
  path('logout', views.logout, name='logout'),

  path('aaa', views.aaa, name='aaa'),

  path('routes', views.routes, name='routes'),
  path('notes/', views.getNotes, name='notes'),
  path('notes/<str:pk>', views.getNote, name='note'),

  # 11/18 추가
  
  path('tasks', TaskList.as_view(), name='tasks'),
  path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
  path('task-create/', TaskCreate.as_view(), name='task-create'),
  path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
  path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),

  # path('task2', views.taskList, name='tasks2'),
  ]