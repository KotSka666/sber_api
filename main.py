import requests


client_id = "13699"
client_secret = "SAND68495PILE"


cert_path = r"C:\lesson_Un\Sber_API\sberapi-ca.cer"


auth_response = requests.post(
    url="https://auth.sberbank.ru/oauth/token",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    },
    cert=(cert_path, None)  # Указали путь до сертификата и приватного ключа (None, если нет ключа)
)

if auth_response.status_code != 200:
    raise Exception(f"Ошибка получения временного кода авторизации: {auth_response.text}")

temp_auth_code = auth_response.json().get("code")
print(f"Временный код авторизации: {temp_auth_code}")


redirect_uri = "http://localhost:8000/callback"

token_response = requests.post(
    url="https://auth.sberbank.ru/oauth/token",
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    data={
        "code": temp_auth_code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
)

if token_response.status_code != 200:
    raise Exception(f"Ошибка получения токена доступа: {token_response.text}")

access_token = token_response.json().get("access_token")
print(f"Токен доступа: {access_token}")


api_endpoint = "https://sandbox.sberbank.ru/api/v1/accounts"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response = requests.get(api_endpoint, headers=headers)

if response.status_code == 200:
    accounts_data = response.json()
    print("Информация о ваших счетах:")
    print(accounts_data)
else:
    print(f"Произошла ошибка при получении информации о счетах: {response.status_code}")