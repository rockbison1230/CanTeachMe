from flask import Flask, request, render_template
from textblob import TextBlob
import openai

app = Flask(__name__)

openai.api_key = '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'
# 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
general_phrases = [
    {
        "phrase": "I'd love it if you did this for me.",
        "sentiment": "Positive",
        "suggestion": "While it is phrased like a general statement expressing favor towards a hypothetical scenario, for many it is also a less direct, 'more polite,' way of saying 'Can you do this for me?'",
        "explanation": "This input is said to have a positive sentiment due to the use of the word 'love' expressing strong positive feelings. It is then a precursor to the phrase, 'if you did this for me,' which means that someone doing a specific action would cause a positive feeling."
    },
    {
        "phrase": "How are you?",
        "sentiment": "Neutral",
        "suggestion": "It helps to keep things simple and say a simple 'Great, and you?' if you'd rather not go in detail and let them continue the conversation, or share more about your feelings if you'd like. ",
        "explanation": "This input is said to have a neutral sentiment. For many, 'how are you' is another way of being polite and starting a conversation. Especially if they are people you are not acquainted with, they are not often expecting a lengthy or even genuine reply. The phrase itself is open-ended and often has an expected reply of 'I'm good / okay.' "

    },
]


@app.route('/index.html', methods=['GET', 'POST'])
def index():
    # first generate sentiment
    sentiment = None
    if request.method == "POST":
        userInput = request.form.get("expression")
        for item in general_phrases:
            if item["phrase"] in userInput:
                sentiment = item["sentiment"]
                suggestion = item["suggestion"]
                explanation = item["explanation"]
                return render_template("index.html", sentiment=sentiment, suggestion=suggestion, explanation=explanation)
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
                max_tokens=100
            )
        explanation = response.choices[0].text.strip()

        return render_template("index.html", sentiment=sentiment, suggestion=suggestion, explanation=explanation)
    else:
        return render_template("index.html", userInput=None)


@app.route('/education.html')
def education():
    return render_template("education.html")


@app.route('/about.html')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)
