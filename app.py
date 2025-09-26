from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from thefuzz import process
from deep_translator import GoogleTranslator # NAYI Library import ki hai

app = Flask(__name__)
CORS(app)

# --- MongoDB Connection ---
CONNECTION_STRING = "mongodb://localhost:27017/"
client = MongoClient(CONNECTION_STRING)
db = client['kisan_sahayak']
collection = db['knowledge_base']
print("Database se connection safal raha!")

# ===================================================================
# == FINAL API Endpoint - Smart Logic + Translation ke saath ==
# ===================================================================
@app.route('/ask', methods=['POST'])
def ask_bot():
    user_message = request.json.get('question')
    language = request.json.get('language', 'en') # NAYA: User ki language lena
    
    if not user_message:
        return jsonify({"error": "Sawaal nahi mila"}), 400

    try:
        # NAYA STEP 1: User ke sawaal ko English mein translate karna
        question_in_english = GoogleTranslator(source='auto', target='en').translate(user_message)
        print(f"User Sawaal ('{language}'): '{user_message}' -> Translated to English: '{question_in_english}'")

        # Aapka Purana Step 2: English sawaal ka sabse accha match dhoondhna
        all_questions = [doc['question'] for doc in collection.find({}, {'question': 1, '_id': 0})]
        if not all_questions:
             return jsonify({"answer": "Database khaali hai."})

        matches = process.extract(question_in_english, all_questions, limit=3)
        best_match = matches[0]
        match_text = best_match[0]
        match_score = best_match[1]
        
        print(f"Top Match: '{match_text}', Score: {match_score}")

        bot_reply_in_english = ""
        
        # Aapka Purana Step 3: Wahi smart wala logic
        if match_score >= 95:
            result = collection.find_one({"question": match_text})
            bot_reply_in_english = result.get("answer", "Jawaab nahi mila.")
        
        elif match_score >= 80:
            second_best_match_score = matches[1][1]
            if (match_score - second_best_match_score) < 8:
                bot_reply_in_english = "Main aapka sawaal theek se samajh nahi paya. Kya aap inmein se kuch pooch rahe hain?\n"
                options = [f"- {match[0]}" for match in matches if match[1] > 75]
                bot_reply_in_english += "\n".join(options)
            else:
                result = collection.find_one({"question": match_text})
                bot_reply_in_english = result.get("answer", "Jawaab nahi mil paya.")
        else:
            bot_reply_in_english = "Maaf kijiye, mujhe is baare mein jaankari nahi hai."
            
        # NAYA STEP 4: Final English jawaab ko wapas user ki language mein translate karna
        print(f"Bot Answer (English): '{bot_reply_in_english}' -> Translating to '{language}'")
        final_answer = GoogleTranslator(source='en', target=language).translate(bot_reply_in_english)
            
        return jsonify({"answer": final_answer})

    except Exception as e:
        print(f"Ek error aa gaya hai: {e}")
        return jsonify({"answer": "Maaf kijiye, kuch takniki samasya aa gayi hai."})

# Server ko Start karna
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)