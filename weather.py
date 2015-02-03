__module_name__ = 'weather'
__module_version__ = '1.0'
__module_description__ = 'What is the weather?'
__module_author__ = 'Allen Stetson'

# To link:
# ln -s ~allen/bin/weather.py

import xchat
import sys
sys.path.insert(0, '/work/td/xchat/mod/')
from dnd.environment import EnvirGenerator

def print_help():
    context = xchat.get_context()
    printStr = []
    printStr.append("/weather Syntax:")
    printStr.append("/weather or /weather short")
 
    context.prnt(str("\n").join(printStr))

def weather_app(word, word_eol, userdata):
    # Get the xchat context and the channel you are in.
    context = xchat.get_context()
    channel = xchat.get_info('channel')

    # Initialize the output string.
    # This is actually a list of strings, one per line.
    printStr = []
    
    weather = EnvirGenerator()
    graphic = getGraphic()
    printStr.append(graphic)
    printString = weather.getWeather()
    printStr.append(printString)
    graphic = getEndGraphic()
    printStr.append(graphic)

    for text in printStr:
        #context.command("say " + str("\n").join(printStr))
        context.command("say " + text)
    
    return xchat.EAT_ALL
    
def getGraphic():
    return("================")
    
def getEndGraphic():
    return("================")

xchat.hook_command("weather", weather_app)
xchat.prnt("/weather successfully loaded.")
