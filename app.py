from flask import Flask, request, jsonify
import re
from collections import defaultdict, Counter

app = Flask(__name__)

# Load sentences and build n-grams as before
def load_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    sentences = text.strip().split('\n\n')
    return [re.sub(r'\s+', ' ', sentence.strip()) for sentence in sentences]

def build_ngrams(sentences, n=3):
    ngrams = defaultdict(Counter)
    for sentence in sentences:
        tokens = sentence.lower().split()
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i + n - 1])
            next_word = tokens[i + n - 1]
            ngrams[ngram][next_word] += 1
    return ngrams

# Predict the next word
def predict_next_word(ngrams, text, n=3):
    tokens = text.lower().split()
    if len(tokens) < n - 1:
        return None
    context = tuple(tokens[-(n - 1):])
    if context in ngrams:
        next_words = ngrams[context]
        most_frequent_word = next_words.most_common(1)[0][0]
        return most_frequent_word
    else:
        return None

# Load and build n-grams once
sentences = load_sentences('all_sentences.txt')
ngrams = build_ngrams(sentences, n=3)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_text = data.get("input_text", "")
    predicted_word = predict_next_word(ngrams, input_text, n=3)
    return jsonify({"predicted_word": predicted_word or ""})

if __name__ == "__main__":
    app.run(debug=True)
