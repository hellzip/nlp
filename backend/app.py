from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import requests
import ai_model
from db import db

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/nlp_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from models import UserInteraction

def load_dataset():
    df = pd.read_csv('D:/University/SEM 4/Natural Language Processing/Assignment 2/backend/data/gen_zz_words.csv')
    data = {}
    for _, row in df.iterrows():
        data[row['Word/Phrase'].lower()] = {
            'definition': row['Definition'],
            'example': row['Example Sentence'],
            'popularity': row['Popularity/Trend Level']
        }
    return data

slang_data = load_dataset()

def get_chatgpt_response(user_input):
    api_key = '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'
    api_url = 'https://api.openai.com/v1/chat/completions'
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': user_input}],
        'max_tokens': 150,
        'temperature': 0.7,
    }
    
    response = requests.post(api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        return "Sorry, I couldn't process that."

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    print(f"User Input: {user_input}")  
    ai_response = ai_model.get_response(user_input, slang_data)
    print(f"Response from Slang Data: {ai_response}") 

    if "Sorry" in ai_response:
        ai_response = get_chatgpt_response(user_input)
        print(f"Response from ChatGPT: {ai_response}") 
    interaction = UserInteraction(user_message=user_input, bot_message=ai_response)
    db.session.add(interaction)
    db.session.commit()
    
    return jsonify({'response': ai_response})


@app.route('/api/train', methods=['POST'])
def train():
    data = UserInteraction.query.all()
    messages = [(interaction.user_message, interaction.bot_message) for interaction in data]
    
    result = ai_model.train(messages)
    
    return jsonify({'status': result})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
