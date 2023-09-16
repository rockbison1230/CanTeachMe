from flask import Flask, request, render_template
import nltk
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import openai

app = Flask(__name__)
nltk.download('all')

analyzer = SentimentIntensityAnalyzer()


@app.route('/', methods=['GET', 'POST'])
def index():
    # first generate sentiment
    sentiment = None
    if request.method == "POST":
        userInput = request.form.get("expression")
        analysis = TextBlob(userInput)
        sentiment_score = analysis.sentiment.polarity
        if sentiment_score > 0:
            sentiment = "Positive"
        elif sentiment_score < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        return render_template("index.html", userInput=userInput, sentiment=sentiment)
    else:
        return render_template("index.html", userInput=None)


if __name__ == '__main__':
    app.run(debug=True)
