import os
import eel


from engine.features import *
from engine.command import *

def start():
    eel.init("www")

    playsoundwww()

    # For macOS
    os.system('open -a "Google Chrome" --args --app="http://127.0.0.1:8000/index.html"')

    eel.start("index.html", mode=None, host='localhost', port=8000, block=True)
