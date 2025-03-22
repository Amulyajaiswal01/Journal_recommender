from flask import Flask, request, jsonify, send_from_directory
import os
import pdfplumber
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__, static_folder="static")

df = pd.read_csv("journals.csv")

vectorizer = TfidfVectorizer(stop_words="english")
journal_vectors = vectorizer.fit_transform(df["abstract"])

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/get_journals", methods=["GET"])
def get_journals():
    return jsonify({"journals": df["journal_name"].tolist()})


@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    pdf_file = request.files["pdf"]
    pdf_path = os.path.join("uploads", pdf_file.filename)
    pdf_file.save(pdf_path)

    paper_text = extract_text_from_pdf(pdf_path)
    paper_vector = vectorizer.transform([paper_text])
    similarities = cosine_similarity(paper_vector, journal_vectors).flatten()

    top_journal_indices = similarities.argsort()[-3:][::-1]
    recommended_journals = df.iloc[top_journal_indices]["journal_name"].tolist()

    return jsonify({"journals": recommended_journals})

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
