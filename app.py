import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    """A simple route to confirm the app is running."""
    return "Flask webhook listener is active!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """This is the endpoint that receives the webhook."""
    if request.is_json:
        data = request.get_json()
        print("Webhook received:")
        print(data)
        # Add your processing logic here
        return jsonify({"status": "success", "data_received": data}), 200
    else:
        return jsonify({"status": "error", "message": "Request was not JSON"}), 400

if __name__ == '__main__':
    # Railway provides the PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    # Running on 0.0.0.0 is important to be accessible externally
    app.run(host='0.0.0.0', port=port)
