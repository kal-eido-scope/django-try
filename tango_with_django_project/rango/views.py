from django.http.request import HttpRequest
from django.shortcuts import render,HttpResponse
from django.conf import settings
from rango.models import Category,Page
from rango.forms import CategoryForm, PageForm
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
# Create your views here.
