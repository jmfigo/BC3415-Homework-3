from flask import Flask, render_template, request
import google.generativeai as genai
import os
from textblob import TextBlob


api = os.getenv("MAKERSUITE_API_TOKEN")
genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return(render_template("index.html"))

@app.route("/financial_QA", methods=["GET", "POST"])
def financial_QA():
    return(render_template("financial_QA.html"))

@app.route("/makersuite", methods=["GET", "POST"])
def makersuite():
    q = request.form.get("q")
    r = model.generate_content(q)
    return(render_template("makersuite.html", r=r.text))

@app.route("/sentiment_analysis", methods=["GET", "POST"])
def sentiment_analysis():
    return(render_template("sentiment_analysis.html"))

@app.route("/sentiment_analysis_results", methods=["GET", "POST"])
def sentiment_analysis_results():
    q = request.form.get("q")
    blob = TextBlob(q)
    
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity == 0:
        polarity_desc = "Neutral sentiment"
    elif polarity > 0:
        if polarity < 0.5:
            polarity_desc = "Slightly positive sentiment"
        else:
            polarity_desc = "Strongly positive sentiment"
    else:
        if polarity > -0.5:
            polarity_desc = "Slightly negative sentiment"
        else:
            polarity_desc = "Strongly negative sentiment"
    
    if subjectivity == 0:
        subjectivity_desc = "Objective statement"
    elif subjectivity == 1:
        subjectivity_desc = "Subjective statement"
    else:
        subjectivity_desc = "Partly subjective, partly objective"

    r = blob.sentiment
    sen = f"Sentiment: {polarity_desc}"
    sub = f"Subjectivity: {subjectivity_desc}"

    return(render_template("sentiment_analysis_results.html", r=r, sen=sen, sub=sub))

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    return(render_template("prediction.html"))

@app.route("/joke", methods=["GET", "POST"])
def joke():
    r = model.generate_content("Tell me one joke rooted in Singaporean culture that can only be as long as two sentences.")
    return(render_template("joke.html", r=r.text))

if __name__ == "__main__":
    app.run()
