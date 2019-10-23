import requests
from decouple import config

google_key = config("GOOGLE_API_KEY")
api_url = "https://translation.googleapis.com/language/translate/v2"

data = {
    "q": "안녕하세요",
    "source": "ko",
    "target": "en"
}

response = requests.post(f'{api_url}?key={google_key}', data).json()
print(response)