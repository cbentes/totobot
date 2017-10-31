import requests


class LUIS:

    def __init__(self, luis_app_chain, luis_sub_key):
        self.luis_app_chain = luis_app_chain
        self.luis_sub_key = luis_sub_key

    def query(self, text):
        resp_list = []
        # Query all apps in the app chain
        for luis_app_ip in self.luis_app_chain:
            luis_url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/{0}".format(luis_app_ip)
            params = dict()
            params['subscription-key'] = self.luis_sub_key
            params['q'] = text
            params['verbose'] = True
            resp = requests.get(luis_url, params=params)
            resp_list.append(resp.json())
        return resp_list
