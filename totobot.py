import os

from flask import Flask
from flask import request
from flask import abort

import totobot
from totobot.bot_manager import BotFramework
from totobot.luis_manager import LUIS
from totobot.config_manager import ConfigurationManager
from totobot.data_manager import DataManager

MONGODB_USER = os.environ["MONGODB_USER"]
MONGODB_PWD = os.environ["MONGODB_PWD"]
MONGODB_HOST = os.getenv("MONGODB_HOST", '127.0.0.1')
MONGODB_PORT = os.getenv("MONGODB_HOST", '27017')

TOTOBOT_DEBUG = os.getenv("TOTOBOT_DEBUG", False)
TOTOBOT_PORT = os.getenv("TOTOBOT_PORT", 5000)
TOTOBOT_HOST = os.getenv("TOTOBOT_HOST", "127.0.0.1")

data_manager = DataManager(MONGODB_USER, MONGODB_PWD)
cm = ConfigurationManager()
bf = BotFramework(cm.MICROSOFT_APP_ID, cm.MICROSOFT_APP_PASSWORD)
luis = LUIS(cm.LUIS_APP_CHAIN, cm.LUIS_SUB_KEY)

app = Flask(__name__)


@app.route("/")
def hello():
    return "Totobot {0}".format(totobot.__version__)


@app.route("/<k>/api/messages", methods=['POST'])
def api_messaages(k):

    if k != cm.TOTOBOT_KEY:
        abort(403)

    bc_token = request.headers.get('Authorization', 'No')
    if not bf.authenticate_bot_connector(bc_token):
        abort(403)

    data = request.json
    data_manager.log_data(data, 'request_json')

    for k in data:
        print('{0} = {1}'.format(k, data[k]))

    if 'text' in data:
        text = data['text']

        reply_context = {
            'serviceUrl': data['serviceUrl'],
            'msg_id': data['id'],
            "type": data['type'],
            "from": data['recipient'],
            "conversation": data['conversation'],
            "recipient": data['from'],
            'conversation_id': data['conversation']['id']
        }

        # Test: get the intent and send it back to the user
        luis_resp_list = luis.query(text)
        data_manager.log_data(luis_resp_list, 'luis_response')
        intents = []
        for luis_resp in luis_resp_list:
            intents += [x['intent'] for x in luis_resp['intents']]
        reply_msg = "<br/>".join(intents)
        bf.send(reply_context, reply_msg)
        data_manager.log_data({'reply_context': reply_context, 'reply_msg': reply_msg}, 'totobot_reply')

    return ''

if __name__ == "__main__":
    app.run(debug=TOTOBOT_DEBUG, host=TOTOBOT_HOST, port=TOTOBOT_PORT)
