import requests
import pytest

class TestUserAuth:
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        self.response_login = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        self.auth_sid = self.response_login.cookies.get('auth_sid')
        self.token = self.response_login.headers.get('x-csrf-token')
        self.user_id_from_auth_method = self.response_login.json()['user_id']

    def test_login_user(self):

        assert 'auth_sid' in self.response_login.cookies, 'There is no auth cookie in the reponse'
        assert 'x-csrf-token' in self.response_login.headers, 'There is no CSRF token header in the response'
        assert 'user_id' in self.response_login.json(), 'There is no user id in the response'

    def test_auth_login(self):

        response_auth = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers={'x-csrf-token':self.token},
            cookies={'auth_sid':self.auth_sid}
        )

        response_auth_json = response_auth.json()
        user_id_from_check_method = response_auth_json['user_id']

        assert 'user_id' in response_auth_json, 'There is no user id in the second response'
        assert self.user_id_from_auth_method == user_id_from_check_method, f"User {self.user_id_from_auth_method} not equals user {user_id_from_check_method}"

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == "no_cookie":
            response_auth = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                headers={'x-csrf-token': self.token}
            )
        else:
            response_auth = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                cookies={'auth_sid':self.auth_sid}
            )

        assert "user_id" in self.response_login.json(), "There is no user id in the response_auth response"
        assert response_auth.json()["user_id"] == 0, f"User is authorized with condition {condition}"