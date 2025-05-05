import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Consulta
from .detector.detector import detectar_placa
from .api_brasil import consultar_placa_apibrasil
from django.utils.timezone import now
import base64, json, cv2, numpy as np
from django.views.decorators.http import require_GET
from .models import Consulta
from .detector.detector import detectar_placa
from .api_brasil import consultar_placa_apibrasil


def camera_view(request):
    return render(request, 'placas/dashboard.html')

def veiculos_view(request):
    return render(request, 'placas/veiculos.html')


def ultima_consulta_json(request):
    ultima = Consulta.objects.order_by('-data_consulta').first()
    historico = Consulta.objects.order_by('-data_consulta')

    if not ultima:
        return JsonResponse({})

    return JsonResponse({
        "placa": ultima.placa,
        "modelo": ultima.modelo,
        "marca": ultima.marca,
        "cor": ultima.cor,
        "ano": ultima.ano,
        "municipio": ultima.municipio,
        "situacao": ultima.situacao_veiculo,  # agora correto
        "restricao": any([
            ultima.restricao1 and ultima.restricao1 != "SEM RESTRICAO",
            ultima.restricao2 and ultima.restricao2 != "SEM RESTRICAO",
            ultima.restricao3 and ultima.restricao3 != "SEM RESTRICAO",
            ultima.restricao4 and ultima.restricao4 != "SEM RESTRICAO",
        ]),
        "combustivel": ultima.combustivel,
        "potencia": ultima.potencia,
        "chassi": ultima.chassi,
        "versao": ultima.versao,
        "logo": ultima.logo_url,
        "data": ultima.data_consulta.strftime('%d/%m/%Y %H:%M'),
        "historico": [
            {
                "placa": c.placa,
                "modelo": c.modelo,
                "cor": c.cor,
                "municipio": c.municipio,
                "situacao": c.situacao_veiculo,
                "data": c.data_consulta.strftime('%d/%m/%Y %H:%M'),
            } for c in historico
        ]
    })


@csrf_exempt
def detectar_placa_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            img_data = data['imagem'].split(',')[1]
            img_bytes = base64.b64decode(img_data)
            nparr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            placa_detectada = detectar_placa(frame)

            if placa_detectada:
                dados = consultar_placa_apibrasil(placa_detectada)

                if dados:
                    Consulta.objects.create(
                        placa=placa_detectada,  # agora usa a placa detectada pela câmera
                        placa_modelo_antigo=dados.get("placa_modelo_antigo"),
                        placa_modelo_novo=dados.get("placa_modelo_novo"),
                        placa_nova=dados.get("placa_nova"),

                        marca=dados.get("marca"),
                        modelo=dados.get("modelo"),
                        submodelo=dados.get("SUBMODELO"),
                        versao=dados.get("VERSAO"),

                        ano=dados.get("ano"),
                        ano_modelo=dados.get("anoModelo"),
                        cor=dados.get("cor_veiculo", {}).get("cor") or dados.get("cor"),
                        municipio=dados.get("municipio") or dados.get("extra", {}).get("municipio", {}).get("municipio"),
                        uf=dados.get("uf"),

                        chassi=dados.get("extra", {}).get("chassi") or dados.get("chassi"),
                        situacao_chassi=dados.get("situacao_chassi"),
                        situacao_veiculo=dados.get("situacao_veiculo"),
                        nacionalidade=dados.get("nacionalidade", {}).get("nacionalidade") or dados.get("extra", {}).get("nacionalidade"),

                        combustivel=dados.get("combustivel") or dados.get("extra", {}).get("combustivel"),
                        potencia=dados.get("potencia"),
                        cilindradas=dados.get("cilindradas"),

                        capacidade_carga=dados.get("capacidade_carga"),
                        quantidade_passageiro=dados.get("quantidade_passageiro"),
                        peso_bruto_total=dados.get("peso_bruto_total"),
                        eixos=dados.get("eixos"),

                        tipo_veiculo=dados.get("tipo_veiculo", {}).get("tipo_veiculo"),
                        tipo_montagem=dados.get("tipo_montagem"),

                        data_api=dados.get("data"),
                        ultima_atualizacao=dados.get("ultima_atualizacao"),

                        logo_url=dados.get("logo"),
                        restricao1=dados.get("restricao1", {}).get("restricao"),
                        restricao2=dados.get("restricao2", {}).get("restricao"),
                        restricao3=dados.get("restricao3", {}).get("restricao"),
                        restricao4=dados.get("restricao4", {}).get("restricao"),

                        data_consulta=now()
                    )
                    return JsonResponse({'status': 'sucesso', 'placa': placa_detectada})
                else:
                    return JsonResponse({'status': 'api_falhou', 'placa': placa_detectada})
            else:
                return JsonResponse({'status': 'falha', 'erro': 'Placa não detectada'})

        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)})

    return JsonResponse({'status': 'erro', 'mensagem': 'Requisição inválida'}, status=400)

