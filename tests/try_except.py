from json.decoder import JSONDecodeError
import requests

response_get_text = requests.get("https://playground.learnqa.ru/api/get_text")
print(response_get_text.text)

try:
    parsed_response_text = response_get_text.json()
    print(parsed_response_text)
except JSONDecodeError:
    print("Response is not a JSON format")