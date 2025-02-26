# Installation des dépendances nécessaires
# pip install flask flask-cors pyserial

from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import receive_uart as receive
import send_uart as send

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis le frontend

# Données stockées en mémoire
data = {
    "temperature": 0.0,
    "humidite": 0.0,
    "relais": False,
    "target_temperature": 0
}

def update_data():
    """Met à jour les données en récupérant celles reçues par UART."""
    global data
    while True:
        data["temperature"] = receive.data["temperature"]
        data["humidite"] = receive.data["humidite"]
        data['target_temperature'] = receive.data["targetTemp"]

@app.route('/api/data', methods=['GET'])
def get_data():
    # print(data)
    return jsonify(data)

@app.route('/api/set_temp', methods=['POST'])
def set_temperature():
    """Met à jour la température cible."""
    global data
    req_data = request.get_json()
    data['target_temperature'] = float(req_data.get('temperature', data['target_temperature']))
    send.send_target_temperature('/dev/ttyACM0', 115200, data['target_temperature'])
    return jsonify({"message": "Température cible mise à jour."})

@app.route('/api/update_sensor', methods=['POST'])
def update_sensor():
    """Mise à jour des données depuis le STM32."""
    global data
    req_data = request.get_json()
    data['temperature'] = float(req_data.get('temperature', data['temperature']))
    data['humidite'] = float(req_data.get('humidite', data['humidite']))
    data['target_temperature'] = float(req_data.get('temperature', data['target_temperature']))
    data['relais'] = bool(req_data.get('relais', data['relais']))
    return jsonify({"message": "Données mises à jour."})

# Démarrer la lecture UART et la mise à jour des données en tâche de fond
threading.Thread(target=receive.read_uart_data, daemon=True).start()
threading.Thread(target=update_data, daemon=True).start()

if __name__ == '__main__':
    app.run(host='192.168.26.169', port=5000, debug=True)