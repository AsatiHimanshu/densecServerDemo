
from django.urls import path, re_path
from django.views import View
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns=[

    # re_path('', csrf_exempt(views.post2), name ='base'),

    re_path(r'^post1/',csrf_exempt(views.post1), name='post1'),
#   url path to add the data for captured image
    re_path(r'^post2/',csrf_exempt(views.post2), name='post2'),
#   url path to update teh data for captured image
    re_path(r'^post3/',csrf_exempt(views.post3), name='post3')
]
