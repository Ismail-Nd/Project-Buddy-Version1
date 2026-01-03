# Intelligent Voice Assistant (AI-Powered)

An advanced Python-based voice assistant that combines fast, local speech recognition with a cloud-based AI brain. It understands complex intents, handles phonetic errors, and executes system/web commands with a human-like interaction flow.

## 🚀 Key Features

- **Persistent Wake Session**: Say "Hey PC" once and give multiple commands sequentially without repeating the wake word.
- **Gemini AI Integration**: Uses the Gemini API to decipher messy speech (e.g., "hoping you tube" -> "Open YouTube") and handle open-ended search queries.
- **Local Speech Recognition**: Built on **Vosk** for near-instant, offline speech-to-text.
- **Smart Fallback**: Prioritizes direct/fuzzy matching for speed, then falls back to AI for complex tasks.
- **Autonomous Search**: Automatically Googles answers to questions it doesn't recognize as system commands.
- **Fast Startup**: No long calibration delays; starts listening immediately.

## 🛠️ Technical Stack

- **Lanuage**: Python 3.10+
- **Speech-to-Text**: [Vosk](https://alphacephei.com/vosk/)
- **AI Engine**: [Google Gemini API](https://aistudio.google.com/)
- **Audio I/O**: SoundDevice, NumPy
- **Environment**: Python-dotenv

## 📋 Requirements

Ensure you have the following installed:
- Python 3.10 or higher
- A microphone (internal or external)
- A Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

## ⚙️ Setup & Installation

### 1. Clone the Project
```powershell
git clone <your-repo-url>
cd <project-folder>
```

### 2. Create a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Download the Vosk Model
1. Visit [Vosk Models](https://alphacephei.com/vosk/models).
2. Download a model (e.g., `vosk-model-small-en-us-0.15`).
3. Extract it into a folder named `models/vosk` in the project root.

### 5. Configure API Key
1. Create a file named `.env` in the root directory.
2. Add your Gemini API Key:
   ```text
   GEMINI_API_KEY=your_actual_key_here
   ```

## 🎤 Usage

1. Run the main script:
   ```powershell
   python main.py
   ```
2. **Wake Word**: Say "**Hey PC**" (or "Hey C", "A PC").
3. **Give Commands**:
   - "*Open Chrome*"
   - "*Open YouTube*"
   - "*Search for the latest space news*"
4. **Persistent Session**: After the first command, you can keep speaking for up to 20 seconds without saying "Hey PC" again.
5. **Sleep**: Say "**Go to sleep**", "**Stop listening**", or "**Goodbye**" to put the assistant back to idle.

## 📄 License
MIT License. Feel free to use and modify for your own projects!
