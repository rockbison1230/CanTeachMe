from flask import Flask, request, render_template
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import openai

app = Flask(__name__)

# openapi key: sk-5mEcjzLISMLrMR73wG9gT3BIbkFJLgtcYn


@app.route('/', methods=["POST"])
def index():
    userExample = request.form['expression']
    return render_template("index.html", userExample=userExample)


if __name__ == '__main__':
    app.run(debug=True)
