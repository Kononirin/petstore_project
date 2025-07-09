import requests
import pytest

class TestUserAuth:
    def response_login(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        return response_login

    def test_login_user(self):
        response_login = self.response_login()

        assert 'auth_sid' in response_login.cookies, 'There is no auth cookie in the reponse'
        assert 'x-csrf-token' in response_login.headers, 'There is no CSRF token header in the response'
        assert 'user_id' in response_login.json(), 'There is no user id in the response'

    def test_auth_login(self):
        response_login = self.response_login()

        auth_sid = response_login.cookies.get('auth_sid')
        token = response_login.headers.get('x-csrf-token')
        user_id_from_auth_method = response_login.json()['user_id']

        response_auth = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={'x-csrf-token':token},
            cookies={'auth_sid':auth_sid}
        )

        response_auth_json = response_auth.json()
        user_id_from_check_method = response_auth_json['user_id']

        assert 'user_id' in response_auth_json, 'There is no user id in the second response'

        assert user_id_from_auth_method == user_id_from_check_method, f"User {user_id_from_auth_method} not equals user {user_id_from_check_method}"

    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        response_login = self.response_login()

        auth_sid = response_login.cookies.get('auth_sid')
        token = response_login.headers.get('x-csrf-token')

        if condition == "no_cookie":
            response_auth = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                headers={'x-csrf-token': token}
            )
        else:
            response_auth = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                cookies={'auth_sid':auth_sid}
            )

        assert "user_id" in response_login.json(), "There is no user id in the response_auth response"

        user_id_from_check_method = response_auth.json()["user_id"]

        assert user_id_from_check_method == 0, f"User is authorized with condition {condition}"


