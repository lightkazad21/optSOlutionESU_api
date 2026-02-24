from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

# Charger les étudiants
with open("students_prepo_25_26.json", "r", encoding="utf-8") as f:
    students = json.load(f)

# ==============================
# ROUTE API ÉTUDIANT
# ==============================

@app.route("/student/<matricule>", methods=["GET"])
def get_student(matricule):
    student = students.get(matricule)

    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Matricule introuvable"}), 404


# ==============================
# CONFIG WHATSAPP
# ==============================

VERIFY_TOKEN = "opt_solution_verify"
WHATSAPP_TOKEN = "EAAJZBhRyiMNsBQz2z2mRwv4ZCW4dsBc8JX1g284lX6EqX9UGZCUFS3ZC4pX8PyRr0ZA0qrO0gj8s3ZB1v0pryA3LpU8mQVIQjZBpubrtpXuEc108hoTuSJEiVoiwYiRe5pvEgyKrYU0Oo8qXUKNHh5QRmbB52DEbgcYv4CGRZAGACFg1GirPq0Kd0E6PUjatRd5ZADvpB4peE713IECcHZAJLh6wHFSe7qEtwxChGAsyRfEjTFYyZCMXMW0rAZDZD"
PHONE_NUMBER_ID = "1022115244319708"
BASE_URL = "https://https://optsolutionesu-api.onrender.com"

# Vérification webhook
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403


# Réception messages WhatsApp
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message["text"]["body"]

        response = requests.get(f"{BASE_URL}/student/{text}")

        if response.status_code == 200:
            student = response.json()
            reply = f"🎓 {student['nom']}\nMoyenne Générale: {student.get('moyenne_generale', 'Non disponible')}"
        else:
            reply = "❌ Matricule introuvable."

        send_message(sender, reply)

    except Exception as e:
        print("Erreur:", e)

    return "OK", 200


def send_message(to, message):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }

    requests.post(url, headers=headers, json=payload)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
