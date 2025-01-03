import os
import sys
sys.path.append('A:/project/Lyra')
from shlex import quote
import google.generativeai as genai
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine
import requests
from engine.helper import extract_yt_term, remove_words

con = sqlite3.connect("lyra.db")
cursor = con.cursor()
api_key_gen = "AIzaSyD0-YO5ipWwgP_peZgoiHgJQTBx78pxv5M"
api_key_weather="64077e46d9d0293f06e86dfd2d905d75"
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    
    # Make the query lowercase to ignore case differences
    app_name = query.strip().lower()

    if app_name != "":

        try:
            # Modify the query to search case-insensitively in the database
            cursor.execute(
                'SELECT path FROM sys_command WHERE LOWER(name) = ?', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                    'SELECT url FROM web_command WHERE LOWER(name) = ?', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("Not found")
        except:
            speak("Something went wrong")
       

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["lyra","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        lyra_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        lyra_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        lyra_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(lyra_message)


# Weather API
def WeatherApi(query):
    
    api_key = api_key_weather
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": query,
        "appid": api_key,
        "units": "metric"  # For temperature in Celsius; use "imperial" for Fahrenheit
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        city_name = data["name"]
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        weather_report = f"The current weather in {city_name} is {weather_desc} with a temperature of {temp:.2f}°C."
      
      
        print(weather_report)
        speak(weather_report)
      
        return weather_report
    else:
        return "Failed to fetch weather data. Please check the city name or API key." 

# chat bot 


def chatBot(query, chat_history=None, model_name="gemini-2.0-flash-exp", max_tokens=128):
    """
    Handles interaction with a generative AI chatbot.

    Args:
        query (str): User's input query.
        chat_history (list, optional): List of previous conversation turns for context. Defaults to an empty list.
        model_name (str, optional): Name of the AI model to use. Defaults to "gemini-2.0-flash-exp".
        max_tokens (int, optional): Maximum number of tokens in the response. Defaults to 128.

    Returns:
        str: Response from the chatbot.
    """
    # Configure the generative AI model
    try:
        genai.configure(api_key=api_key_gen)
    except Exception as e:
        print(f"Error configuring generative AI: {e}")
        return "An error occurred while setting up the AI model."

    # Create the generation configuration
    generation_config = {
        "temperature": 0.3,
        "top_p": 0.8,
        "top_k": 20,
        "max_output_tokens": max_tokens,
        "response_mime_type": "text/plain",
    }

    # Initialize the generative AI model
    try:
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
        )
    except Exception as e:
        print(f"Error initializing the AI model: {e}")
        return "An error occurred while initializing the AI model."

    # Start a new chat session or use provided history
    chat_history = chat_history if chat_history else []
    try:
        chat_session = model.start_chat(history=chat_history)
    except Exception as e:
        print(f"Error starting chat session: {e}")
        return "An error occurred while starting the chat session."

    # Send the user's query to the chat model
    try:
        response = chat_session.send_message(query)
        response_text = response.text.replace("*", "")
    except Exception as e:
        print(f"Error sending message: {e}")
        return "An error occurred while communicating with the AI."

    # Print and speak the response
    print(response_text)
    speak(response_text)

    return response_text


# def chatBot(query):
#     # Configure the generative AI model
#     genai.configure(api_key=api_key_gen)

#     # Create the generation configuration
#     generation_config = {
#         "temperature": 0.5,
#         "top_p": 0.95,
#         "top_k": 40,
#         "max_output_tokens": 128,
#         "response_mime_type": "text/plain",
#     }

#     # Initialize the generative AI model
#     model = genai.GenerativeModel(
#         model_name="gemini-2.0-flash-exp",
#         generation_config=generation_config,
#     )

#     # Start a new chat session
#     chat_session = model.start_chat(
#         history=[]
#     )

#     # Send the user's query to the chat model
#     response = chat_session.send_message(query)

#     # Extract the response text
#     response_text = response.text
#     response_text = response_text.replace("*","")

#     # Print and speak the response
#     print(response_text)
#     speak(response_text)

#     return response_text


# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(136, 2220)
    #start chat
    tapEvents(819, 2192)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 2270)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1397)
    speak("message send successfully to "+name)