import requests
import pytest

class TestFirstAPI:
    names = [
        ("Vitalii"),
        ("Arseniy"),
        ("")
    ]

    @pytest.mark.parametrize("name", names)
    def test_hello_call(self, name):
        url = "https://playground.learnqa.ru/api/hello"
        data = {"name": name}

        response_hello = requests.get(url, params=data)
        assert response_hello.status_code == 200, "Wrong response code"

        response_hello_dict = response_hello.json()
        assert "answer" in response_hello_dict, "There is no 'answer' in the response"

        if len(name) == 0:
            expect_response_text = "Hello, someone"
        else:
            expect_response_text = f"Hello, {name}"

        actual_response_text = response_hello_dict["answer"]
        assert actual_response_text == expect_response_text, "Actual text in the response is not correct"