from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^register$',views.register),
    url(r'^register_handler$',views.register_handler,name='register_handler'),
    url(r'^login$',views.login,name='login'),
    url(r'^login_handle$',views.login_handle,name='login_handle'),
    url(r'^site$',views.site,name='site'),
    url(r'^logout$',views.logout,name='logout'),
    url(r'^info$',views.info,name='info'),
]