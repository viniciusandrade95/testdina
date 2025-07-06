import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the Verify Token from Railway's environment variables
VERIFY_TOKEN = os.environ.get('WHATSAPP_VERIFY_TOKEN')

@app.route('/')
def home():
    """A simple route to confirm the app is running."""
    return "WhatsApp webhook listener is active!"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """
    This endpoint handles both webhook verification (GET) and
    event notifications (POST) from WhatsApp.
    """
    # ADD THIS LINE FOR DEBUGGING
    print(f"Token loaded from environment: '{VERIFY_TOKEN}'")

    if request.method == 'GET':
        # This is the verification request from WhatsApp
        if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
            # Respond with the challenge token from the request
            challenge = request.args.get("hub.challenge")
            print("WEBHOOK_VERIFIED")
            return challenge, 200
        else:
            # Respond with '403 Forbidden' if tokens do not match
            print("VERIFICATION_FAILED")
            return "Verification token mismatch", 403

    if request.method == 'POST':
        # ... (the rest of the code is unchanged) ...
        data = request.get_json()
        print("Webhook received:")
        print(data) 

        if data.get('object') == 'whatsapp_business_account':
            try:
                for entry in data.get('entry', []):
                    for change in entry.get('changes', []):
                        value = change.get('value', {})
                        if 'messages' in value:
                            for message in value.get('messages', []):
                                phone_number = message.get('from')
                                message_body = message.get('text', {}).get('body')
                                print(f"From: {phone_number}, Message: {message_body}")
            except Exception as e:
                print(f"Error processing webhook: {e}")

        return jsonify({"status": "success"}), 200

    return "Method Not Allowed", 405

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
