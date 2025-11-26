Advanced Emotional Intelligence (EQ) Assessment System

A Django-based web application that measures a user’s emotional intelligence using transformer-based NLP models for emotion detection and sentiment analysis. The system evaluates the emotional tone of user responses to workplace scenarios and generates an EQ score breakdown, visual graphs, and personalized feedback.


---

🚀 Project Overview

The Advanced EQ Assessment System analyzes a user’s text responses to real-world conflict scenarios. Using transformer models, it detects:

Emotional tone

Sentiment polarity

Emotional intensity


These signals are then passed into a custom scoring engine that outputs:

🌟 Overall EQ Score

🔍 EQ Category Breakdown

🧠 Detailed feedback

📊 Interactive charts (Chart.js)


This project demonstrates the use of NLP, transformers, and psychological scoring logic inside a modern Django application.


---

🧠 Technologies Used

Backend

Django 5

Python 3.10+

HuggingFace Transformers

DistilBERT (sentiment model)

DistilRoBERTa emotion classification model


NLP Models

distilbert-base-uncased-finetuned-sst-2-english (sentiment analysis)

j-hartmann/emotion-english-distilroberta-base (emotion classification)


Frontend

HTML, CSS

Bootstrap

Chart.js (for EQ score visualization)



---

🎯 System Workflow

1. User Inputs Responses

The user answers 3 scenario-based EQ questions.

2. Transformer Models Analyze Text

Each response is processed through:

Sentiment Analysis → POSITIVE / NEGATIVE + polarity score

Emotion Detection → anger, joy, fear, sadness, trust, etc.

Emotion Intensity → how strong the detected emotion is


3. EQ Scoring Engine

A custom engine maps transformer outputs to EQ attributes:

Self-awareness

Emotional regulation

Empathy

Conflict resolution

Motivation

Social skills


Scoring includes:

Baseline scores

Emotion-to-category weights

Polarity influence

Pattern detection (High EQ & Low EQ keywords)

Response quality factor

Final normalization


4. Results Page

The system displays:

Overall EQ score

Category breakdown

Personalized feedback

A bar chart of all EQ components



---

📁 Project Structure

eq_project/
│── eq_project/         # Django project settings
│── assessment/         # Main application
│   ├── templates/
│   │   ├── assessment/
│   │   │   ├── base.html
│   │   │   ├── index.html
│   │   │   ├── result.html
│   │   │   └── scenarios.html
│   ├── static/
│   ├── views.py
│   ├── scoring.py      # EQ Scoring Engine (final version)
│   ├── forms.py
│   ├── models.py
│── db.sqlite3
│── manage.py
│── README.md


---

📊 EQ Categories Explained

Category	Meaning

Self-Awareness	Understanding own emotions
Emotional Regulation	Staying calm under pressure
Empathy	Understanding others' emotions
Conflict Resolution	Managing disagreements constructively
Motivation	Drive, discipline, positivity
Social Skills	Communication, collaboration



---

🛠 How to Run the Project

1. Create Virtual Environment

python -m venv venv

2. Activate

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Run Server

python manage.py runserver

5. Open Browser

http://127.0.0.1:8000/


---

🧩 Key Features

✔ Transformer-based NLP
✔ Multi-response emotional analysis
✔ Advanced EQ scoring engine
✔ Clean and modern UI
✔ Interactive bar charts
✔ Fully responsive HTML/CSS
✔ Professional insights & feedback
✔ Ready for deployment or extension


---

🧪 Testing the System

Try 3 types of responses:

🔹 High EQ → Expect 90+

Calm, collaborative, empathetic answers.

🔹 Medium EQ → Expect 50–70

Basic emotional awareness.

🔹 Low EQ → Expect 20–40

Reactive, dismissive, irritated responses.

This confirms that the model + scoring logic works correctly.


---

📌 Notes

This project is designed as a practical NLP application demonstrating:

Sentiment analysis

Emotion classification

Scoring logic design

Psychological interpretation

Deployment in a real web app


It can be extended into:

HR screening tools

Leadership assessment

Chat-based coaching

Emotional wellness apps
