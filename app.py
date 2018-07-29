from flask import Flask, request
import os, sys
from pymessenger import Bot

app = Flask(__name__)


PAGE_ACCESS_TOKEN = "EAAcgY40xQYIBAGcc34hfhTZCRy0bTZBGQ9ACmNgm8W6DZCqdgWHom06TnjEcjLHNlqVOmIwFHpHj5R0gdKw6WCAg8pHYV7h9QmckZAvd9foxXO1ZCZCj5NU6HYj5GuwVknwmJTIRVtiRtTq7OnrA1NeLaYr8ZCz8t0hbyWXf1AM46UXz47upMX7"

bot =Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "hello":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world", 200

@app.route('/', methods = ['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    #ECHO
                    response = messaging_text

                    bot.send_text_message(sender_id,response)    

    return "ok" , 200

def log(message):
    print(message)
    sys.stdout.flush()

if __name__ == "__main__":
	app.run(debug = True, port = 80)
