import platform
from shlex import quote
import struct
import subprocess
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

from engine.helper import remove_words

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


#find contacts
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'wahtsapp', 'video', 'voice']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        
        # Clean the number: Handle multiple numbers split by ":::" or ","
        mobile_number_str = mobile_number_str.split(':::')[0].strip()
        mobile_number_str = mobile_number_str.split(',')[0].strip()
        
        # Extract only digits
        import re
        mobile_number_str = re.sub(r'[^0-9]', '', mobile_number_str)
        
        # Prepend country code '91' if length is 10
        if len(mobile_number_str) == 10:
            mobile_number_str = '91' + mobile_number_str
        elif mobile_number_str.startswith('0') and len(mobile_number_str) == 11:
            mobile_number_str = '91' + mobile_number_str[1:]

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
#### 9. Create Whatsapp Function in features.py
from urllib.parse import quote as url_quote

def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        jarvis_message = "message send successfully to " + name
        encoded_message = url_quote(message)
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        subprocess.run(["open", whatsapp_url])
        time.sleep(5)
        # On macOS WhatsApp, opening the URL directly puts focus on the text box.
        pyautogui.press('enter')

    elif flag == 'call':
        jarvis_message = "calling to " + name
        whatsapp_url = f"whatsapp://send?phone={mobile_no}"
        subprocess.run(["open", whatsapp_url])
        time.sleep(5)
        # Trigger Voice Call via AppleScript
        applescript = '''
        tell application "System Events"
            if exists process "WhatsApp" then
                tell process "WhatsApp"
                    set frontmost to true
                    delay 1
                    try
                        set chatMenu to first menu bar item of menu bar 1 whose name contains "Chat"
                        set callItem to first menu item of menu 1 of chatMenu whose name contains "Voice Call"
                        click callItem
                    on error
                        try
                            set callItem to first menu item of menu 1 of chatMenu whose name contains "Audio Call"
                            click callItem
                        on error
                            keystroke "d" using {command down, shift down}
                        end try
                    end try
                end tell
            end if
        end tell
        '''
        subprocess.run(["osascript", "-e", applescript])

    else:
        jarvis_message = "starting video call with " + name
        whatsapp_url = f"whatsapp://send?phone={mobile_no}"
        subprocess.run(["open", whatsapp_url])
        time.sleep(5)
        # Trigger Video Call via AppleScript
        applescript = '''
        tell application "System Events"
            if exists process "WhatsApp" then
                tell process "WhatsApp"
                    set frontmost to true
                    delay 1
                    try
                        set chatMenu to first menu bar item of menu bar 1 whose name contains "Chat"
                        set callItem to first menu item of menu 1 of chatMenu whose name contains "Video Call"
                        click callItem
                    on error
                        keystroke "v" using {command down, shift down}
                    end try
                end tell
            end if
        end tell
        '''
        subprocess.run(["osascript", "-e", applescript])

    speak(jarvis_message)