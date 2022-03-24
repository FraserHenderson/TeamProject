from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Medium, MediaCategory, UserEntity
from rango.forms import UserForm, UserProfileForm, MediumForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views import View
from django.utils.decorators import method_decorator
from rango.models import UserProfile
from django.contrib.auth.models import User
from rango.bing_search import run_query


import logging
logger = logging.getLogger(__name__)


class IndexView(View):
    def get(self, request):
        posts_list = Medium.objects.order_by('-publish_date')[:5]
        users_list = UserEntity.objects.order_by('name')
        media_categories_list = MediaCategory.objects.order_by('name')
    
        context_dict = {}
        context_dict['posts'] = posts_list
        context_dict['media_categories'] = media_categories_list
        context_dict['users'] = users_list
    
        visitor_cookie_handler(request)
    
        response = render(request, 'rango/index.html', context_dict)
    
        return response

class AboutView(View):
    def get(self, request):
        users_list = UserEntity.objects.order_by('name')

        context_dict = {}
        context_dict['users'] = users_list

        return render(request, 'rango/about.html', context_dict)


class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        #form = CategoryForm()
        form = None;
        return render(request, 'rango/add_category.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return IndexView(request)
        else:
            print(form.errors)
        
        return render(request, 'rango/add_category.html', {'form': form})


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    
    if not val:
        val = default_val
    
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

class GotoView(View):
    def get(self, request):
        page_id = request.GET.get('page_id')
        
        try:
            selected_page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return redirect(reverse('rango:index'))
            
        selected_page.views = selected_page.views + 1
        selected_page.save()
        
        return redirect(selected_page.url)

class RegisterProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = UserProfileForm()
        context_dict = {'form': form}
        return render(request, 'rango/profile_registration.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            u = UserEntity.objects.get_or_create(name=request.user.username)[0]
            u.name = request.user.username
            u.profile_picture = form['picture'].value()
            u.save()

            return redirect('rango:index')
        else:
            print(form.errors)
        
        context_dict = {'form': form}
        return render(request, 'rango/profile_registration.html', context_dict)

class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        userprofile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': userprofile.picture})
        posts = Medium.objects.filter(medium_author__name__exact=username)
        users_list = UserEntity.objects.order_by('name')
        
        return (user, userprofile, form, posts, users_list)
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, userprofile, form, posts, users_list) = self.get_user_details(username)
        except TypeError:
            return redirect('rango:index')
        
        context_dict = {'userprofile': userprofile,
                        'selecteduser': user,
                        'form': form,
                        'posts': posts,
                        'users_list': users_list}
        
        return render(request, 'rango/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, userprofile, form, posts, users_list) = self.get_user_details(username)
        except TypeError:
            return redirect('rango:index')
        
        if user == request.user:  # Added for authentication exercise.
            form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        
            if form.is_valid():
                form.save(commit=True)
                return redirect('rango:profile', user.username)
            else:
                print(form.errors)
        
            context_dict = {'userprofile': userprofile,
                            'selecteduser': user,
                            'form': form,
                            'posts': posts,
                            'users_list': users_list}
        
        return render(request, 'rango/profile.html', context_dict)

class MediumView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        userprofile = UserProfile.objects.get_or_create(user=user)[0]
        
        return (user, userprofile)
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, userprofile) = self.get_user_details(username)
            form = MediumForm()
        except TypeError:
            return redirect('rango:index')
        
        category_list = MediaCategory.objects.order_by('name')
        users_list = UserEntity.objects.order_by('name')
        
        context_dict = {'form' : form, 'user': user, 'userprofile': userprofile, 'category_list' : category_list}
        context_dict['users'] = users_list

        return render(request, 'rango/new_post.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        context_dict = {}
        try:
            (user, userprofile) = self.get_user_details(username)
        except TypeError:
            return redirect('rango:index')
        

        form = MediumForm(request.POST, request.FILES)
        context_dict['form'] = form
        
        if form.is_valid():
            medium = form.save(commit=False)
            medium.medium_author = UserEntity.objects.get(name=user.username)
            medium.medium_category = MediaCategory.objects.get(name=request.POST["dropdown"])
            medium.likes = 0
            medium.views = 0
            medium.publish_date = datetime.strptime((str(datetime.now()))[:19], '%Y-%m-%d %H:%M:%S')
            medium.save()
                
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)
        

        users_list = UserEntity.objects.order_by('name')

        context_dict = {'user': user, 'userprofile': userprofile}
        context_dict['users'] = users_list
        
        return render(request, 'rango/new_post.html', context_dict)


class MyCollectionView(View):
    def get(self, request):
        posts_list = Medium.objects.filter(medium_author = user).order_by('-publish_date')
        users_list = UserEntity.objects.order_by('name')
        media_categories_list = MediaCategory.objects.order_by('name')
    
        context_dict = {}
        context_dict['posts'] = posts_list
        context_dict['media_categories'] = media_categories_list
        context_dict['users'] = users_list

    
        visitor_cookie_handler(request)
    
        response = render(request, 'rango/index.html', context_dict)
    
        return response
    
def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        results = Medium.objects.filter(name__contains=query)
        
        return render(request, 'rango/search.html', {'query': query, 'results': results})
    else:
        return render(request, 'rango/search.html', {})
