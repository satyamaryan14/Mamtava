// 1. Language Logic
function changeLanguage(lang) {
    alert("Language switched to: " + lang + " (Demo Mode)");
}

// 2. Voice Logic
function startVoiceListening() {
    const btn = document.querySelector('.voice-btn');
    
    // Check if browser supports speech
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert("Voice not supported. Try Chrome browser.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US'; // Default to English
    
    // UI Feedback
    btn.classList.add('listening');
    recognition.start();

    recognition.onresult = async (event) => {
        const text = event.results[0][0].transcript;
        btn.classList.remove('listening');
        
        // Show what user said
        console.log("User said:", text);
        
        // SEND TO PYTHON BACKEND
        await sendToPythonAI(text);
    };

    recognition.onerror = () => {
        btn.classList.remove('listening');
        alert("Couldn't hear you. Try again.");
    };
}

// 3. Connect to Python Backend
async function sendToPythonAI(voiceText) {
    const responseBox = document.getElementById('ai-response');
    const responseText = document.getElementById('ai-text');
    
    responseBox.style.display = 'block';
    responseText.innerText = "Thinking...";

    try {
        const response = await fetch('/api/analyze_voice', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: voiceText })
        });
        
        const data = await response.json();
        
        // Display AI Result
        responseText.innerHTML = `
            <strong>Symptoms:</strong> ${data.detected_symptoms.join(", ") || "None"}<br>
            <strong>Mood:</strong> ${data.mood}
        `;
        
    } catch (error) {
        console.error(error);
        responseText.innerText = "Error connecting to AI Server.";
    }
}
// --- 4. GOVT OPEN DATA LOGIC ---
async function fetchGovtStores() {
    const list = document.getElementById('store-list');
    list.innerHTML = '<p style="font-size:12px;">Fetching from Open Govt Data...</p>';

    try {
        // Call the Python API we just made
        const response = await fetch('/api/govt_stores');
        const stores = await response.json();

        // Clear the list
        list.innerHTML = '';

        // Add each store to the UI
        stores.forEach(store => {
            const item = document.createElement('div');
            item.style = "background: #fdfce7; padding: 10px; border-radius: 8px; border: 1px solid #fef08a;";
            item.innerHTML = `
                <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:13px;">
                    <span>${store.name}</span>
                    <span style="color:#854d0e;">${store.distance}</span>
                </div>
                <div style="font-size:11px; color:#666; margin-top:4px; display:flex; gap:10px;">
                    <span>${store.type}</span>
                    <span style="color:green; font-weight:600;">• ${store.stock}</span>
                </div>
            `;
            list.appendChild(item);
        });

    } catch (error) {
        console.error(error);
        list.innerHTML = '<p style="color:red;">Error fetching data.</p>';
    }
}
// --- 5. MAP LOGIC (Leaflet.js) ---
let mapInitialized = false;

function loadMap() {
    if (mapInitialized) return; // Don't reload if already open
    
    // 1. Initialize the map (Centered on a sample location in India)
    // In a real app, we would use navigator.geolocation to get real user location
    const map = L.map('map').setView([28.6139, 77.2090], 13); // New Delhi Coordinates

    // 2. Add the "Skin" (OpenStreetMap - Free)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // 3. Add Pins (Markers) for Govt Stores
    const stores = [
        { lat: 28.6139, lng: 77.2090, title: "PM Jan Aushadhi Kendra (Sec 4)" },
        { lat: 28.6200, lng: 77.2100, title: "Civil Hospital Blood Bank" },
        { lat: 28.6100, lng: 77.2000, title: "Anganwadi Center 12" }
    ];

    stores.forEach(store => {
        L.marker([store.lat, store.lng])
            .addTo(map)
            .bindPopup(`<b>${store.title}</b><br>Stock: Available`);
    });

    mapInitialized = true;
    alert("Map Loaded! Look for the Blue Pins 📍");
}
// --- 6. WELLNESS LOGIC ---
async function fetchWellness() {
    const card = document.getElementById('wellness-card');
    
    // Toggle visibility (Show/Hide)
    if (card.style.display === 'block') {
        card.style.display = 'none';
        return;
    }
    card.style.display = 'block';

    // Show loading state
    document.getElementById('cal-target').innerText = "Calculating personal needs...";

    try {
        const response = await fetch('/api/get_wellness_plan');
        const data = await response.json();

        // 1. Update Calories
        document.getElementById('cal-target').innerText = data.calories;

        // 2. Build Meal List
        const mealBox = document.getElementById('meal-list');
        mealBox.innerHTML = ''; // Clear old
        data.meals.forEach(m => {
            mealBox.innerHTML += `
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <span><b>${m.time}:</b> ${m.food}</span>
                    <span style="color:#10b981;">${m.cal} cal</span>
                </div>
            `;
        });

        // 3. Build Exercise Chips
        const exBox = document.getElementById('exercise-list');
        exBox.innerHTML = ''; // Clear old
        data.exercises.forEach(ex => {
            exBox.innerHTML += `
                <div style="min-width:100px; background:#f0fdf4; padding:8px; border-radius:8px; border:1px solid #bbf7d0; text-align:center;">
                    <div style="font-weight:bold; font-size:12px; color:#166534;">${ex.name}</div>
                    <div style="font-size:10px; color:#15803d;">${ex.duration}</div>
                </div>
            `;
        });

    } catch (error) {
        console.error("Error fetching wellness plan", error);
        document.getElementById('cal-target').innerText = "Error loading plan.";
    }
}