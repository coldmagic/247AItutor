from flask import Flask, render_template, request, jsonify
import openai
import json
import os

app = Flask(__name__)

# Replace 'your_openai_api_key' with your actual OpenAI API key
openai.api_key = os.environ.get("openai_api")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    subject = data.get('subject')
    message = data.get('message')

    ai_response = get_ai_response(subject, message)

    return jsonify({'response': ai_response})

def get_ai_response(subject, message):
    messages = [
        {"role": "system", "content": f"You are an AI expert in {subject}."},
        {"role": "user", "content": message}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response_text = response.choices[0].message.content.strip()
    return response_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
