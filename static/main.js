var timeElement = document.getElementById("time");

function updateTime() {
    var currentTime = new Date();
    var hours = currentTime.getHours();
    var minutes = currentTime.getMinutes();
    var seconds = currentTime.getSeconds();
    var ampm = hours >= 12 ? '下午' : '上午';

    hours = hours % 12;
    hours = hours ? hours : 12;

    var formattedTime = ampm + ' ' + hours + ':' +
        (minutes < 10 ? "0" : "") + minutes + ':' +
        (seconds < 10 ? "0" : "") + seconds;
    timeElement.textContent = formattedTime;
}

updateTime();
setInterval(updateTime, 1000);

document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.place-card');
    cards.forEach(card => {
        card.addEventListener('click', function() {
            const cardId = this.querySelector('.overlay-text h1').textContent;
            showModal(cardId);
        });
    });
});

function showModal(cardId) {
    fetchData(cardId);
    document.getElementById('myModal').style.display = 'block';
    document.getElementById('nameid').textContent = ` ${cardId} 長者監測視窗`;
}

function fetchData(cardId) {
    fetch(`/data/place${cardId}`)
        .then(response => response.json())
        .then(data => {
            const dataTable = document.getElementById('data-table');
            dataTable.innerHTML = '';
            data.forEach(item => {
                const row = `<tr><td>${item.time}</td><td>${item.place}</td></tr>`;
                dataTable.innerHTML += row;
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}

function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == document.getElementById('myModal')) {
        closeModal();
    }
}

function fetchDataAndUpdate() {
    ['104', '105', '106'].forEach(placeId => {
        fetch(`/data/place${placeId}`)
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
                    const latestPlace = data[data.length - 1].place;
                    const placeElement = document.getElementById(`${placeId}-place`);
                    const watchOutElement = document.getElementById(`${placeId}-Watch-out`);

                    placeElement.textContent = latestPlace;

                    let warnings = [];

                    if (isLunchSimulationActive && latestPlace !== '餐廳') {
                        warnings.push('長者未於午餐時間在餐廳，已傳Line通知照護者');
                    }

                    if (isLongTimeSimulationActive) {
                        warnings.push('長時間未移動，已傳Line通知照護者');
                    }

                    if (latestPlace === '危險區域') {
                        warnings.push('誤闖危險區域，已傳Line通知照護者');
                    }

                    if (warnings.length === 0) {
                        warnings.push('暫無事項');
                    }

                    watchOutElement.innerHTML = warnings.join('<br>');
                    watchOutElement.style.color = warnings.some(warning => warning !== '暫無事項') ? 'red' : 'initial';
                }
            })
            .catch(error => console.error('Error fetching data:', error));
    });
}






fetchDataAndUpdate();
setInterval(fetchDataAndUpdate, 5000);

var isLunchSimulationActive = false;
var isLongTimeSimulationActive = false;

function toggleLunchSimulation() {
    isLunchSimulationActive = !isLunchSimulationActive;
    var button = document.querySelector("#lunch-button");
    button.textContent = isLunchSimulationActive ? "取消模擬" : "模擬午餐時間";
    fetchDataAndUpdate();
}

function simulateLongTime() {
    isLongTimeSimulationActive = !isLongTimeSimulationActive;
    var button = document.querySelector("#long-time-button");
    button.textContent = isLongTimeSimulationActive ? "取消模擬" : "模擬長時間長者在固定區域";
    fetchDataAndUpdate();
}