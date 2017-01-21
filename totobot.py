
from flask import Flask
from flask import request
from flask import abort

import totobot
from totobot.bot_manager import BotFramework
from totobot.luis_manager import LUIS
import os


MICROSOFT_APP_ID = os.environ['MICROSOFT_APP_ID']
MICROSOFT_APP_PASSWORD = os.environ['MICROSOFT_APP_PASSWORD']
LUIS_APP_ID = os.environ['LUIS_APP_ID']
LUIS_SUB_KEY = os.environ['LUIS_SUB_KEY']
TOTOBOT_KEY = os.environ['TOTOBOT_KEY']

bf = BotFramework(MICROSOFT_APP_ID, MICROSOFT_APP_PASSWORD)
app = Flask(__name__)

luis = LUIS(LUIS_APP_ID, LUIS_SUB_KEY)


@app.route("/")
def hello():
    return "Totobot {0}".format(totobot.__version__)


@app.route("/<k>/api/messages", methods=['POST'])
def api_messaages(k):

    if k != TOTOBOT_KEY:
        abort(403)

    bc_token = request.headers.get('Authorization', 'No')
    if not bf.authenticate_bot_connector(bc_token):
        abort(403)

    data = request.json

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
        luis_resp = luis.query(text)
        intent = luis_resp['topScoringIntent']['intent']
        reply_msg = "Intent: {0}".format(intent)
        bf.send(reply_context, reply_msg)

    return ''

if __name__ == "__main__":
    app.run(debug=False)
