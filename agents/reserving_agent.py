import streamlit as st
from datetime import datetime
import torch
import json
import os
import csv
import random
import re
from detoxify import Detoxify
from transformers import pipeline, DistilBertTokenizerFast, DistilBertForSequenceClassification
from sklearn.preprocessing import LabelEncoder

# === Load models ===
#bert_model_dir = "models/distilbert_response_type_balanced"
#bert_tokenizer = DistilBertTokenizerFast.from_pretrained(bert_model_dir)
#bert_model = DistilBertForSequenceClassification.from_pretrained(bert_model_dir)

bert_model_repo = "scdong/distilbert-response-type"
bert_tokenizer = DistilBertTokenizerFast.from_pretrained(bert_model_repo)
bert_model = DistilBertForSequenceClassification.from_pretrained(bert_model_repo)


bert_model.eval()

generator = pipeline("text2text-generation", model="google/flan-t5-xl", device=0 if torch.cuda.is_available() else -1)
tox_model = Detoxify("original")

label_names = ["advice", "information", "question", "validation"]
le = LabelEncoder().fit(label_names)

# === Improved prompt templates ===
prompt_table = {
    "advice": "You are a licensed mental health counselor preparing to support a client who said: \"{msg}\". Provide a thoughtful and supportive suggestion that the counselor might offer to the client.",
    "validation": "You are an empathetic therapist helping a client who shared: \"{msg}\". Write a kind, emotionally validating reflection the counselor might use.",
    "information": "You are a knowledgeable therapist assisting a client who said: \"{msg}\". Provide accurate, relevant information that could help the counselor respond knowledgeably.",
    "question": "You are a licensed therapist preparing to support a client who said: \"{msg}\". Generate an insightful, open-ended question to help the client reflect on their experience and move the conversation forward."
}

response_bank = {
    "advice": [
        "You're doing more than enough — even if it doesn't feel like it right now.",
        "Try to be as kind to yourself as you would to a close friend.",
        "Even small steps count. You're showing up, and that matters."
    ],
    "validation": [
        "It makes total sense you'd feel that way given what you're going through.",
        "Your feelings are valid. Many would feel similarly.",
        "That sounds really tough — thank you for sharing."
    ],
    "information": [
        "Anxiety can cause a racing heart or shortness of breath — that’s very common.",
        "Panic attacks are intense but temporary. They usually pass within minutes.",
        "Mindfulness and deep breathing can help calm your nervous system."
    ],
    "question": [
        "Can you tell me more about what’s been making you feel this way?",
        "What do you think might be behind these feelings?",
        "How long have you been feeling this way?"
    ]
}

# === Safety detection ===
CRISIS_PATTERN = re.compile("|".join([
    r"\bi want to (kill|hurt) myself\b",
    r"\bi (feel|am|have) suicidal\b",
    r"\bsuicidal thoughts\b",
    r"\bsuicidal\b",
    r"\bi want to die\b",
    r"\bend my life\b",
    r"\bno reason to live\b",
    r"\bgive up on life\b",
    r"\bcan.?t go on\b",
    r"\bhopeless\b",
    r"\bhelpless\b",
    r"\bi hate myself\b",
    r"\bkill me\b", r"\bself[- ]?harm\b", r"\bi need help now\b",
    r"\bi never feel good enough\b", r"\bi feel like giving up\b", r"\bi feel worthless\b",
    r"\bmy (client|patient) .* (is|has|feels|wants to).* (suicidal|end their life|kill (himself|herself))\b"
]), flags=re.IGNORECASE)




VIOLENCE_PATTERN = re.compile("|".join([
    r"\bi want to (hurt|kill) (someone|others|people|them|him|her)\b",
    r"\bi will kill\b", r"\bi feel like attacking\b", r"\bhomicide\b",
    r"\bviolence against\b", r"\bi want to cause harm\b"
]), flags=re.IGNORECASE)

CRISIS_RESPONSE = "I'm really sorry you're feeling this way. You're not alone. Please consider calling 988 or speaking with a mental health professional right away."
VIOLENCE_RESPONSE = "If you're having thoughts of harming others, it's critical to speak with a professional immediately. Please reach out to emergency services or a crisis line."

# === Cache ===
CACHE_FILE = "cache.json"
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        response_cache = json.load(f)
else:
    response_cache = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(response_cache, f, indent=2)

