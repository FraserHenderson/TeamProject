from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views import View
from django.utils.decorators import method_decorator
from rango.models import UserProfile
from django.contrib.auth.models import User
from rango.bing_search import run_query

class IndexView(View):
    def get(self, request):
        category_list = Category.objects.order_by('-likes')[:5]
        page_list = Page.objects.order_by('-views')[:5]
    
        context_dict = {}
        context_dict['boldmessage'] = 'Click a link and get exploring'
        context_dict['categories'] = category_list
        context_dict['pages'] = page_list
    
        visitor_cookie_handler(request)
    
        response = render(request, 'rango/index.html', context_dict)
    
        return response

class AboutView(View):
    def get(self, request):
        context_dict = {}
        context_dict['visits'] = request.session['visits']
        
        return render(request, 'rango/about.html', context_dict)

class ShowCategoryView(View):
    def create_context_dict(self, category_name_slug):
        """
        A helper method that was created to demonstrate the power of class-based views.
        You can reuse this method in the get() and post() methods!
        """
        context_dict = {}
        
        try:
            category = Category.objects.get(slug=category_name_slug)
            pages = Page.objects.filter(category=category).order_by('-views')
        
            context_dict['pages'] = pages
            context_dict['category'] = category
        except Category.DoesNotExist:
            context_dict['category'] = None
            context_dict['pages'] = None
        
        return context_dict
    
    def get(self, request, category_name_slug):
        context_dict = self.create_context_dict(category_name_slug)
        return render(request, 'rango/category.html', context_dict)
    
    def post(self, request, category_name_slug):
        context_dict = self.create_context_dict(category_name_slug)
        query = request.POST['query'].strip()
        
        if query:
            context_dict['result_list'] = run_query(query)
            context_dict['query'] = query
        
        return render(request, 'rango/category.html', context_dict)

class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})
    
    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
        
        return render(request, 'rango/add_category.html', {'form': form})

class AddPageView(View):
    def get_category_name(self, category_name_slug):
        """
        A helper method that was created to demonstrate the power of class-based views.
        You can reuse this method in the get() and post() methods!
        """
        try:
            category = Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            category = None
        
        return category
    
    @method_decorator(login_required)
    def get(self, request, category_name_slug):
        form = PageForm()
        category = self.get_category_name(category_name_slug)
        context_dict = {'form': form, 'category': category}
        return render(request, 'rango/add_page.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, category_name_slug):
        form = PageForm(request.POST)
        category = self.get_category_name(category_name_slug)
        
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                
                return HttpResponseRedirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
        
        context_dict = {'form': form, 'category': category}
        return render(request, 'rango/add_page.html', context_dict)

class RestrictedView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'rango/restricted.html')

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
        form = UserProfileForm({'website': userprofile.website,
                                'picture': userprofile.picture})
        
        return (user, userprofile, form)
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, userprofile, form) = self.get_user_details(username)
        except TypeError:
            return redirect('rango:index')
        
        context_dict = {'userprofile': userprofile,
                        'selecteduser': user,
                        'form': form}
        
        return render(request, 'rango/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, userprofile, form) = self.get_user_details(username)
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
                            'form': form}
        
        return render(request, 'rango/profile.html', context_dict)

##def search(request):
##    result_list = []
##    query = ''
##    
##    if request.method == 'POST':
##        query = request.POST['query'].strip()
##        
##        if query:
##            result_list = run_query(query)
##    
##    return render(request, 'rango/search.html', {'result_list': result_list, 'query': query})
