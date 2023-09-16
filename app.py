from flask import Flask, request, render_template
import nltk
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import openai
import os

app = Flask(__name__)
nltk.download('all')
analyzer = SentimentIntensityAnalyzer()

openai.api_key = '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'
# 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

implicit_requests = [
    "I'd like it if you did this for me.",
    "It's hot in here.",
    "I could really use a cup of water right now.",
    "This would be a cool place to go to.",
    "I don't like that one.",
]

small_Talk = [
    "How are you?",
    "What's up?",
    "How've you been?",
    "The weather's pretty nice out."
]

# Define actions and explanations based on sentiment
actions = {
    "positive": ("Validate their feelings and offer support.", "Acknowledge their feelings and show empathy."),
    "negative": ("Use gentle language and ask if they need space or support.", "Offer to listen and understand their perspective."),
    "neutral": ("Ask for clarification or more information.", "Seek to understand their point of view.")
}


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
                max_tokens=90
            )
            explanation = response.choices[0].text.strip()

        return render_template("index.html", userInput=userInput, sentiment=sentiment, suggestion=suggestion, explanation=explanation)
    else:
        return render_template("index.html", userInput=None)


"""
@app.route('/', methods=['GET', 'POST'])
def index():
    input_phrase = None
    sentiment = None
    suggested_action = None
    explanation = None

    if request.method == "POST":
        input_phrase = request.form.get("expression")
        sentiment_score = analyzer.polarity_scores(input_phrase)

        if sentiment_score['compound'] >= 0.05:
            sentiment = "positive"
        elif sentiment_score['compound'] <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        if sentiment in actions:
            suggested_action, explanation = actions[sentiment]

    return render_template("index.html", input_phrase=input_phrase, sentiment=sentiment, suggested_action=suggested_action, explanation=explanation)
"""


if __name__ == '__main__':
    app.run(debug=True)
