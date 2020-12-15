from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload-csv', views.upload, name='upload'),
    path('convert', views.convert, name='convert'),
    path('transform', views.transform, name='transform'),
    path('geographic', views.geographic, name='geographic'),
    path('utm', views.utm, name='utm'),
    path('cassini', views.cassini, name='cassini'),
]