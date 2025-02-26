import serial

def send_target_temperature(port, baudrate, target_temperature):
    try:
        # Ouvrir le port série
        ser = serial.Serial(port, baudrate, timeout=1)
        
        # Convertir la température cible en chaîne de caractères et l'envoyer
        temperature_str = f"{target_temperature}\n"
        ser.write(temperature_str.encode('utf-8'))
        
        # Fermer le port série
        ser.close()
        print(f"Température cible {target_temperature} envoyée avec succès.", port, baudrate, target_temperature)
    except serial.SerialException as e:
        print(f"Erreur de communication avec le port série: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")