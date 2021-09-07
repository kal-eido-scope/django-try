import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',             #设置环境变量
                      'tango_with_django_project.settings')

import django                             #初始化django基础设施
django.setup()
from rango.models import Category,Page
from random import randint
def populate():
    python_pages = [
        {"title":"Official Python Tutorial",
         "url":"https://docs.python.org/2/tutorial/"},
        {"title":"How to think like a Computer Scientist",
         "url":"http://www.greenteapress.com/thinkpython/"},
        {"title":"Learn Python in 10 Minutes",
         "url":"http://www.korokithakis.net/tutorials/python/"}
    ]
    django_pages = [
        {"title":"Official Django Tutorial",
         "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title":"Django Rocks",
         "url":"http://www.djangorocks.com/"},
        {"title":"How to Tango with Django",
         "url":"http://www.tangowithdjango.com/"}
    ]
    other_pages = [
        {"title":"Bottle",
         "url":"http://bottlepy.org/docs/dev/"},
        {"title":"Flask",
         "url":"http://flask.pocoo.org"}
    ]
    cats = {"Python":{"pages":python_pages,"views":128,"likes":64},
            "Django":{"pages":django_pages,"views":64,"likes":32},
            "Other frameworks":{"pages":other_pages,"views":32,"likes":16}}
    for cat,cat_data in cats.items():
        c = add_cat(cat,cat_data["views"],cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c,p["title"],p["url"],randint(1,60))
    for c in Category.objects.all():
        for p in Page.objects.filter(category = c):
            print("- {0} - {1}".format(str(c),str(p)))

def add_page(cat,title,url,views=0):
    p = Page.objects.get_or_create(category=cat,title=title)[0]     #get_or_create返回(object,created:bool)
    p.url = url
    p.views = views
    p.save()
    return p
def add_cat(name,views,likes):
    c = Category.objects.get_or_create(name=name,views=views,likes=likes)[0]
    c.save()
    return c
if __name__ == "__main__":
    print("Starting Rango population script....")
    populate()