from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Charger base étudiants
with open("students_prepo_25_26.json", "r", encoding="utf-8") as f:
    students = json.load(f)


def calculate_average(notes):
    return round(sum(notes.values()) / len(notes), 2)


@app.route("/student/<matricule>", methods=["GET"])
def get_student(matricule):
    if matricule not in students:
        return jsonify({"error": "Matricule introuvable"}), 404

    student = students[matricule]

    if "notes" not in student:
        student["notes"] = {
            "S1": {"Math": 12, "Physique": 14, "Info": 15},
            "S2": {"Math": 13, "Physique": 15, "Info": 16}
        }

    s1_avg = calculate_average(student["notes"]["S1"])
    s2_avg = calculate_average(student["notes"]["S2"])
    general = round((s1_avg + s2_avg) / 2, 2)

    return jsonify({
        "nom": student["nom"],
        "sexe": student["sexe"],
        "S1": student["notes"]["S1"],
        "S2": student["notes"]["S2"],
        "moyenne_S1": s1_avg,
        "moyenne_S2": s2_avg,
        "moyenne_generale": general
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
