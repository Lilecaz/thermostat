import time
import serial

# Stockage des valeurs reçues
data = {
    "temperature": 0.0,
    "humidite": 0.0,
    "temperaturecible":0.0
}

def read_uart_data():
    """Lit les trames UART du STM32 et met à jour les valeurs de température et humidité."""
    print("Démarrage de la lecture du port série...")
    
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        ser.flush()
        
        print("Connexion établie. En attente de données...")
        
        while True:
            if ser.in_waiting > 0:
                ligne = ser.readline().decode('utf-8').strip()
                valeurs = ligne.split(",")  # Séparer la ligne par la virgule
                
                if len(valeurs) == 3:  # Vérifier qu'on a bien 2 valeurs
                    try:
                        data["temperature"] = float(valeurs[0])
                        data["humidite"] = float(valeurs[1])
                        data['temperaturecible'] = float(valeurs[2])
                        print(f"Température: {data['temperature']}°C, Humidité: {data['humidite']}%, temp_Cible :{data['temperaturecible']}°C")
                    except ValueError:
                        print(f"Erreur de conversion des valeurs: {ligne}")
            
            time.sleep(0.1)  # Petite pause pour réduire l'utilisation CPU
            
    except serial.SerialException as e:
        print(f"Erreur lors de l'ouverture du port série: {e}")
    except KeyboardInterrupt:
        print("Lecture interrompue par l'utilisateur")
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Port série fermé")

if __name__ == "__main__":
    read_uart_data()
