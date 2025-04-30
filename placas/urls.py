from django.urls import path
from . import views

urlpatterns = [
    path('', views.camera_view, name='camera'),
    path('detectar-placa/', views.detectar_placa_view, name='detectar_placa'),
]
