import requests


class LUIS:

    def __init__(self, luis_app_id, luis_sub_key):
        self.luis_app_ip = luis_app_id
        self.luis_sub_key = luis_sub_key

    def query(self, text):
        luis_url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/{0}".format(self.luis_app_ip)
        params = {}
        params['subscription-key'] = self.luis_sub_key
        params['q'] = text
        resp = requests.get(luis_url, params=params)
        return resp.json()
