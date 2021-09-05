from django.shortcuts import render,HttpResponse
def index(request):
    context_dict = {'boldmessage':"Crunchy,creamy,cookie,candy,cupcake"}
    return render(request,'rango/index.html',context=context_dict)
def about(request):
    content = '<a href="/rango/">Index</a>' 
    return HttpResponse('Rango says here is the about page!'+content)
# Create your views here.
