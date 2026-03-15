import os
import json
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import speech_recognition as sr
from autocorrect import Speller
import threading

app = Flask(__name__)
CORS(app)
spell = Speller(lang='en')

# Settings
GESTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'static', 'gestures')

# Load MS-ASL Mapping as Fallback
msasl_db = {}
try:
    with open(os.path.join("MS-ASL", "MSASL_train.json"), "r") as f:
        msasl_data = json.load(f)
        for item in msasl_data:
            word = item.get("clean_text", "").lower()
            # We want short direct signs, avoid long multi-word mappings if possible
            if word and word not in msasl_db:
                msasl_db[word] = item
except Exception as e:
    print(f"Warning: MS-ASL dataset not found or failed to load: {e}")

@app.route('/')
def index():
    """Serves the main index.html page."""
    return render_template('index.html')

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    """Accepts audio blob from frontend, uses Python SpeechRecognition to convert to text."""
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
        
    audio_file = request.files['audio']
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return jsonify({"text": text.lower()})
    except sr.UnknownValueError:
        return jsonify({"error": "Speech was not understood"}), 400
    except sr.RequestError:
        return jsonify({"error": "Speech recognition service unavailable"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-word-list', methods=['GET'])
def get_word_list():
    """Returns list of all available gesture video words from the gestures folder."""
    words = []
    asl_dir = os.path.join(GESTURES_DIR, 'asl')
    if os.path.exists(asl_dir):
        for filename in os.listdir(asl_dir):
            if filename.endswith('.mp4'):
                words.append(filename.replace('.mp4', ''))
    return jsonify({"words": list(set(words))})

@app.route('/gestures/<language>/<word>', methods=['GET'])
def get_gesture(language, word):
    """Serves the video file for a given word or falls back to fingerspelling."""
    word = word.lower()
    target_dir = os.path.join(GESTURES_DIR, language)
    video_path = os.path.join(target_dir, f"{word}.mp4")
    
    if os.path.exists(video_path):
        return jsonify({
            "type": "word",
            "video": f"/static/gestures/{language}/{word}.mp4"
        })
    else:
        # Fallback to fingerspelling
        letters = list(word)
        videos = []
        for char in letters:
            if char.isalpha():
                videos.append(f"/static/gestures/{language}/{char}.mp4")
        return jsonify({
            "type": "fingerspell",
            "letters": letters,
            "videos": videos
        })

@app.route('/process-sentence', methods=['POST'])
def process_sentence():
    """Accepts a sentence, cleans it, and returns the full video queue."""
    data = request.get_json()
    if not data or 'sentence' not in data:
        return jsonify({"error": "No sentence provided"}), 400
        
    original_sentence = data['sentence'].lower()
    
    # Expand common contractions for better translation
    contractions = {
        "im": "i am", "i'm": "i am", "dont": "do not", "don't": "do not", 
        "cant": "can not", "can't": "can not", "wont": "will not", "won't": "will not",
        "ive": "i have", "i've": "i have", "ill": "i will", "i'll": "i will",
        "youre": "you are", "you're": "you are", "theyre": "they are", "they're": "they are",
        "isnt": "is not", "isn't": "is not", "arent": "are not", "aren't": "are not",
        "whats": "what is", "what's": "what is", "that's": "that is", "thats": "that is",
        "it's": "it is", "its": "it is"
    }
    
    words_split = original_sentence.split()
    expanded_words = [contractions.get(w, w) for w in words_split]
    expanded_sentence = " ".join(expanded_words)
    
    # Apply auto-correct in case of typos
    corrected_sentence = spell(expanded_sentence)
    
    words_list = "".join([c if c.isalnum() or c.isspace() else "" for c in corrected_sentence]).split()
    
    language = data.get('language', 'asl').lower()
    target_dir = os.path.join(GESTURES_DIR, language)
    
    # Improved greedy N-gram matcher to catch phrases like "thank you"
    queue = []
    i = 0
    while i < len(words_list):
        found_match = False
        # Try finding the longest possible matching phrase first (up to length of remaining words)
        for j in range(len(words_list), i, -1):
            phrase = " ".join(words_list[i:j])
            
            video_path = os.path.join(target_dir, f"{phrase}.mp4")
            
            # We must strip spaces from phrase for fallback letters
            letters = list(phrase.replace(" ", ""))
            fallback_videos = [f"/static/gestures/{language}/{char}.mp4" for char in letters if char.isalpha()]
            fallback_images = [f"/static/gestures/alphabets_images/{char.upper()}.jpg" for char in letters if char.isalpha()]

            if os.path.exists(video_path):
                queue.append({
                    "word": phrase,
                    "type": "word",
                    "video": f"/static/gestures/{language}/{phrase}.mp4",
                    "fallback_videos": fallback_videos,
                    "fallback_images": fallback_images
                })
                i = j
                found_match = True
                break
            elif phrase in msasl_db:
                ms_entry = msasl_db[phrase]
                url: str = ms_entry["url"]
                video_id = url.split("v=")[-1] if "v=" in url else url.split("/")[-1]
                
                queue.append({
                    "word": phrase,
                    "type": "youtube",
                    "video_id": video_id,
                    "start": ms_entry.get("start_time", 0),
                    "end": ms_entry.get("end_time", 0),
                    "fallback_videos": fallback_videos,
                    "fallback_images": fallback_images
                })
                i = j
                found_match = True
                break
                
        if not found_match:
            # If no known word or phrase is found, fallback to fingerspelling a single word
            word = words_list[i]
            letters = list(word)
            videos = [f"/static/gestures/{language}/{char}.mp4" for char in letters if char.isalpha()]
            images = [f"/static/gestures/alphabets_images/{char.upper()}.jpg" for char in letters if char.isalpha()]
            queue.append({
                "word": word,
                "type": "fingerspell",
                "letters": letters,
                "videos": videos,
                "images": images
            })
            i += 1
            
    return jsonify({"queue": queue, "corrected_sentence": corrected_sentence})

@app.route('/easter-egg', methods=['GET'])
def easter_egg():
    """Triggered when user types 'antigravity'."""
    # Importing antigravity inside the request opens a comic in the browser!
    # Moved from top of file to only trigger when the route is hit.
    import antigravity 
    return jsonify({"easter_egg": True, "message": "You found it! 🚀"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)