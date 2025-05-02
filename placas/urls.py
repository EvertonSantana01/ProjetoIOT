from django.urls import path
from .views import camera_view, detectar_placa_view, ultima_consulta_json

urlpatterns = [
    path('', camera_view, name='dashboard'),
    path('detectar-placa/', detectar_placa_view, name='detectar_placa'),
    path('ultima-consulta-json', ultima_consulta_json, name='ultima_consulta_json'),
]
