import requests

# response = requests.post("https://playground.learnqa.ru/api/get_301", allow_redirects=True)
#
# first_response = response.history[0]
# second_response = response
#
# print(first_response.url)
# print(second_response.url)

# headers = {"some_header":"123"}
# resonse = requests.get("https://playground.learnqa.ru/api/show_all_headers", headers=headers)
#
# print(response.text)
# print(response.headers)

payload = {"login":"secret_login", "password":"secret_pass2"}
response1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)

cookie_value = response1.cookies.get('auth_cookie')
cookies = {}
if cookie_value is not None:
    cookies.update( {'auth_cookie': cookie_value})

response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies = cookies)

print(response2.text)
