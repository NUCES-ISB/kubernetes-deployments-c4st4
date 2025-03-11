from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Define storage file in persistent volume
STORAGE_DIR = "/app-data"
STORAGE_FILE = os.path.join(STORAGE_DIR, "messages.txt")

# Ensure storage directory exists
os.makedirs(STORAGE_DIR, exist_ok=True)

# Function to read stored messages
def read_messages():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as file:
            return file.readlines()
    return []

# Function to save messages
def save_message(message):
    with open(STORAGE_FILE, "a") as file:
        file.write(message + "\n")

@app.route('/')
def home():
    return """
    <h1>Simple Messaging App (Persistent Storage)</h1>
    <p>Use /add?msg=yourmessage to add a message</p>
    <p>Use /messages to view stored messages</p>
    """

@app.route('/add', methods=['GET'])
def add_message():
    message = request.args.get("msg", "")
    if message:
        save_message(message)
        return jsonify({"message": "Message saved!", "content": message}), 200
    return jsonify({"error": "No message provided"}), 400

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = read_messages()
    return jsonify({"messages": messages}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
