from django.urls import re_path
from rango import views
urlpatterns = [
    re_path(r'^$',views.index,name = 'index'),
    re_path(r'about/',views.about,name = 'about')
]
