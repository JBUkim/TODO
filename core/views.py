from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from core.models import Profile, Post, LikePost, FollowersCount, Note, Task
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.serializers import NoteSerializer

# 11/18
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

# Create your views here.

@login_required(login_url='signin')
def index(request) :
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(user=user_object)

  user_following_list = []
  feed = []

  user_following = FollowersCount.objects.filter(follower=request.user.username)

  for users in user_following:
    user_following_list.append(users.user)

  for usernames in user_following_list:
    feed_lists = Post.objects.filter(user=usernames)
    feed.append(feed_lists)
  
  feed_list = list(chain(*feed))

  # user suggestion starts
  all_users = User.objects.all()
  user_following_all = []
  
  for user in user_following :
    user_list = User.objects.get(username=user.user)
    user_following_all.append(user_list)
  
  new_suggestions_list = [ x for x in list(all_users) if (x not in list(user_following_all))]
  current_user = User.objects.filter(username=request.user.username)
  final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
  random.shuffle(final_suggestions_list)

  username_profile = []
  username_profile_list = []

  for users in final_suggestions_list :
    username_profile.append(users.id)

  for ids in username_profile :
    profile_lists = Profile.objects.filter(id_user=ids)
    username_profile_list.append(profile_lists)

  suggestions_username_profile_list = list(chain(*username_profile_list))


  posts = Post.objects.all()
  return render(request, 'index.html', {'user_profile' : user_profile, 'posts': posts,
                'suggestions_username_profile_list' : suggestions_username_profile_list,})

@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def search(request) :
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(user=user_object)

  if request.method == 'POST' :
    username = request.POST['username']
    username_object = User.objects.filter(username__icontains=username)

    username_profile = []
    username_profile_list = []

    for users in username_object :
      username_profile.append(users.id)

    for ids in username_profile :
      profile_lists = Profile.objects.filter(id_user=ids)
      username_profile_list.append(profile_lists)

    username_profile_list = list(chain(*username_profile_list))
  return render(request, 'search.html', {'user_profile' : user_profile, 'username_profile_list' : username_profile_list, })

@login_required(login_url='signin')
def follow(request) :
  if request.method == 'POST' :
    follower = request.POST['follower']
    user = request.POST['user']

    if FollowersCount.objects.filter(follower=follower, user=user).first() :
      delete_follower = FollowersCount.objects.get(follower=follower, user=user)
      delete_follower.delete()
      return redirect('/profile/'+ user)
    else:
      new_follower = FollowersCount.objects.create(follower=follower, user=user)
      new_follower.save()
      return redirect('/profile/'+ user)
  else :
    return redirect('/')

@login_required(login_url='signin')
def like_post(request) :
  username = request.user.username
  post_id = request.GET.get('post_id')

  post = Post.objects.get(id=post_id)

  like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

  if like_filter == None :
    new_like = LikePost.objects.create(post_id=post_id, username=username)
    new_like.save()
    post.no_of_likes = post.no_of_likes+1
    post.save()
    return redirect('/')
  else:
    like_filter.delete()
    post.no_of_likes = post.no_of_likes-1
    post.save()
    return redirect('/')

@login_required(login_url='signin')
def profile(request, pk) :
  user_object = User.objects.get(username=pk)
  user_profile = Profile.objects.get(user=user_object)
  user_posts = Post.objects.filter(user=pk)
  user_post_length = len(user_posts)

  follower = request.user.username
  user = pk

  if FollowersCount.objects.filter(follower=follower, user=user).first():
    button_text = 'Unfollow'
  else:
    button_text = 'Follow'

  user_followers =len(FollowersCount.objects.filter(user=pk))
  user_following =len(FollowersCount.objects.filter(follower=pk))

  context = {
    'user_object': user_object,
    'user_profile': user_profile,
    'user_posts': user_posts,
    'user_post_length': user_post_length,
    'button_text' : button_text,
    'user_followers' : user_followers,
    'user_following' : user_following,
  }
  return render(request, 'profile.html', context)

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request) :
  if request.method == "POST" :
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    if password == password2 :
      if User.objects.filter(email=email).exists() :
        messages.info(request, "Email Taken")
        return redirect('signup')
      elif User.objects.filter(username=username).exists() :
        messages.info(request, "Username Taken")
        return redirect('signup')
      else :
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Log user in and redirect to settings 
        user_login = auth.authenticate(username=username, password=password)
        auth.login(request, user_login)

        # create a profile object for the new user
        user_model = User.objects.get(username=username)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        return redirect('settings')

    else :
      messages.info(request, "Password Not Matching")
      return redirect('signup')

  else:
    return render(request, 'signup.html')