import re

def is_mercosul(placa):
    return bool(re.match(r'^[A-Z]{3}[0-9][A-Z][0-9]{2}$', placa.upper()))

@csrf_exempt
def consultar_placa_manual_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            placa_digitada = data.get('placa', '').strip().upper()

            if not placa_digitada:
                return JsonResponse({'status': 'erro', 'mensagem': 'Placa não informada'})

            dados = consultar_placa_apibrasil(placa_digitada)
            if not dados:
                return JsonResponse({'status': 'erro', 'mensagem': 'API não retornou dados'})

            # Lógica correta: usa modelo novo apenas se a placa digitada for Mercosul
            if is_mercosul(placa_digitada):
                placa_principal = dados.get("placa_modelo_novo") or dados.get("placa_nova") or placa_digitada
            else:
                placa_principal = placa_digitada

            Consulta.objects.create(
                placa=placa_principal,
                placa_modelo_antigo=dados.get("placa_modelo_antigo"),
                placa_modelo_novo=dados.get("placa_modelo_novo"),
                placa_nova=dados.get("placa_nova"),
                marca=dados.get("marca"),
                modelo=dados.get("modelo"),
                submodelo=dados.get("SUBMODELO"),
                versao=dados.get("VERSAO"),
                ano=dados.get("ano"),
                ano_modelo=dados.get("anoModelo"),
                cor=dados.get("cor_veiculo", {}).get("cor") or dados.get("cor"),
                municipio=dados.get("municipio") or dados.get("extra", {}).get("municipio", {}).get("municipio"),
                uf=dados.get("uf"),
                chassi=dados.get("extra", {}).get("chassi") or dados.get("chassi"),
                situacao_chassi=dados.get("situacao_chassi"),
                situacao_veiculo=dados.get("situacao_veiculo"),
                nacionalidade=dados.get("nacionalidade", {}).get("nacionalidade") or dados.get("extra", {}).get("nacionalidade"),
                combustivel=dados.get("combustivel") or dados.get("extra", {}).get("combustivel"),
                potencia=dados.get("potencia"),
                cilindradas=dados.get("cilindradas"),
                capacidade_carga=dados.get("capacidade_carga"),
                quantidade_passageiro=dados.get("quantidade_passageiro"),
                peso_bruto_total=dados.get("peso_bruto_total"),
                eixos=dados.get("eixos"),
                tipo_veiculo=dados.get("tipo_veiculo", {}).get("tipo_veiculo"),
                tipo_montagem=dados.get("tipo_montagem"),
                data_api=dados.get("data"),
                ultima_atualizacao=dados.get("ultima_atualizacao"),
                logo_url=dados.get("logo"),
                restricao1=dados.get("restricao1", {}).get("restricao"),
                restricao2=dados.get("restricao2", {}).get("restricao"),
                restricao3=dados.get("restricao3", {}).get("restricao"),
                restricao4=dados.get("restricao4", {}).get("restricao"),
                data_consulta=now()
            )

            return JsonResponse({'status': 'sucesso', 'dados': dados})

        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)})

    return JsonResponse({'status': 'erro', 'mensagem': 'Método inválido'}, status=400)


