# Thermostat Project

Ce projet est une application complète de gestion de thermostat, composée d'un backend Python et d'un frontend web.

## Structure du projet

```
thermostat/
│
├── back/           # Backend Python (API, communication UART)
│   ├── server.py           # Serveur principal
│   ├── receive_uart.py     # Réception UART
│   ├── send_uart.py        # Envoi UART
│   ├── output.log          # Logs d'exécution
│   └── __pycache__/        # Fichiers compilés Python
│
└── front/          # Frontend web (interface utilisateur)
    ├── index.html         # Page principale
    ├── script.js          # Logique JavaScript
    └── styles.css         # Styles CSS
```

## Prérequis
- Python 3.11 ou supérieur
- (Optionnel) Environnement virtuel Python (`venv`)
- Navigateur web moderne

## Installation et lancement

### 1. Backend (Python)
1. Ouvrir un terminal et aller dans le dossier `back` :
   ```powershell
   cd back
   ```
2. (Optionnel) Créer et activer un environnement virtuel :
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
3. Installer les dépendances (si besoin) :
   ```powershell
   pip install -r requirements.txt
   ```
   *(Créer le fichier `requirements.txt` si nécessaire)*
4. Lancer le serveur :
   ```powershell
   python server.py
   ```

### 2. Frontend (Web)
1. Ouvrir le fichier `front/index.html` dans votre navigateur.
2. L'interface communique avec le backend (assurez-vous que le serveur Python est lancé).

## Fonctionnalités principales
- Communication UART via scripts Python
- Interface web pour contrôler et visualiser le thermostat
- Logs d'exécution dans `output.log`

## Auteurs
- Lilecaz

## Licence
Ce projet est sous licence MIT (à adapter selon vos besoins).
