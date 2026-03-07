import re
def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None

# def takecommand():

#     r = sr.Recognizer()

#     with sr.Microphone() as source:
#         print('listening....')
#         eel.DisplayMessage('listening....')
#         r.pause_threshold = 1
#         r.adjust_for_ambient_noise(source)
        
#         audio = r.listen(source, 10, 6)

#     try:
#         print('recognizing')
#         eel.DisplayMessage('recognizing....')
#         query = r.recognize_google(audio, language='en-in')
#         print(f"user said: {query}")
        
        
#         eel.DisplayMessage(query)
#         time.sleep(2)
        
       
#     except Exception as e:
#         return ""
    
#     return query.lower()

# @eel.expose
# def allcommand():


#     try:
#         query = takecommand()
#         print(query)
#         if "open" in query:
#             from engine.features import openCommand
#             openCommand(query)
#         elif "on youtube":
#             from engine.features import PlayYoutube
#             PlayYoutube(query)
#         else:
#                 print("not run")
#     except:
#         print("error")

#     eel.ShowHood()


