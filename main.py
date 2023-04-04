# main.py
from flask import Flask, render_template, request, jsonify
from server.chat_gpt import ask_kate

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    subject = data.get('subject')
    message = data.get('message')

    ai_response = ask_kate(message)

    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