def is_crisis(text): return bool(CRISIS_PATTERN.search(text))
def is_violent_threat(text): return bool(VIOLENCE_PATTERN.search(text))
def is_toxic(text): return tox_model.predict(text)["toxicity"] > 0.7

def predict_response_type(msg):
    inputs = bert_tokenizer(msg, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        logits = bert_model(**inputs).logits
    return le.inverse_transform([torch.argmax(logits).item()])[0]

def clean_response(text):
    text = text.strip()
    text = re.sub(r'^["“”\'-]*', '', text)
    text = re.sub(r'\s+', ' ', text)
    if text and not text[0].isupper(): text = text[0].upper() + text[1:]
    if text and text[-1] not in ".!?": text += "."
    return text

def is_high_quality(text):
    return len(text.split()) >= 5 and "kill" not in text.lower() and "hurt" not in text.lower()

# === Streamlit App ===
st.set_page_config(page_title="Mental Health Assistant", layout="centered")
st.title("🧠 Mental Health Counselor Assistant")

# 📘 Instructions
st.markdown("### 📘 How to use this app")
st.markdown("""
1. Enter a message from a patient in the text box.
2. The app will generate helpful suggestions for how the counselor might reply.
3. If a safety risk is detected (e.g., crisis or violence), a safe response will be shown instead.
4. You can save the conversation history as a CSV file.
""")

# 💬 Patient input
msg = st.chat_input("💬 Enter a message from the patient")

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# === Response Generation ===
if msg:
    timestamp = datetime.now().isoformat()

    if is_violent_threat(msg):
        safe_responses = [
            "It’s important to take violent thoughts seriously. If you or someone is in danger, call 911 immediately.",
            "Please seek professional help right away. Safety is the top priority.",
            "If your client has expressed intent to harm others, it's urgent to contact crisis services immediately."
        ]
        st.error("🚨 Violence detected")
        st.markdown(f"**🧍 Patient:** {msg}")
        for r in safe_responses:
            st.markdown(f"**🧠 Suggestion:** {r}")
        st.session_state.chat_log.append((timestamp, msg, "VIOLENCE", safe_responses[0]))

    elif is_crisis(msg):
        safe_responses = [
            "It sounds like you're in a lot of pain right now. Please know that you're not alone.",
            "Your life matters. I encourage you to speak with a mental health professional or call 988.",
            "Thank you for sharing this. There is help available, and you deserve support and care."
        ]
        st.error("🆘 Crisis detected")
        st.markdown(f"**🧍 Patient:** {msg}")
        for r in safe_responses:
            st.markdown(f"**🧠 Suggestion:** {r}")
        st.session_state.chat_log.append((timestamp, msg, "CRISIS", safe_responses[0]))

    elif is_toxic(msg):
        safe_responses = [
            "Thank you for expressing yourself. Let's approach this with compassion and care.",
            "It’s okay to be upset. I'm here to help you explore these feelings in a safe way.",
            "Let’s take a deep breath together and talk through what's on your mind."
        ]
        st.warning("⚠️ Toxic message detected")
        st.markdown(f"**🧍 Patient:** {msg}")
        for r in safe_responses:
            st.markdown(f"**🧠 Suggestion:** {r}")
        st.session_state.chat_log.append((timestamp, msg, "TOXIC", safe_responses[0]))

    else:
        response_type = predict_response_type(msg)
        prompt = prompt_table[response_type].format(msg=msg)

        if prompt in response_cache:
            responses = response_cache[prompt]
        else:
            outputs = generator(
                prompt,
                max_new_tokens=150,
                do_sample=True,
                top_p=0.9,
                temperature=0.7,
                num_return_sequences=3
            )
            responses = [
                clean_response(o["generated_text"])
                for o in outputs
                if is_high_quality(clean_response(o["generated_text"]))
            ]
            if not responses:
                responses = random.sample(response_bank[response_type], 3)
            response_cache[prompt] = responses
            save_cache()

        st.markdown(f"**🧍 Patient:** {msg}")
        for r in responses:
            st.markdown(f"**🧠 Suggestion:** {r}")
        st.session_state.chat_log.append((timestamp, msg, response_type, responses[0]))

# === Save History ===
if st.session_state.chat_log:
    if st.button("💾 Save Conversation History"):
        os.makedirs("logs", exist_ok=True)
        filename = f"logs/counselor_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "message", "type", "response"])
            for row in st.session_state.chat_log:
                writer.writerow(row)
        st.success(f"Saved to `{filename}`")

