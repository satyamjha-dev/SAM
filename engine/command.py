import os
import speech_recognition as sr
import eel
import time

VOICE = "Samantha"
RATE = 120  # words per minute


def ui_call(func, *args):
    """Safe Eel call (prevents AttributeError)"""
    try:
        getattr(eel, func)(*args)
    except Exception:
        pass


def speak(text):
    text = str(text)

    # UI updates (safe)
    ui_call("DisplayMessage", text)
    ui_call("receiverText", text)

    # macOS native TTS
    os.system(f'say -v {VOICE} -r {RATE} "{text}"')


def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        ui_call("DisplayMessage", "listening....")

        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=10, phrase_time_limit=6)

    try:
        print('recognizing....')
        ui_call("DisplayMessage", "recognizing....")

        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")

        ui_call("DisplayMessage", query)
        time.sleep(1)

        return query.lower()

    except Exception as e:
        print("Speech error:", e)
        return ""


@eel.expose
def allcommand(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        # eel.senderText(query)
    else:
        query = message
        # eel.senderText(query)
    try:
        print("Final query:", query)

        if not query:
            return

        if "youtube" in query and "play" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "message" in query or "call" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "video" in query:
                    flag = 'video call'
                else:
                    flag = 'call'
                    
                whatsApp(contact_no, query, flag, name)


        else:
            print("Command not matched")

    except Exception as e:
        print("Main error:", e)

    ui_call("ShowHood")