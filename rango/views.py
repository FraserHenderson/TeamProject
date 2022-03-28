from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Medium, MediaCategory, UserEntity
from rango.forms import UserForm, UserProfileForm,CategoryRequestForm , MediumForm
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
        media_categories_list = MediaCategory.objects.filter(approved=True).order_by('name')
    
        context_dict = {}
        context_dict['posts'] = posts_list
        context_dict['media_categories'] = media_categories_list
        context_dict['users'] = users_list
    
        #visitor_cookie_handler(request)
    
        response = render(request, 'rango/index.html', context_dict)
    
        return response

class AboutView(View):
    def get(self, request):
        users_list = UserEntity.objects.order_by('name')

        context_dict = {}
        context_dict['users'] = users_list

        return render(request, 'rango/about.html', context_dict)


class AddCategoryRequestView(View):
    @method_decorator(login_required)
    def get(self, request, username):
        ensure_that_corresponding_UserEntity_exists(username)

        form = CategoryRequestForm()
        context_dict = {}
        context_dict['form'] = form

        return render(request, 'rango/add_category.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        ensure_that_corresponding_UserEntity_exists(username)

        form = CategoryRequestForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return redirect('the_stash:index')
        else:
            print(form.errors)

        context_dict = {}
        context_dict['form'] = form
        
        return render(request, 'rango/add_category.html', context_dict)

class ShowCategoryRequestsView(View):
    @method_decorator(login_required)
    def get(self, request, username):
        ensure_that_corresponding_UserEntity_exists(username)

        pending_categories_list = MediaCategory.objects.filter(approved=False).order_by('name')

        context_dict = {}
        context_dict['pending_categories'] = pending_categories_list

        return render(request, 'rango/category_requests.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        ensure_that_corresponding_UserEntity_exists(username)

        approved_category_name = request.POST['dropdown']
        approved_category = MediaCategory.objects.get(name=approved_category_name)
        approved_category.approved = True
        approved_category.save()

        return redirect('the_stash:index')

class GotoView(View):
    def get(self, request):
        page_id = request.GET.get('page_id')
        
        try:
            selected_page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            return redirect(reverse('the_stash:index'))
            
        selected_page.views = selected_page.views + 1
        selected_page.save()
        
        return redirect(selected_page.url)

class RegisterProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = UserProfileForm()
        context_dict = {}
        context_dict['form'] = form
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

            return redirect('the_stash:index')
        else:
            print(form.errors)
        
        context_dict = {}
        context_dict['form'] = form
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
            ensure_that_corresponding_UserEntity_exists(username)
        except TypeError:
            return redirect('the_stash:index')
        
        context_dict = {}
        context_dict['userprofile'] = userprofile
        context_dict['selecteduser'] = user
        context_dict['form'] = form
        context_dict['posts'] = posts
        context_dict['users_list'] = users_list
        
        return render(request, 'rango/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, userprofile, form, posts, users_list) = self.get_user_details(username)
            ensure_that_corresponding_UserEntity_exists(username)
        except TypeError:
            return redirect('the_stash:index')
        
        if user == request.user:  # Added for authentication exercise.
            form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        
            if form.is_valid():
                form.save(commit=True)

                user_entity = UserEntity.objects.get(name=user.username)
                user_entity.profile_picture = form['picture'].value()
                user_entity.save()

                return redirect('the_stash:profile', user.username)
            else:
                print(form.errors)
        
            context_dict = {}
            context_dict['userprofile'] = userprofile
            context_dict['selecteduser'] = user
            context_dict['form'] = form
            context_dict['posts'] = posts
            context_dict['users_list'] = users_list
        
        return render(request, 'rango/profile.html', context_dict)

class MediumView(View):
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            user = get_user(username)
            form = MediumForm()
        except TypeError:
            return redirect('the_stash:index')
        
        category_list = MediaCategory.objects.filter(approved=True).order_by('name')
        users_list = UserEntity.objects.order_by('name')
        
        context_dict = {}
        context_dict['user'] = user
        context_dict['users'] = users_list
        context_dict['form'] = form
        context_dict['category_list'] = category_list

        return render(request, 'rango/new_post.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            user = get_user(username)
            form = MediumForm(request.POST, request.FILES)
        except TypeError:
            return redirect('the_stash:index')
        
        if form.is_valid():
            medium = form.save(commit=False)
            medium.medium_author = UserEntity.objects.get(name=user.username)
            medium.medium_category = MediaCategory.objects.get(name=request.POST["dropdown"])
            medium.likes = 0
            medium.views = 0
            medium.publish_date = datetime.strptime((str(datetime.now()))[:19], '%Y-%m-%d %H:%M:%S')
            medium.save()
                
            return redirect('the_stash:my_collection', user.username)
        else:
            print(form.errors)
        

        users_list = UserEntity.objects.order_by('name')

        context_dict = {}
        context_dict['user'] = user
        context_dict['users'] = users_list
        context_dict['form'] = form
        
        return render(request, 'rango/new_post.html', context_dict)


class MyCollectionView(View):
    def get(self, request, username):
        ensure_that_corresponding_UserEntity_exists(username)

        target_user = UserEntity.objects.get(name=username)
        posts_list = Medium.objects.filter(medium_author=target_user).order_by('-publish_date')
        users_list = UserEntity.objects.order_by('name')
        media_categories_list = MediaCategory.objects.filter(approved=True).order_by('name')
    
        context_dict = {}
        context_dict['posts'] = posts_list
        context_dict['media_categories'] = media_categories_list
        context_dict['users'] = users_list
        context_dict['target_user'] = target_user

    
        #visitor_cookie_handler(request)
    
        response = render(request, 'rango/my_collection.html', context_dict)
    
        return response
    
class MediaCategoryView(View):
    def get(self, request, category):
        target_category = MediaCategory.objects.get(name=category)
        posts_list = Medium.objects.filter(medium_category=target_category).order_by('-publish_date')
    
        context_dict = {}
        context_dict['target_category'] = target_category
        context_dict['posts'] = posts_list
    
        response = render(request, 'rango/category.html', context_dict)
    
        return response
    
def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        search_type = ''
        results = None
        
        if 'media' in request.POST:
            search_type = 'media'
            results = Medium.objects.filter(name__contains=query)
        if 'category' in request.POST:
            search_type = 'category'
            results = MediaCategory.objects.filter(name__contains=query)
        if 'user' in request.POST:
            search_type = 'user'
            results = UserEntity.objects.filter(name__contains=query)
            
        print(search_type)
            
        return render(request, 'rango/search.html', {'query': query,'search_type': search_type,'results': results})
    else:
        return render(request, 'rango/search.html', {})


def get_user(username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    ensure_that_corresponding_UserEntity_exists(username)
    
    return user

def ensure_that_corresponding_UserEntity_exists(username):
    # Since behind the scenes Users can be created by other means (admin interface or command line "createsuperuser"), there are two possible fixes to do
    # this makes sure that the corresponding UserEntity exists in the database
    user_entity, created = UserEntity.objects.get_or_create(name=username)
    if created is True:
        user = User.objects.get(username=username)
        userprofile = UserProfile.objects.get(user=user)
        logger.warning(userprofile.picture)
        user_entity.profile_picture = userprofile.picture
        logger.warning(user_entity.profile_picture)
        user_entity.save()

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
    
class LikeMediaView(View):
    @method_decorator(login_required)
    def get(self, request):
        post_id = request.GET['post_id']
        logger.warning(post_id)
        print(post_id)
        
        try:
            post = Medium.objects.get(name=post_id)
        except Medium.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        post.likes = post.likes + 1
        post.save()
        return HttpResponse(post.likes)