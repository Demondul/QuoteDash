from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$',views.index),
    url(r'^register$',views.register),
    url(r'^home$',views.home),
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^edit/(?P<id>\d+)$',views.editUser),
    url(r'^newQuote/(?P<id>\d+)$',views.newQuote),
    url(r'^user/(?P<id>\d$)$',views.user),
    url(r'^like/(?P<id>\d+)$',views.like),
    url(r'^delete/(?P<qid>\d+)$',views.delete)
]