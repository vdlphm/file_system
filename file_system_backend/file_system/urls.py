from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.create, name='create'),
    path('cat/', views.catFile, name='catFile'),
    path('list/', views.listFolder, name='listFolder'),
    path('move/', views.moveTo, name='move'),
    path('remove/', views.delete, name='remove'),
    path('update/', views.update, name='update')
]