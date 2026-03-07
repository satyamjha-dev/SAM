# SAM (Satyam's Automated Machine)

SAM is an intelligent, voice-controlled virtual assistant built with Python. It features a modern web-based UI powered by the Eel library, background hotword detection, speech recognition, and an SQLite database to seamlessly manage system applications and user commands.

## 🚀 Features

- **Voice Interaction:** Listens and responds to commands via the `speech_recognition` package and native macOS Text-to-Speech (TTS).
- **Wake Word Detection:** Always-on background listening using `pvporcupine` for the "hey-sam" hotword.
- **Web-based UI:** A sleek graphical user interface created with HTML, CSS, and JS linked to Python using the `eel` framework.
- **Application Automation:** Opens Mac system applications (Chrome, VSCode, Safari, etc.) quickly. Paths are managed and dynamically queried from a local SQLite database (`sam.db`).
- **Web Navigation & YouTube:** Automatically searches and plays requested videos on YouTube, or opens websites dynamically if an app is not found locally.
- **Multiprocessing Support:** Runs UI processes and hotword listening simultaneously using Python's `multiprocessing`.

## 🛠️ Technologies & Libraries Used

- **Python 3**
- **Eel:** For the frontend-backend communication (Chrome App Mode).
- **SpeechRecognition:** To recognize voice input commands.
- **Pvporcupine:** Keyword detection engine.
- **SQLite3:** Relational database for system commands & paths.
- **PyAudio / Pygame:** For audio streaming and playing sounds.
- **PyWhatKit:** To perform automation tasks like playing YouTube videos.

## 📂 Project Structure

- `run.py` - The main entry point. Orchestrates multiprocessing streams for the start UI and hotword listener.
- `main.py` - Initializes the UI and starts Eel.
- `engine/` - Core internal processing modules.
  - `features.py` - Core logic for command execution, YouTube playback, and hotword handling.
  - `command.py` - Handles capturing user voice via mic and TTS operations.
  - `db.py` - Sets up the SQLite database and populates initial app records.
  - `config.py` - Global configurations.
- `sam.db` - The underlying SQLite database that stores application paths.
- `www/` - The web assets directory containing the HTML, CSS, and JS files for the frontend UI.
- `hey-sam_en_mac_v4_0_0.ppn` - The Picovoice hotword model file for triggering SAM.

## 🚧 Status

I am still working on it.
