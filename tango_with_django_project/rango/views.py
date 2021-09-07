from django.shortcuts import render,HttpResponse
from django.conf import settings
from rango.models import Category,Page
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
# Create your views here.
