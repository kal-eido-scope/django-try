from io import UnsupportedOperation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from rango.models import User
from django.http.request import HttpRequest
from django.shortcuts import render,HttpResponse
from django.conf import settings
from rango.models import Category,Page, UserProfile
from rango.forms import CategoryForm, PageForm,UserForm,UserProfileForm
def index(request):
    context_dict = {}
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = pages_list
    context_dict['categories'] = category_list
    return render(request,'rango/index.html',context=context_dict)
def about(request):
    """content = '<a href="/rango/">Index</a>' 
    return HttpResponse('Rango says here is the about page!'+content)"""
    context_dict = {'MEDIA_URL':settings.MEDIA_URL}
    return render(request,'rango/about.html',context = context_dict)
def show_category(request,category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug = category_name_slug)
        pages = Page.objects.filter(category = category)

        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request,'rango/category.html',context_dict)
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':    #是HTTP请求吗？
        form = CategoryForm(request.POST)

        if form.is_valid():         #表单数据有效
            form.save(commit=True)  #存储
            return index(request)   #返回首页，也可显示确认消息
        else:
            print(form.errors)      #显示错误
    context_dict = {'form':form}
    return render(request,'rango/add_category.html',context_dict)
def add_page(request,category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
            return show_category(request,category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form,'category':category}
    return render(request,'rango/add_page.html',context_dict)
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context_dict = {'user_form':user_form,
                    'profile_form':profile_form,
                    'registered':registered}
    return render(request,'rango/register.html',context_dict)
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details:{0},{1}".format(username,password))
            if User.objects.all().filter(username=username).count()==0:
                return HttpResponse("User %s is not registered."%username)
            else:
                return HttpResponse("You've entered a wrong password.")
    else:
        return render(request,'rango/login.html',{})

@login_required     #登录后的受限视图
def restricted(request):
    context_dict = {}
    return render(request,'rango/restricted.html',context_dict)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
# Create your views here.
