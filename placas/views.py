import os
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Consulta
from .detector.detector import detectar_placa
from .api_brasil import consultar_placa_apibrasil
from django.utils.timezone import now
import base64, json, cv2, numpy as np

from .models import Consulta
from .detector.detector import detectar_placa
from .api_brasil import consultar_placa_apibrasil

def camera_view(request):
    return render(request, 'placas/dashboard.html')

from django.http import JsonResponse
from .models import Consulta

def ultima_consulta_json(request):
    ultima = Consulta.objects.order_by('-data_consulta').first()
    historico = Consulta.objects.order_by('-data_consulta')[:10]

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

            placa = detectar_placa(frame)

            if placa:
                dados = consultar_placa_apibrasil(placa)

                if dados:
                    Consulta.objects.create(
                        placa=dados.get("placa"),
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
                    return JsonResponse({'status': 'sucesso', 'placa': placa})
                else:
                    return JsonResponse({'status': 'api_falhou', 'placa': placa})
            else:
                return JsonResponse({'status': 'falha', 'erro': 'Placa não detectada'})

        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)})

    return JsonResponse({'status': 'erro', 'mensagem': 'Requisição inválida'}, status=400)
