from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Clave de API de OpenAI (de tu entorno en Render o local)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Diccionario para guardar contexto por usuario (simple memoria)
conversaciones = {}

# Base de conocimiento
BASE_CONOCIMIENTO = """
Modelos B2Grow: MB2, MB3, EB210, EB240, MOBILE CHASSIS, AC200, AC300 y paneles solares plegables.
Escalabilidad modular: 2 kWh a 100 kWh, salida de 2,2 kW a 22 kW.
Carga rápida CA: 80% ≈ 1 h, 100% ≈ 1.6 h. Carga solar máxima: 1000 W (XT60 11–60 V, 20 A).
BMS: 18 protecciones, sobrecarga, cortocircuito, sobretemperatura.
Refrigeración: 10 ventiladores, disipadores de aluminio.
App EnergyKeeper: control remoto, requiere Wi-Fi 2.4 GHz.
Mantenimiento: mantener seco, ventilar, limpiar puertos.
Instalación: apilar hasta 8.5 kWh máx; activar sistema cargándolo al 100%.
UPS: tres modos según tipo de carga; no apto 0 ms.
Paneles plegables: 100–500 W, IP67, monocristalinos.
UFO LED B2GHB12: 100W, 150W, 200W; 3000K/5500K/6500K; IP65; dimerizable 1–10V; garantía 5 años.
"""

@app.route("/message", methods=["POST"])
def message():
    data = request.get_json()
    user_msg = data.get("message", "")
    user_id = data.get("user_id", "default")  # identificador de sesión simple

    if not user_msg.strip():
        return jsonify({"reply": "Por favor, escribí un mensaje para que pueda ayudarte."})

    # Recuperar historial de conversación del usuario
    historial = conversaciones.get(user_id, [])
    historial.append({"role": "user", "content": user_msg})

    try:
        # Crear el contexto con historial + conocimiento base
        messages = [{"role": "system", "content": f"Sos Bitu, asistente técnico de B2Grow. Usa este conocimiento:\n{BASE_CONOCIMIENTO}"}]
        messages.extend(historial)

        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=350,
            temperature=0.4
        )

        reply = completion.choices[0].message["content"].strip()
        historial.append({"role": "assistant", "content": reply})
        conversaciones[user_id] = historial  # guardar conversación

        return jsonify({"reply": reply})

    except Exception as e:
        print("⚠️ Error:", e)
        return jsonify({
            "reply": "Ocurrió un error al conectar con la IA. Revisá la API Key o el servidor."
        })


if __name__ == "__main__":
    app.run(debug=True)
