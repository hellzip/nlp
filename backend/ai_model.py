import pandas as pd
from models import SlangWord
import db as db

slang_data = {}

conversation_data = []

def load_dataset():
    df = pd.read_csv('gen_zz_words.csv')
    data = {}
    for _, row in df.iterrows():
        data[row['Word/Phrase'].lower()] = {
            'definition': row['Definition'],
            'example': row['Example Sentence'],
            'popularity': row['Popularity/Trend']
        }
    return data

def get_response(user_input, slang_data):
    user_input_lower = user_input.lower()
    
    if user_input_lower in slang_data:
        slang_info = slang_data[user_input_lower]
        return f"{slang_info['definition']} (Example: {slang_info['example']})"
    
    if "define" in user_input_lower:
        word_to_define = user_input_lower.split("define")[-1].strip()
        if word_to_define in slang_data:
            slang_info = slang_data[word_to_define]
            return f"{word_to_define.capitalize()}: {slang_info['definition']} (Example: {slang_info['example']})"
    
    return "Sorry, I don't understand that."

def train(data):
    for user_message, bot_message in data:
        if "define" in user_message.lower():
            parts = user_message.split("define")
            if len(parts) > 1:
                new_word = parts[1].strip().lower()
                new_definition = bot_message.strip()
                
                slang_data[new_word] = {
                    'definition': new_definition,
                    'example': 'No example available yet.',
                    'popularity': 'New'
                }
                
                new_entry = SlangWord(word=new_word, definition=new_definition, example='No example available yet.', popularity='New')
                db.session.add(new_entry)
                db.session.commit()

                return f"Added definition for '{new_word}': {new_definition}"

    return "No new definitions added."