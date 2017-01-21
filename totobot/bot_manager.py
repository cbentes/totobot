import requests
import datetime
import time


class BotFramework:

    def __init__(self, ms_app_id, ms_app_password):
        self.ms_app_id = ms_app_id
        self.ms_app_password = ms_app_password
        self.token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        self.scope_url = "https://graph.microsoft.com/.default"
        self.expiration_time = 0
        self.token_type = ''
        self.access_token = ''

    def _check_token(self, force_renew=False):
        if time.time() > self.expiration_time or force_renew:
            data = {"grant_type": "client_credentials",
                    "client_id": self.ms_app_id,
                    "client_secret": self.ms_app_password,
                    "scope": self.scope_url
                    }
            self.expiration_time = time.time()
            response = requests.post(self.token_url, data)
            resp = response.json()
            self.access_token = resp['access_token']
            self.token_type = resp['token_type']
            self.expiration_time += resp['expires_in']

    def send(self, context, text):
        self._check_token()
        data = dict(context)
        data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ")
        data['text'] = text
        data['replyToId'] = {'id': context['conversation_id']}
        service_url = context['serviceUrl']
        msg_id = context['msg_id']
        conversation_id = context['conversation_id']
        response_url = '{0}/v3/conversations/{1}/activities/{2}'.format(service_url, conversation_id, msg_id)
        authorization = '{0} {1}'.format(self.token_type, self.access_token)
        resp = requests.post(response_url, json=data, headers={"Authorization": authorization})
        return resp
