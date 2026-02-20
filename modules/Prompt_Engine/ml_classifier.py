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


from LLM_Provider_Orchestration.llm_client import llm_client
from modules.Prompt_Engine.vector_store import vector_store

def route_prompt(text: str) -> str:
    label = classify_prompt(text)
    
    if label == "greeting":
        return "Hello! How can I assist you today?"
    elif label == "farewell":
        return "Goodbye! Have a great day!"
    elif label == "question":
        # RAG Logic
        context_docs = vector_store.search(text)
        if context_docs:
            context = "\n".join(context_docs)
            prompt = f"Use the following context to answer the question:\n\nContext:\n{context}\n\nQuestion: {text}"
            return llm_client.generate_response(prompt, system_prompt="You are a helpful AI assistant for PromptWise.")
        else:
            # Fallback if no context found
            return llm_client.generate_response(text)
    elif label == "intent":
        return "I understand your intent. Let's proceed with that action."
    else:
        # For unknown or general intents, let the LLM handle it
        return llm_client.generate_response(text)
