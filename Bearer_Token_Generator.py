import os
import requests
from dotenv import load_dotenv

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

        print("\n✅ Dados retornados da API Brasil:\n")
        for chave, valor in data.items():
            print(f"{chave}: {valor}")
        return data
    except Exception as e:
        print("\n❌ Erro ao consultar a placa:", e)

if __name__ == "__main__":
    gerar_bearer_token()
