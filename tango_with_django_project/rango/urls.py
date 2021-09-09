from populate_rango import add_page
from django.urls import re_path
from rango import views
app_name = 'rango'
urlpatterns = [
    re_path(r'^$',views.index,name = 'index'),
    re_path(r'about/',views.about,name = 'about'),
    re_path(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.show_category,name='show_category'),
    re_path(r'^add_category/$',views.add_category,name='add_category'),
    re_path(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/',views.add_page,name='add_page')
]
