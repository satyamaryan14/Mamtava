# Mamtava: Maa ki Mamta, Science ka Bharosa. 🌸

>  *Bridging the gap between Rural Mothers and Medical Care.*

**Mamtava** is a **Real-Time, AI-Powered Maternal Health Ecosystem** designed specifically for **Rural India**. It empowers expecting mothers with vernacular voice support while providing doctors with a live, autonomous triage dashboard.

---

## 🚩 The Problem
According to **NFHS-5 Data**, rural India faces a critical maternal health crisis:
* **Language Barrier:** Most health apps are in English; rural mothers speak dialects like *Bhojpuri* or *Maithili*.
* **The "Golden Hour" Delay:** In emergencies, connecting to a doctor takes too long.
* **Information Overload:** Doctors cannot monitor hundreds of healthy patients to find the one at risk.

---

## 💡 The Solution: Mamtava 2.0
Mamtava is not just a tracker; it is an **Intelligent Real-Time Triage System**.

### 🌟 Key Features
* **🗣️ Multilingual Voice AI:** Mothers can speak in **Hindi, Bhojpuri, Maithili, Kannada, or Gujarati**. The system translates, analyzes symptoms, and speaks back medical advice in their own accent.
* **🚨 Zero-Latency SOS:** Powered by **WebSockets (Socket.IO)**. When a mother presses "SOS", the Doctor's dashboard flashes **Red** instantly—faster than an SMS.
* **🧠 Predictive Risk AI:** A custom **Random Forest Machine Learning Model** predicts risks (Preeclampsia/Anemia) based on vitals and voice sentiment.
* **⚡ Hybrid Doctor Dashboard:** Built with **React.js** embedded in Flask for high-performance, real-time patient monitoring without page reloads.
* **🗺️ Jan Aushadhi Map:** Automatically finds the nearest affordable government pharmacy using Open Govt Data.

---

## ⚙️ Technology Stack (Hybrid Architecture)
* **Frontend:** HTML5, Tailwind CSS, **React.js** (Doctor Portal), Leaflet.js (Maps).
* **Backend:** Python (**Flask**), **Flask-SocketIO** (Real-Time Engine).
* **AI & NLP:**
    * **GoogleTrans API:** For real-time translation of 5+ Indian languages.
    * **Scikit-Learn:** Random Forest Classifier for Risk Prediction.
    * **TextBlob:** Sentiment Analysis of voice notes.
    * **Web Speech API:** Native browser-based speech recognition.

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone [https://github.com/satyamaryan14/Mamtava.git](https://github.com/satyamaryan14/Mamtava.git)
cd Mamtava

### Steps
1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/satyamaryan14/Mamtava.git](https://github.com/satyamaryan14/Mamtava.git)
    cd Mamtava
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**
    ```bash
    python app.py
    ```

4.  **Access the App**
    * **Patient App:** Open `http://127.0.0.1:5000/` in your browser.
    * **Doctor Dashboard:** Open `http://127.0.0.1:5000/doctor` in a second tab.

---

## 📸 Project Screenhots
*(Add screenshots here after you run the app)*

---

## 🔮 Future Roadmap
1.  **Hardware Integration:** Connect with Bluetooth BP monitors for automated logging.
2.  **Vernacular Video:** Add "Didi" video bot for illiterate users.
3.  **Govt Integration:** Sync data with Ayushman Bharat Health Account (ABHA).
