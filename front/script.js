document.addEventListener("DOMContentLoaded", () => {
    checkPermissionAndRequestLocation();
    setInterval(fetchData, 2000);
});

function checkPermissionAndRequestLocation() {
    if ("permissions" in navigator) {
        navigator.permissions.query({ name: "geolocation" }).then((result) => {
            if (result.state === "granted") {
                console.log("✅ Localisation autorisée !");
                requestLocation();
            } else if (result.state === "prompt") {
                console.log("⏳ Demande de localisation...");
                requestLocation();
            } else if (result.state === "denied") {
                document.getElementById("location").textContent = "📍 Localisation refusée. Activez-la dans les paramètres.";
                alert("⚠️ Vous avez refusé la localisation. Activez-la dans votre navigateur.");
            }
        });
    } else {
        requestLocation();
    }
}

function requestLocation() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                console.log(`Coordonnées : ${lat}, ${lon}`);

                // API pour obtenir la ville
                const apiKey = "8a9a69033956aa3eb56fa5d2f4e4a35f"; // Remplace par ta clé OpenWeather
                const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${apiKey}&lang=fr`;

                try {
                    const response = await fetch(url);
                    const data = await response.json();
                    const city = data.name;
                    document.getElementById("location").textContent = `📍 ${city}, ${lat.toFixed(2)}, ${lon.toFixed(2)}`;
                } catch (error) {
                    console.error("Erreur récupération de la ville :", error);
                    document.getElementById("location").textContent = "📍 Localisation indisponible";
                }
            },
            (error) => {
                console.error("Erreur de géolocalisation :", error);
                if (error.code === 1) {
                    document.getElementById("location").textContent = "📍 Localisation refusée.";
                    alert("⚠️ Activez la localisation dans votre navigateur.");
                } else if (error.code === 2) {
                    document.getElementById("location").textContent = "📍 Position non disponible.";
                } else if (error.code === 3) {
                    document.getElementById("location").textContent = "📍 Localisation trop lente.";
                } else {
                    document.getElementById("location").textContent = "📍 Erreur inconnue.";
                }
            }
        );
    } else {
        document.getElementById("location").textContent = "📍 Géolocalisation non supportée.";
    }
}

function fetchData() {
    fetch('http://192.168.26.169:5000/api/data', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('temperature').textContent = data.temperature;
        document.getElementById('humidite').textContent = data.humidite;

        updateBackground(data.temperature);
        updateTemperatureIcon(data.temperature);
        updateHumidityCircle(data.humidite);
    });
}

function setTemperature() {
    const temp = document.getElementById('targetTemp').value;

    fetch('http://192.168.26.169:5000/api/set_temp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ temperature: temp })
    })
    .then(response => response.json())
    .then(() => {
        showPopup('Température cible définie !');
    });
}

function updateBackground(temp) {
    if (temp < 10) {
        document.body.style.background = "linear-gradient(135deg, #1e3a8a, #3b82f6)";
    } else if (temp >= 10 && temp < 25) {
        document.body.style.background = "linear-gradient(135deg, #22c55e, #86efac)";
    } else {
        document.body.style.background = "linear-gradient(135deg, #f97316, #facc15)";
    }
}

function updateTemperatureIcon(temp) {
    document.getElementById('tempIcon').textContent = temp < 10 ? "❄️" : temp < 25 ? "☀️" : "🔥";
}

function updateHumidityCircle(humidity) {
    const circle = document.getElementById('humidityCircle');
    circle.style.strokeDashoffset = (100 - humidity) * 2.51;

    const humidityIcon = document.getElementById('humidityIcon');
    if (humidity < 30) {
        humidityIcon.textContent = "💨";
    } else if (humidity >= 30 && humidity < 70) {
        humidityIcon.textContent = "💧";
    } else {
        humidityIcon.textContent = "🌧️";
    }
}

function showPopup(message) {
    const popup = document.getElementById('popup');
    popup.textContent = message;
    popup.style.display = "block";
    setTimeout(() => popup.style.display = "none", 2000);
}
