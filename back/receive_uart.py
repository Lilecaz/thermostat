import time
import serial

# Stockage des valeurs reçues
data = {
    "temperature": 0.0,
    "humidite": 0.0,
    "targetTemp":0.0
}

def read_uart_data():
    """Lit les trames UART du STM32 et met à jour les valeurs de température et humidité."""
    print("Démarrage de la lecture du port série...")
    
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        ser.flush()
        
        print("Connexion établie. En attente de données...")
        print("step1")
        while True:
            print("step2")
            ligne = ser.readline().decode('utf-8').strip()

            # Vérifier si la ligne est vide ou contient autre chose qu'un format attendu
            if not ligne or not any(char.isdigit() for char in ligne):
                print(f"Message reçu non numérique : '{ligne}'")
                continue  # Ignorer cette ligne et recommencer la boucle

            valeurs = ligne.split(",")  # Séparer la ligne par la virgule

            if len(valeurs) == 3:  # Vérifier qu'on a bien 3 valeurs
                try:
                    data["temperature"] = float(valeurs[0])
                    data["humidite"] = float(valeurs[1])
                    data["targetTemp"] = float(valeurs[2])
                    print(f"Température: {data['temperature']}°C, Humidité: {data['humidite']}%, Target: {data['targetTemp']}")
                except ValueError:
                    print(f"Erreur de conversion des valeurs : {ligne}")
            else:
                print(f"Format inattendu reçu : {ligne}")  # Gérer les cas où la ligne ne contient pas 3 valeurs

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