from flask import Flask, request, jsonify
from textblob import TextBlob
import nltk
from flask_cors import CORS
import math

nltk.download("punkt")

app = Flask(__name__)
CORS(app)


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Tokenize sentences and words
    sentences = nltk.sent_tokenize(text)
    words = nltk.word_tokenize(text)

    # Statistics
    sentence_count = len(sentences)
    word_count = len(words)
    unique_word_count = len(set(words))
    avg_word_length = sum(len(word) for word in words) / word_count

    # Readability Scores
    def syllable_count(word):
        vowels = "aeiouy"
        count = 0
        word = word.lower()
        word = "".join([ch for ch in word if ch.isalpha()])
        if len(word) == 0:
            return 0
        count += len([char for char in word if char in vowels])
        if word.endswith("e"):
            count -= 1
        return max(1, count)

    total_syllables = sum(syllable_count(word) for word in words)
    flesch_reading_ease = (
        206.835
        - (1.015 * (word_count / sentence_count))
        - (84.6 * (total_syllables / word_count))
    )
    flesch_kincaid_grade = (
        (0.39 * (word_count / sentence_count))
        + (11.8 * (total_syllables / word_count))
        - 15.59
    )

    return jsonify(
        {
            "statistics": {
                "sentence_count": sentence_count,
                "word_count": word_count,
                "unique_word_count": unique_word_count,
                "average_word_length": round(avg_word_length, 2),
            },
            "readability": {
                "flesch_reading_ease": round(flesch_reading_ease, 2),
                "flesch_kincaid_grade": round(flesch_kincaid_grade, 2),
            },
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
