# Mamtava: Maa ki Mamta, Science ka Bharosa.
### (Formerly Little Bloom)

**Mamtava** is an AI-powered maternal health ecosystem designed specifically for **Rural India**. It bridges the gap between expecting mothers in remote villages and proper medical care using **Offline-First AI** and **Voice Interactions**.

---

## 🚩 The Problem (Why we built this)
According to **NFHS-5 Data**, rural India faces a critical maternal health crisis:
1.  **54.1% of rural women are Anemic**, leading to high risk of complications.
2.  **The "4-Visit Gap":** Only 58% of rural mothers complete the required 4 Antenatal Care (ANC) visits.
3.  **Device Gap:** 58% of rural women access the internet via shared devices, making standard apps unusable.

## 💡 The Solution: Mamtava
Mamtava is not just a tracker; it is an intelligent triage system.

### Key Features:
* **🗣️ Voice-First AI:** Mothers can speak symptoms ("I feel dizzy") in their local language. The AI analyzes sentiment and clinical keywords to detect risks like **Preeclampsia** or **Anemia**.
* **📡 Offline-Ready:** Works in low-network areas. Data syncs when connectivity is available.
* **🏥 Smart Doctor Dashboard:** Doctors don't see raw data. They see a **Prioritized Risk List** (Critical/High/Low) powered by our Random Forest Logic.
* **📍 Jan Aushadhi Map:** Automatically finds the nearest affordable government pharmacy (PMBJP Kendras) using Open Govt Data.

---

## ⚙️ Technology Stack
* **Backend:** Python (Flask)
* **AI Engine:** TextBlob (Sentiment Analysis) + Custom Risk Algorithm
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
* **Mapping:** Leaflet.js + OpenStreetMap
* **Data Source:** Open Government Data (OGD) Platform & NFHS-5 Reports

---

## 🚀 How to Run Locally

### Prerequisites
* Python 3.x installed

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