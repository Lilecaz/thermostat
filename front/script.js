
function fetchData() {
    console.log("on fetch")

    fetch('http://192.168.26.169:5000/api/data', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    })
        .then(response => response.json())
        .then(data => {
            console.log("on fetch", data)

            document.getElementById('temperature').textContent = data.temperature;
            document.getElementById('humidite').textContent = data.humidite;
            document.getElementById('relais').textContent = data.relais ? 'Activé' : 'Désactivé';
        });
}

function setTemperature() {
    const temp = document.getElementById('targetTemp').value;

    // Envoyer la température cible à la Raspberry Pi
    fetch('http://192.168.26.169:5000/api/set_temp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ temperature: temp })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Température cible définie !');
            } else {
                alert('Erreur lors de la définition de la température cible.');
            }
        });
}

setInterval(fetchData, 2000);

console.log()