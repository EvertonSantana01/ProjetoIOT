import requests

# 👉 Substitua pelo seu e-mail e senha cadastrados no site da API Brasil
EMAIL = "adersan@hotmail.com"
SENHA = "151214Aderval@"

def gerar_bearer_token(email, senha):
    url = "https://gateway.apibrasil.io/api/v2/auth/login"
    headers = { "Content-Type": "application/json" }
    payload = {
        "email": email,
        "password": senha
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        token = data.get("authorization", {}).get("token")
        if token:
            print("✅ Bearer Token gerado com sucesso:\n")
            print(token)
            return token
        else:
            print("⚠️ Token não encontrado na resposta:")
            print(data)

    except requests.exceptions.HTTPError as err:
        print("❌ Erro HTTP:", err)
        print("Resposta:", response.text)
    except Exception as e:
        print("❌ Erro geral:", e)

# Chamada
gerar_bearer_token(EMAIL, SENHA)