@require_GET
def consultar_cadastrados_view(request):
    placa = request.GET.get('placa', '').strip().upper()
    if not placa:
        return JsonResponse({'status': 'erro', 'mensagem': 'Placa não fornecida'})

    try:
        consulta = Consulta.objects.filter(placa__iexact=placa).order_by('-data_consulta').first()
        if not consulta:
            return JsonResponse({'status': 'erro', 'mensagem': 'Placa não encontrada'})

        dados = {
            "placa": consulta.placa,
            "modelo": consulta.modelo,
            "marca": consulta.marca,
            "versao": consulta.versao,
            "cor": consulta.cor,
            "ano": consulta.ano,
            "anoModelo": consulta.ano_modelo,
            "municipio": consulta.municipio,
            "uf": consulta.uf,
            "chassi": consulta.chassi,
            "combustivel": consulta.combustivel,
            "potencia": consulta.potencia,
            "cilindradas": consulta.cilindradas,
            "situacao_veiculo": consulta.situacao_veiculo,
            "nacionalidade": consulta.nacionalidade,
            "quantidade_passageiro": consulta.quantidade_passageiro,
            "peso_bruto_total": consulta.peso_bruto_total,
            "data": consulta.data_api,
            "ultima_atualizacao": consulta.ultima_atualizacao,
            "restricao1": consulta.restricao1,
            "restricao2": consulta.restricao2,
            "restricao3": consulta.restricao3,
            "restricao4": consulta.restricao4,
            "logo": consulta.logo_url
        }
        return JsonResponse({'status': 'sucesso', 'dados': dados})
    except Exception as e:
        return JsonResponse({'status': 'erro', 'mensagem': str(e)})
    
    

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator
import json

@require_http_methods(["GET"])
def listar_veiculos_view(request):
    filtro = request.GET.get('filtro', '').strip().upper()
    consultas = Consulta.objects.all().order_by('-data_consulta')

    if filtro:
        consultas = consultas.filter(placa__icontains=filtro)

    dados = []
    for c in consultas:
        dados.append({
            "id": c.id,
            "placa": c.placa,
            "modelo": c.modelo,
            "marca": c.marca,
            "versao": c.versao,
            "ano": c.ano,
            "cor": c.cor,
            "municipio": c.municipio,
            "uf": c.uf,
            "chassi": c.chassi,
            "combustivel": c.combustivel,
            "potencia": c.potencia,
            "cilindradas": c.cilindradas,
            "capacidade_carga": c.capacidade_carga,
            "quantidade_passageiro": c.quantidade_passageiro,
            "peso_bruto_total": c.peso_bruto_total,
            "situacao": c.situacao_veiculo,
            "data": c.data_consulta.strftime('%d/%m/%Y %H:%M'),
            "data_api": c.data_api.strftime('%d/%m/%Y %H:%M') if hasattr(c.data_api, 'strftime') else c.data_api or ""
        })

    return JsonResponse({
        "total": len(dados),
        "dados": dados
    })


    return JsonResponse({
        "total": len(dados),
        "dados": dados
    })



@csrf_exempt
@require_http_methods(["PUT"])
def editar_veiculo_view(request, id):
    try:
        consulta = Consulta.objects.get(id=id)
        dados = json.loads(request.body)

        consulta.placa = dados.get("placa", consulta.placa)
        consulta.modelo = dados.get("modelo", consulta.modelo)
        consulta.marca = dados.get("marca", consulta.marca)
        consulta.cor = dados.get("cor", consulta.cor)
        consulta.ano = dados.get("ano", consulta.ano)
        consulta.municipio = dados.get("municipio", consulta.municipio)
        consulta.situacao_veiculo = dados.get("situacao", consulta.situacao_veiculo)
        consulta.save()

        return JsonResponse({"status": "sucesso"})

    except Consulta.DoesNotExist:
        return JsonResponse({"status": "erro", "mensagem": "Veículo não encontrado"}, status=404)

    except Exception as e:
        return JsonResponse({"status": "erro", "mensagem": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def excluir_veiculo_view(request, id):
    try:
        consulta = Consulta.objects.get(id=id)
        consulta.delete()
        return JsonResponse({"status": "sucesso"})

    except Consulta.DoesNotExist:
        return JsonResponse({"status": "erro", "mensagem": "Veículo não encontrado"}, status=404)

    except Exception as e:
        return JsonResponse({"status": "erro", "mensagem": str(e)}, status=500)


def veiculos_gerenciar_view(request):
    return render(request, 'placas/veiculos_gerenciar.html')

