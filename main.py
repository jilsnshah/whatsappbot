from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os
app = Flask(__name__)

TOGETHER_API_KEY = os.environ.get("TOGETHER_API_KEY")


def generate_reply_with_together(user_input):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [{"role": "user", "content": user_input}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "Sorry, something went wrong with the AI."

# ✅ This is what Twilio will call
@app.route("/whatsapp", methods=["POST", "GET"])
def whatsapp_reply():
    if request.method == "GET":
        return "✅ WhatsApp bot is running"

    incoming_msg = request.values.get('Body', '').strip()
    print(f"Incoming: {incoming_msg}")

    reply = generate_reply_with_together(incoming_msg)

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
