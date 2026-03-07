import platform
import struct
import pyaudio
import pyautogui
import pygame
import os
import re
import time
import eel
import webbrowser
import speech_recognition as sr

from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import pvporcupine
import sqlite3

import os

# replace with the actual path to your database file
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, '..', 'sam.db')
db_path = os.path.abspath(db_path)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

@eel.expose
def playsoundwww():
    music_dir = "Assests/audio/sound.mp3"
    pygame.mixer.init()
    pygame.mixer.music.load(music_dir)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip()
    query = query.lower()

    app_name = query

    if app_name != "":
        try:
            cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = ?', (app_name.lower(),))
            results = cursor.fetchall()

            if results:
                speak("Opening " + app_name)
                app_path = results[0][0]
                if platform.system() == "Darwin":  # macOS
                    os.system(f'open "{app_path}"')
                elif platform.system() == "Linux":
                    os.system(f'xdg-open "{app_path}"')
                else:  # Windows
                    os.startfile(app_path)

            else:
                speak("Opening " + app_name)
                try:
                    import webbrowser
                    website = app_name.replace(" ", "")
                    webbrowser.open(f"https://www.{website}.com")
                except Exception as e:
                    print("Browser fallback error:", e)
                    speak("Not found")

        except Exception as e:
            print("Database or execution error:", e)
            speak("Something went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)

def extract_yt_term(command):
    pattern = r'play\s+(.*?)(?:\s+on\s+youtube|$)'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1).strip() if match else command.replace("play", "").strip()
def hotword():
    porcupine=None
    paud=None
    audio_stream=None 
    try:
       
        # pre trained keywords    
        porcupine = pvporcupine.create(
    access_key="Rryz6896x7Sf672kJ5jFlPTRAvH7ppAApxkYv01HYUnV6xsvUOpNUg==",
    keyword_paths=["engine/hey-sam_en_mac_v4_0_0.ppn"]
)
        paud=pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            input_device_index=0,
            frames_per_buffer=porcupine.frame_length
        )
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index >= 0:
                print("hotword detected")

                # temporarily stop mic stream before triggering UI
                audio_stream.stop_stream()
                audio_stream.close()

                import pyautogui as autogui
                if platform.system() == "Darwin":  # macOS
                    autogui.keyDown("command")
                    autogui.press("j")
                    time.sleep(0.5)
                    autogui.keyUp("command")
                else:  # Windows
                    autogui.keyDown("win")
                    autogui.press("j")
                    time.sleep(0.5)
                    autogui.keyUp("win")

                # wait for UI interaction to finish
                time.sleep(3)

                # restart microphone stream so hotword works again
                audio_stream = paud.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    input_device_index=0,
                    frames_per_buffer=porcupine.frame_length
                )
                
    except Exception as e:
        print(f"Hotword Error: {e}")
        print("Note: If the error is regarding a missing AccessKey, you need to sign up at Picovoice console and pass access_key='YOUR_KEY' to pvporcupine.create()")
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()