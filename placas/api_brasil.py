import os
import requests
from dotenv import load_dotenv

load_dotenv()

def consultar_placa_apibrasil(placa):
    bearer = os.getenv("API_BRASIL_TOKEN")
    device = os.getenv("API_BRASIL_DEVICE_TOKEN")

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

        if data.get("error") is False and "response" in data:
            return data["response"]
        else:
            print("⚠️ Placa não encontrada ou erro na API.")
            return None

    except Exception as e:
        print(f"❌ Erro na consulta API Brasil: {e}")
        return None
