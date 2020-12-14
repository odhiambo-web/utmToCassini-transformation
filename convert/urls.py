from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload-csv', views.upload, name='upload'),
    path('convert', views.convert, name='convert'),
    path('transform', views.transform, name='transform'),
]