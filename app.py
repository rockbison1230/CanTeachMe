from flask import Flask, request, render_template
import nltk
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import openai
import os

app = Flask(__name__)
nltk.download('all')
analyzer = SentimentIntensityAnalyzer()

openai.api_key = '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'
# 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
general_positive = [('how are you?', 'neutral'),
                    ('have you eaten?', 'neutral'),
                    ('how was your day?', 'neutral'),
                    ('how are you doing?', 'neutral'),
                    ('how are you feeling?', 'neutral'),
                    ('how are you', 'neutral'),
                    ('have you eaten', 'neutral'),
                    ('how was your day', 'neutral'),
                    ('how are you doing', 'neutral'),
                    ('how are you feeling', 'neutral')
                    ]


@app.route('/', methods=['GET', 'POST'])
def index():
    # first generate sentiment
    sentiment = None
    if request.method == "POST":
        userInput = request.form.get("expression")
        sentiment_score = analyzer.polarity_scores(userInput)
        if sentiment_score > 0:
            sentiment = "Positive"
        elif sentiment_score < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Provide a suggestion of an action the receiver of this message can take: '{userInput}'",
            max_tokens=60
        )
        suggestion = response.choices[0].text.strip()
        if sentiment == "Positive":
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Provide a detailed explanation for why the sentiment of the input is positive. Example: '{userInput}'",
                max_tokens=60
            )
            explanation = response.choices[0].text.strip()
        if sentiment == "Negative" or sentiment == "Neutral":
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Provide a detailed explanation for why the sentiment of the input is either neutral or negative.: '{userInput}'",
                max_tokens=100
            )
            explanation = response.choices[0].text.strip()
        return render_template("index.html", userInput=userInput, sentiment=sentiment, suggestion=suggestion, explanation=explanation)
    else:
        return render_template("index.html", userInput=None)


if __name__ == '__main__':
    app.run(debug=True)