def signin(request) :
  
  if request.method == "POST" :
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username, password=password)
    
    if user is not None :
      auth.login(request, user)
      return redirect('/')
    else :
      messages.info(request, 'Credentails Invalid')
      return redirect('signin')

  else :
    return render(request, "signin.html") 

@login_required(login_url='signin')
def logout(request) :
  auth.logout(request)
  return redirect('signin')

# 실험
@login_required(login_url='signin')
def aaa(request) :
  user_object = User.objects.get(username=request.user.username)
  user_profile = Profile.objects.get(user=user_object)

  user_following_list = []
  feed = []

  user_following = FollowersCount.objects.filter(follower=request.user.username)

  for users in user_following:
    user_following_list.append(users.user)

  for usernames in user_following_list:
    feed_lists = Post.objects.filter(user=usernames)
    feed.append(feed_lists)
  
  feed_list = list(chain(*feed))

  # user suggestion starts
  all_users = User.objects.all()
  user_following_all = []
  
  for user in user_following :
    user_list = User.objects.get(username=user.user)
    user_following_all.append(user_list)
  
  new_suggestions_list = [ x for x in list(all_users) if (x not in list(user_following_all))]
  current_user = User.objects.filter(username=request.user.username)
  final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
  random.shuffle(final_suggestions_list)

  username_profile = []
  username_profile_list = []

  for users in final_suggestions_list :
    username_profile.append(users.id)

  for ids in username_profile :
    profile_lists = Profile.objects.filter(id_user=ids)
    username_profile_list.append(profile_lists)

  suggestions_username_profile_list = list(chain(*username_profile_list))


  posts = Post.objects.all()
  return render(request, 'aaa.html', {'user_profile' : user_profile, 'posts': posts,
                'suggestions_username_profile_list' : suggestions_username_profile_list,})

# note
@api_view(['GET'])
def routes(request):
  routes = [
        {
            'Endpoint': '/notes/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of notes'
        },
        {
            'Endpoint': '/notes/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/notes/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing note with data sent in post request'
        },
        {
            'Endpoint': '/notes/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting note'
        },
    ]
    
  return Response(routes)


@api_view(['GET'])
def getNotes(request) :
  notes = Note.objects.all()
  serializer = NoteSerializer(notes, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def getNote(request, pk) :

  notes = Note.objects.get(id=pk)
  serializer = NoteSerializer(notes, many=False)
  return Response(serializer.data)



# task-list

# 로그인/회원가입 사용x
class CustomLoginView(LoginView) :
  template_name = 'core/signin.html'
  fields = '__all__'
  redirect_authenticated_user = True

  def get_success_url(self):
    return reverse_lazy('tasks')

class RegisterPage(FormView) :
  template_name = 'core/signup.html'
  form_class = UserCreationForm
  redirect_authenticated_user = True
  success_url = reverse_lazy('tasks')

  def form_valid(self, form) :
    user = form.save()
    if user is not None:
      login(self.request, user)
    return super(RegisterPage, self).form_valid(form)
  
  def get(self, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect('tasks')
    return super(RegisterPage, self).get(*args, **kwargs)
  

# TaskList

class TaskList(LoginRequiredMixin, ListView) :
  model = Task
  context_object_name = 'tasks'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tasks'] = context['tasks'].filter(user=self.request.user)
    context['count'] = context['tasks'].filter(complete=False).count()

    search_input = self.request.GET.get('search-area') or ""
    if search_input:
      context['tasks'] = context['tasks'].filter(title__icontains=search_input)

      # #시작 단어로 검색
      # context['tasks'] = context['tasks'].filter(title__startswith=search_input)
    context['search_input'] = search_input
    return context

class TaskDetail(LoginRequiredMixin, DetailView) :
  model = Task
  context_object_name = 'task'
  template_name = "core/task.html"

class TaskCreate(LoginRequiredMixin, CreateView) :
  model = Task
  fields =  ['title', 'description', 'complete']
  success_url = reverse_lazy('tasks')

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView) :
  model = Task
  fields =  ['title', 'description', 'complete']
  success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView) :
  model = Task
  context_object_name = 'task'
  success_url = reverse_lazy('tasks')



# Change Form

# @login_required(login_url='signin')
# def taskList(request) :
#   user_object = User.objects.get(username=request.user.username)
#   user_profile = Profile.objects.get(user=user_object)

#   task_title = Task.objects.get(title=request.user.title)
#   user_title = Task.objects.get(title=task_title)

#   return render(request, 'task_list.html', { 'user_profile' : user_profile, 'user_title': user_title })


  # if request.method == 'POST':
  #   user = request.user.username
  #   title = request.POST['title']
  #   description = request.POST['description']

  #   new_task = Task.objects.create(user=user, title=title, description=description)
  #   new_task.save()
    
  #   return redirect('/task2')
  # else:
  #   return redirect('/task2')
