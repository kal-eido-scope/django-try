from django.shortcuts import render,HttpResponse
from django.conf import settings
def index(request):
    context_dict = {'boldmessage':"Crunchy,creamy,cookie,candy,cupcake"}
    return render(request,'rango/index.html',context=context_dict)
def about(request):
    """content = '<a href="/rango/">Index</a>' 
    return HttpResponse('Rango says here is the about page!'+content)"""
    context_dict = {'MEDIA_URL':settings.MEDIA_URL}
    return render(request,'rango/about.html',context = context_dict)
# Create your views here.
