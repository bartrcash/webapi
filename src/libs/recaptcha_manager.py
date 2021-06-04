import requests

# flask
from flask import request


class RecaptchaManager:
    @classmethod
    def verify_recaptcha(cls, token):
        recaptcha_url = "https://www.google.com/recaptcha/api/siteverify"
        recaptcha_secret_key = "6LeLoAgbAAAAALcGYpCQiYh-c1xKLtcKC4CkrnvP"
        payload = {
            "secret": recaptcha_secret_key,
            "response": token,
            "remoteip": request.remote_addr,
        }
        response = requests.post(recaptcha_url, data=payload)
        result = response.json()

        return result.get("success", None)
