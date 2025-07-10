# 💡 Innovize: AI-Powered Innovation Platform

<div align="center">
  <img src="https://raw.githubusercontent.com/user-attachments/assets/53545b7f-a631-4e6f-827d-0e42fce81a5c" alt="Innovize Banner" width="800"/>
</div>

<p align="center">
  <strong>Transform raw ideas into refined concepts.</strong>
  <br />
  Innovize is a lightweight, zero-auth web platform that uses Google's Gemini AI to instantly evaluate, refine, and visualize crowdsourced ideas.
  <br />
  <br />
  <a href="#-key-features"><strong>Features</strong></a> ·
  <a href="#-tech-stack"><strong>Tech Stack</strong></a> ·
  <a href="#-getting-started"><strong>Getting Started</strong></a> ·
  <a href="#-how-to-run"><strong>How to Run</strong></a>
</p>

---

## ✅ Key Features

Innovize is built to be fast, intelligent, and frictionless. Just submit an idea and see the results instantly.

-   **📝 Multimodal Idea Submission**: Submit ideas via rich text (markdown) and supporting documents (PDFs, Images).
-   **🤖 Gemini-Powered Evaluation**: Uses Google's Gemini AI (`gemini-1.5-flash`) to generate an instant scorecard on your idea's:
    -   Technical Feasibility
    -   Market Potential
    -   Innovation Rating
    -   Sustainability Relevance
-   **🧠 AI-Driven Refinements**: Get immediate suggestions to improve your idea's title, summary, and structure.
-   **📊 ML Clustering & Visualization**: Similar ideas are automatically clustered and visualized on an interactive dashboard, helping to identify trends and innovation hotspots.
-   **🚀 Zero-Auth & Anonymous**: No accounts, no logins, no friction. All submissions are processed on the fly without storing user data.
-   **⚙️ Mock Mode**: Runs with pre-programmed dummy data if no API key is provided, perfect for offline development and testing the UI.

## 🛠️ Tech Stack

This project uses a simple and powerful stack, with a Python backend and a single-page vanilla JS frontend.

| Category      | Technology                                                                                                                              |
| :------------ | :-------------------------------------------------------------------------------------------------------------------------------------- |
| **Backend**   | <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" /> <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" /> |
| **AI Engine** | <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google-gemini&logoColor=white" />                   |
| **Frontend**  | <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" /> <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" /> <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white" /> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" /> |
| **Data & ML** | <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" /> <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" /> <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" /> |
| **OCR**       | <img src="https://img.shields.io/badge/Tesseract-000000?style=for-the-badge&logo=tesseract&logoColor=white" />                             |

---

## 🚀 Getting Started

Follow these steps to get a local copy of Innovize up and running.

### Prerequisites

1.  **Python (3.8+):** Make sure Python is installed and added to your system's PATH.
    ```sh
    python --version
    ```
2.  **Tesseract OCR Engine:** Required for extracting text from image uploads.
    -   **On macOS (Homebrew):**
        ```sh
        brew install tesseract
        ```
    -   **On Ubuntu/Debian:**
        ```sh
        sudo apt-get install tesseract-ocr
        ```
    -   **On Windows:** Download and run the installer from the [Tesseract at UB Mannheim repository](https://github.com/UB-Mannheim/tesseract/wiki). **Remember to add the installation folder to your system's PATH variable.**

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/your-username/innovize.git
    cd innovize
    ```

2.  **Create and activate a Python virtual environment:**
    ```sh
    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # On Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
    You should see `(venv)` appear in your terminal prompt.

3.  **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your API Key (for full AI functionality):**
    -   Rename the `.env.example` file to `.env`.
    -   Open the `.env` file and paste in your Google Gemini API key. You can get one from [Google AI Studio](https://aistudio.google.com/).
        ```
        GOOGLE_API_KEY="your-gemini-api-key-here"
        ```
    -   **Note:** If you leave the key blank, the app will run in **Mock Mode** with dummy data.

---

## ▶️ How to Run

With the setup complete, running the application is just one command away.

1.  **Start the Flask development server:**
    ```sh
    flask run
    ```

2.  **Open your web browser** and navigate to the local address provided:
    > **http://127.0.0.1:5000**

You can now start submitting ideas to Innovize! To stop the server, press `CTRL+C` in your terminal.
