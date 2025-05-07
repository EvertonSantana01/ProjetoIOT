import os
import requests
from dotenv import load_dotenv
import json
from tabulate import tabulate
from fpdf import FPDF

load_dotenv()

def gerar_bearer_token():
    bearer = os.getenv("API_BRASIL_TOKEN")
    device = os.getenv("API_BRASIL_DEVICE_TOKEN")
    placa = input("Digite a placa do veículo: ").strip().upper()

    headers = {
        "Authorization": f"Bearer {bearer}",
        "DeviceToken": device,
        "Content-Type": "application/json"
    }

    payload = { "placa": placa }

    try:
        response = requests.post("https://gateway.apibrasil.io/api/v2/vehicles/dados", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        print("\n✅ Dados retornados da API Brasil (Organizados em Tabelas):\n")
        exibir_tabelas_terminal(data)
        return data, placa  # Retorna os dados e a placa
    except requests.exceptions.RequestException as e:
        print("\n❌ Erro ao consultar a placa:", e)
        return None, None
    except json.JSONDecodeError as e:
        print("\n❌ Erro ao decodificar a resposta JSON:", e)
        return None, None
    except Exception as e:
        print("\n❌ Erro inesperado:", e)
        return None, None

def exibir_tabelas_terminal(data):
    if 'response' in data and not data.get('error'):
        response_data = data['response']

        # Tabela 1: Status da Requisição
        status_data = {"Campo": ["error", "message", "Status Code"],
                       "Valor": [data.get('error'), data.get('message'), data.get('status_code')]}
        print("Tabela 1: Status da Requisição")
        print(tabulate(status_data, headers="keys", tablefmt="grid"))
        print("\n")

        # Tabela 2: Dados do Veículo (Principais)
        principais_campos = ["MARCA", "MODELO", "SUBMODELO", "VERSAO", "ano", "anoModelo", "chassi", "codigoRetorno", "codigoSituacao", "cor", "data", "placa", "placa_modelo_antigo", "placa_modelo_novo", "placa_nova", "municipio", "uf", "uf_placa", "combustivel", "potencia", "capacidade_carga", "nacionalidade", "linha", "carroceria", "caixa_cambio", "eixos", "tipo_veiculo", "situacao_chassi", "tipo_montagem", "ultima_atualizacao", "cilindradas", "situacao_veiculo"]
        principais_data = {"Campo": [], "Valor": []}
        for campo in principais_campos:
            if campo in response_data:
                principais_data["Campo"].append(campo)
                principais_data["Valor"].append(response_data[campo])
        print("Tabela 2: Dados do Veículo (Principais)")
        print(tabulate(principais_data, headers="keys", tablefmt="grid"))
        print("\n")

        # Tabela 3: Dados Extras
        extra_data_dict = response_data.get('extra', {})
        extra_campos = ["ano_fabricacao", "chassi", "cor_veiculo", "faturado", "tipo_doc_faturado", "uf_faturado", "tipo_doc_prop", "motor", "municipio", "peso_bruto_total", "marca_modelo", "restricao1", "restricao2", "restricao3", "restricao4"]
        extra_data = {"Campo": [], "Valor": []}
        for campo in extra_campos:
            if campo in extra_data_dict:
                extra_data["Campo"].append(campo)
                extra_data["Valor"].append(extra_data_dict[campo])
        print("Tabela 3: Dados Extras")
        print(tabulate(extra_data, headers="keys", tablefmt="grid"))
        print("\n")

        # Tabela 4: Informações da API
        api_info_campos = ["listamodelo", "server", "version", "info", "logo"]
        api_info_data = {"Campo": [], "Valor": []}
        for campo in api_info_campos:
            if campo in data:
                api_info_data["Campo"].append(campo)
                api_info_data["Valor"].append(data[campo])
        print("Tabela 4: Informações da API")
        print(tabulate(api_info_data, headers="keys", tablefmt="grid"))
        print("\n")

        # Tabela 5: Limites da API
        limites_data = {"Campo": ["api_limit", "api_limit_for", "api_limit_used"],
                        "Valor": [data.get('api_limit'), data.get('api_limit_for'), data.get('api_limit_used')]}
        print("Tabela 5: Limites da API")
        print(tabulate(limites_data, headers="keys", tablefmt="grid"))
        print("\n")

        # Tabela 6: FIPE e Multas
        fipe_multas_data = {"Campo": ["fipe", "multas"],
                            "Valor": [response_data.get('fipe'), response_data.get('multas')]}
        print("Tabela 6: FIPE e Multas")
        print(tabulate(fipe_multas_data, headers="keys", tablefmt="grid"))
        print("\n")
    else:
        print("❌ Não há dados válidos para exibir em tabelas.")

def exportar_para_pdf(data, placa, diretorio_salvamento="pdf"):
    if not os.path.exists(diretorio_salvamento):
        os.makedirs(diretorio_salvamento)

    nome_arquivo = f"{placa}.pdf"
    caminho_completo = os.path.join(diretorio_salvamento, nome_arquivo)

    if 'response' in data and not data.get('error'):
        response_data = data['response']

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        def adicionar_tabela_pdf(titulo, data_dict):
            pdf.set_font("Arial", 'B', size=12)
            pdf.cell(0, 10, titulo, ln=True)
            pdf.set_font("Arial", size=10)
            for campo, valor in data_dict.items():
                pdf.cell(50, 5, txt=f"{campo}:")
                pdf.multi_cell(0, 5, txt=str(valor), ln=True)
            pdf.ln(5)

        # Tabela 1: Status da Requisição
        status_data = {"error": data.get('error'), "message": data.get('message'), "Status Code": data.get('status_code')}
        adicionar_tabela_pdf("Status da Requisição", status_data)

        # Tabela 2: Dados do Veículo (Principais)
        principais_campos = ["MARCA", "MODELO", "SUBMODELO", "VERSAO", "ano", "anoModelo", "chassi", "codigoRetorno", "codigoSituacao", "cor", "data", "placa", "placa_modelo_antigo", "placa_modelo_novo", "placa_nova", "municipio", "uf", "uf_placa", "combustivel", "potencia", "capacidade_carga", "nacionalidade", "linha", "carroceria", "caixa_cambio", "eixos", "tipo_veiculo", "situacao_chassi", "tipo_montagem", "ultima_atualizacao", "cilindradas", "situacao_veiculo"]
        principais_data = {campo: response_data.get(campo) for campo in principais_campos if campo in response_data}
        adicionar_tabela_pdf("Dados do Veículo (Principais)", principais_data)

        # Tabela 3: Dados Extras
        extra_data_dict = response_data.get('extra', {})
        extra_campos = ["ano_fabricacao", "chassi", "cor_veiculo", "faturado", "tipo_doc_faturado", "uf_faturado", "tipo_doc_prop", "motor", "municipio", "peso_bruto_total", "marca_modelo", "restricao1", "restricao2", "restricao3", "restricao4"]
        extra_data = {campo: extra_data_dict.get(campo) for campo in extra_campos if campo in extra_data_dict}
        adicionar_tabela_pdf("Dados Extras", extra_data)

        # Tabela 4: Informações da API
        api_info_campos = ["listamodelo", "server", "version", "info", "logo"]
        api_info_data = {campo: data.get(campo) for campo in api_info_campos if campo in data}
        adicionar_tabela_pdf("Informações da API", api_info_data)

        # Tabela 5: Limites da API
        limites_data = {"api_limit": data.get('api_limit'), "api_limit_for": data.get('api_limit_for'), "api_limit_used": data.get('api_limit_used')}
        adicionar_tabela_pdf("Limites da API", limites_data)

        # Tabela 6: FIPE e Multas
        fipe_multas_data = {"fipe": response_data.get('fipe'), "multas": response_data.get('multas')}
        adicionar_tabela_pdf("FIPE e Multas", fipe_multas_data)

        try:
            pdf.output(caminho_completo, "F")
            print(f"\n✅ Dados exportados para: {caminho_completo}")
        except Exception as e:
            print(f"\n❌ Erro ao salvar o PDF em '{caminho_completo}': {e}")
    else:
        print("\n❌ Não há dados válidos para exportar para PDF.")

if __name__ == "__main__":
    diretorio_inicial = os.getcwd()
    dados, placa_veiculo = gerar_bearer_token()
    if dados:
        exportar_para_pdf(dados, placa_veiculo)

    try:
        os.chdir(diretorio_inicial)
        print(f"\n✅ Terminal retornado ao diretório: {diretorio_inicial}")
    except Exception as e:
        print(f"\n❌ Erro ao retornar ao diretório inicial: {e}")