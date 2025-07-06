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
        # This is an event notification from WhatsApp
        data = request.get_json()
        print("Webhook received:")
        print(data) # Log the full payload to see its structure

        # Here, you would add your logic to process the WhatsApp message
        # For example, check for 'messages' in the payload
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

    # If the request is not GET or POST
    return "Method Not Allowed", 405

if __name__ == '__main__':
    # Railway provides the PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    # Running on 0.0.0.0 is important to be accessible externally
    app.run(host='0.0.0.0', port=port)
