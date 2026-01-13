# HospiBot - Hospital Information Assistant 🏥

HospiBot is a specialized, production-ready chatbot designed to assist hospital visitors with non-medical queries. It strictly refuses medical advice and provides accurate information about hospital services, doctors, and scheduling.

## 🌟 Features

-   **Strict Medical Refusal**: Safely detects and refuses medical/symptom-related queries.
-   **Live Dashboard**: Real-time visualization of ER Wait Times, Visiting Status, and Department Capacity.
-   **Tabbed Interface**: Clean separation between Chat, Live Stats, and Resources.
-   **Dynamic Data**: Loads hospital information (Contacts, Doctors, Departments) from a structured JSON source.
-   **Premium UI**: Custom "Glassmorphism" design with a Modern Teal theme.

## 🛠️ Tech Stack

-   **Frontend**: Streamlit (Python)
-   **Backend**: FastAPI
-   **Logic**: LangGraph (State management & Routing)
-   **Data**: JSON (Single Source of Truth)

## 🚀 Getting Started

### Prerequisites

-   Python 3.9+
-   pip

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/ManthanBohra/HospiBot--Hospital-Information-Assistant.git
    cd HospiBot--Hospital-Information-Assistant
    ```

2.  **Create a Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Create a requirements.txt with `pip freeze > requirements.txt` if not present)*

### Running the App

1.  **Start the Backend** (Terminal 1)
    ```bash
    source venv/bin/activate
    uvicorn backend.main:app --reload --port 8000
    ```

2.  **Start the Frontend** (Terminal 2)
    ```bash
    source venv/bin/activate
    streamlit run frontend/app.py
    ```

3.  Access the app at `http://localhost:8501`.

## 📂 Project Structure

```
HospiBot/
├── backend/            # FastAPI Backend
│   ├── app/
│   │   ├── graph.py    # LangGraph Logic
│   │   └── ...
│   └── main.py         # Entry Point
├── frontend/           # Streamlit Frontend
│   └── app.py          # UI Logic
├── data/               # Static Data
│   └── hospital_info.json
└── README.md
```

## 🛡️ Safety & Disclaimer

**HospiBot is NOT a medical device.** It is programmed to strictly refuse any requests for medical diagnosis, treatment, or advice. In case of emergency, it provides the hospital's emergency contact number.
