import os
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from modules.Prompt_Engine.training_data import TRAINING_DATA

MODEL_PATH = "model.joblib"
VECTORIZER_PATH = "vectorizer.joblib"


def train_and_save_model():
    texts, labels = zip(*TRAINING_DATA)
    vectorizer = CountVectorizer(stop_words="english")  # ✅ Stopword filtering
    X = vectorizer.fit_transform(texts)
    model = MultinomialNB()
    model.fit(X, labels)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)


def load_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        train_and_save_model()
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


model, vectorizer = load_model()


def classify_prompt(text: str) -> str:
    X_input = vectorizer.transform([text])
    return model.predict(X_input)[0]


def route_prompt(text: str) -> str:
    label = classify_prompt(text)
    if label == "greeting":
        return "Hello!"
    elif label == "farewell":
        return "Goodbye!"
    elif label == "question":
        return "Let me help you with that."
    elif label == "intent":
        return "Great! Let’s get started."
    else:
        return "I'm not sure how to respond."
