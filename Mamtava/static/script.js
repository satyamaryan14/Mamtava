// --- 1. CONFIGURATION & SETUP ---
    const socket = io();
    let map;
    let currentLang = 'en';

    // Language Mapping for Voice (Chrome/Web Speech API)
    // Maithili (mai), Bhojpuri (bho), Angika (hi) -> Mapped to Hindi (hi-IN)
    const voiceCodes = {
        'en': 'en-US',
        'hi': 'hi-IN',
        'mai': 'hi-IN', 
        'bho': 'hi-IN',
        'kn': 'kn-IN',  // Kannada
        'gu': 'gu-IN'   // Gujarati
    };

    // --- 2. SMART LANGUAGE SWITCHER (Calls Python API) ---
    async function changeLang() {
        // Get selected language
        currentLang = document.getElementById('lang').value;
        
        // Visual Feedback
        document.getElementById('voice-title').innerText = "Translating...";
        document.getElementById('voice-sub').innerText = "Please wait...";

        try {
            // Call Python to translate the UI text
            const res = await fetch('/api/translate_ui', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ lang: currentLang })
            });
            
            const txt = await res.json();
            
            // Update the Screen with Translated Text
            document.getElementById('greet').innerText = txt.greet;
            document.getElementById('sos-txt').innerText = txt.sos;
            document.getElementById('voice-title').innerText = txt.voice_title;
            document.getElementById('voice-sub').innerText = txt.voice_sub;
            document.getElementById('diet-title').innerText = txt.diet;
            document.getElementById('map-title').innerText = txt.map;

        } catch (err) {
            console.error("Translation Error:", err);
            document.getElementById('voice-title').innerText = "Translation Failed";
        }
    }

    // --- 3. VOICE AI (Sends Language + Text) ---
    function startListening() {
        const btn = document.getElementById('mic-btn');
        const resultBox = document.getElementById('ai-result');
        
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) { alert("Voice features require Chrome or Edge."); return; }

        const recognition = new SpeechRecognition();
        
        // IMPORTANT: Set the microphone to the correct regional accent
        recognition.lang = voiceCodes[currentLang] || 'en-US';
        
        btn.classList.add('voice-wave');
        recognition.start();

        recognition.onresult = async (event) => {
            btn.classList.remove('voice-wave');
            const text = event.results[0][0].transcript;
            
            // Show "Thinking" UI
            resultBox.classList.remove('hidden');
            document.getElementById('ai-risk').innerText = `"${text}"`;
            document.getElementById('ai-advice').innerText = "Consulting AI Doctor...";

            try {
                // SEND TEXT AND LANGUAGE TO PYTHON
                const response = await fetch('/api/analyze_voice', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        text: text, 
                        lang: currentLang // <--- Sending language code (e.g., 'bho')
                    })
                });
                const data = await response.json();

                // Display Translated Results
                const riskColor = data.risk === "Critical" ? "text-red-600" : (data.risk === "High" ? "text-orange-600" : "text-green-600");
                document.getElementById('ai-risk').className = `font-bold text-lg mt-1 ${riskColor}`;
                
                // Show translated Risk & Advice
                document.getElementById('ai-risk').innerText = data.risk_display; 
                document.getElementById('ai-advice').innerText = data.action;
                
                // Speak out the advice in the regional language!
                if(data.risk !== "Low") {
                    const utterance = new SpeechSynthesisUtterance(data.action);
                    utterance.lang = voiceCodes[currentLang]; // Speak in Bhojpuri/Kannada etc.
                    window.speechSynthesis.speak(utterance);
                }
            } catch (err) {
                document.getElementById('ai-advice').innerText = "Error connecting to AI.";
            }
        };

        recognition.onerror = () => {
            btn.classList.remove('voice-wave');
            alert("Could not hear you. Please try again.");
        };
    }

    // --- 4. SOS LOGIC (Real-Time) ---
    function triggerSOS() {
        if(confirm("🚨 Are you sure? This will alert the Ambulance.")) {
            socket.emit('trigger_sos', { lat: "28.6139", lng: "77.2090" });
            alert("🚑 SOS SENT! Doctor has been alerted.");
        }
    }

    // --- 5. WELLNESS PLAN ---
    async function loadWellness() {
        const box = document.getElementById('wellness-content');
        box.innerHTML = '<p class="text-xs text-green-600 animate-pulse">Fetching Personal Plan...</p>';
        try {
            const res = await fetch('/api/get_wellness_plan');
            const data = await res.json();
            box.innerHTML = data.meals.map(m => `
                <div class="flex justify-between text-sm border-b border-gray-50 pb-2">
                    <span class="font-bold text-gray-700">${m.time}</span>
                    <span class="text-gray-500">${m.food}</span>
                </div>
            `).join('');
        } catch (err) {
            box.innerHTML = '<p class="text-xs text-red-500">Failed to load plan.</p>';
        }
    }

    // --- 6. MAP LOGIC ---
    function initMap() {
        map = L.map('map').setView([28.6139, 77.2090], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        fetch('/api/govt_stores')
            .then(r => r.json())
            .then(stores => {
                stores.forEach(s => {
                    const lat = 28.6139 + (Math.random() - 0.5) * 0.03;
                    const lng = 77.2090 + (Math.random() - 0.5) * 0.03;
                    L.marker([lat, lng]).addTo(map).bindPopup(`<b>${s.name}</b><br>${s.stock}`);
                });
            })
            .catch(e => console.log("Map Error:", e));
    }
    
    // Start Map
    initMap();

//connecting frontend to flask
const API_URL = "http://127.0.0.1:5000"; // Flask URL

function sendOTP() {
  const mobile = document.getElementById("mobile").value;
  localStorage.setItem("mobile", mobile);

  fetch(`${API_URL}/send-otp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mobile: mobile })
  })
  .then(res => res.json())
  .then(data => {
    alert("OTP sent");
    window.location.href = "otp.html";
  });
}

function verifyOTP() {
  const otp = document.getElementById("otp").value;
  const mobile = localStorage.getItem("mobile");

  fetch(`${API_URL}/verify-otp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mobile: mobile, otp: otp })
  })
  .then(res => res.json())
  .then(data => {
    alert("Login successful");
    window.location.href = "dashboard.html";
  });
}
