
from django.urls import path
from .views import camera_view, detectar_placa_view, ultima_consulta_json, consultar_placa_manual_view, veiculos_view, consultar_cadastrados_view, listar_veiculos_view, editar_veiculo_view, excluir_veiculo_view, veiculos_gerenciar_view

urlpatterns = [
    path('', camera_view, name='dashboard'),
    path('veiculos/', veiculos_view, name='pagina_veiculos'),
    path('detectar-placa/', detectar_placa_view, name='detectar_placa'),
    path('veiculos/gerenciar/', veiculos_gerenciar_view, name='veiculos_gerenciar'),
    path('ultima-consulta-json', ultima_consulta_json, name='ultima_consulta_json'),
    path('consultar-placa/', consultar_placa_manual_view, name='consultar_placa'),
    path('consultar-cadastrados/', consultar_cadastrados_view, name='consultar_cadastrados'),

    path('api/veiculos/', listar_veiculos_view, name='listar_veiculos'),
    path('api/veiculos/<int:id>/', editar_veiculo_view, name='editar_veiculo'),
    path('api/veiculos/<int:id>/excluir/', excluir_veiculo_view, name='excluir_veiculo'),
]


