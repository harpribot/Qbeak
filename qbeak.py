import config
import json
from flask import Flask, request
import os
from src.utils.log import log
from src.utils.handlers import handle_message
from src.utils.feedback import about_response

VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', config.VERIFY_TOKEN)

app = Flask(__name__)


@app.route('/')
def info():
    """
    Displays on the website of the page.

    :return: response for each get request on '/'.
    """
    return about_response()


@app.route('/webhook/', methods=['GET', 'POST'])
def webhook():
    """
    Triggers on each GET and POST request. Handles GET and POST requests using this function.

    :return: Return status code acknowledge for the GET and POST request
    """
    if request.method == 'POST':
        data = request.get_json(force=True)
        log(json.dumps(data))  # you may not want to log every incoming message in production, but it's good for testing

        if data["object"] == "page":
            for entry in data["entry"]:
                for event in entry["messaging"]:
                    sender_id = event["sender"]["id"]

                    if 'message' in event and 'text' in event['message']:
                        message_text = event["message"]["text"]
                        if event.get("message").get("quick_reply"):
                            feedback_payload = event["message"]["quick_reply"]["payload"]
                            handle_message(feedback_payload, sender_id, message_type="feedback")
                        else:
                            handle_message(message_text, sender_id)

                    if 'postback' in event and 'payload' in event['postback']:
                        postback_payload = event['postback']['payload']
                        log(postback_payload)
                        handle_message(postback_payload, sender_id, message_type="feedback")

                    if event.get("delivery"):
                        pass

                    if event.get("optin"):
                        pass

        return "ok", 200

    elif request.method == 'GET':  # Verification
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get('hub.challenge'), 200
        else:
            return 'Error, wrong validation token', 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
