import requests
import datetime
import time

import jwt


class BotFramework:

    def __init__(self, ms_app_id, ms_app_password):
        self.ms_app_id = ms_app_id
        self.ms_app_password = ms_app_password
        self.token_url = "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token"
        self.scope_url = "https://api.botframework.com/.default"

        self.expiration_time = 0
        self.token_type = ''
        self.access_token = ''

    def _check_token(self, force_renew=False):
        # Get JWT token from MSA/AAD v2
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

    def authenticate_bot_connector(self, bc_token):
        # Authenticates the JWT token that was signed by the Bot Connector
        bc_token_parts = bc_token.split()
        # Verify Authorization header with “Bearer” scheme
        if bc_token_parts[0] != 'Bearer' or len(bc_token_parts) != 2:
            return False
        jwt_token = bc_token_parts[1]
        payload = jwt.decode(jwt_token, verify=False)
        # Verify issuer claim
        iss = payload['iss']
        if iss != 'https://api.botframework.com':
            return False
        # Verify Microsoft App ID
        aud = payload['aud']
        if aud != self.ms_app_id:
            return False
        # Verify token has not yet expired
        exp_time = int(payload['exp'])
        l5_time = int(time.time()) - 300
        if exp_time < l5_time:
            return False
        return True

    def send(self, context, text):
        self._check_token()
        data = dict(context)
        data['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%zZ")
        data['text'] = text
        data['replyToId'] = context['conversation_id']
        service_url = context['serviceUrl']
        msg_id = context['msg_id']
        conversation_id = context['conversation_id']
        response_url = '{0}/v3/conversations/{1}/activities/{2}'.format(service_url, conversation_id, msg_id)
        authorization = '{0} {1}'.format(self.token_type, self.access_token)
        resp = requests.post(response_url, json=data, headers={"Authorization": authorization})
        return resp
