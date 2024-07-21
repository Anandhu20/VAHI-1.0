import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from flask import Flask, render_template, request
import anthropic
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
import google.generativeai as genai
import PIL.Image
import keys

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
	engine.say(audio)
	engine.runAndWait()

def wishMe():
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		speak("Good Morning Sir !")

	elif hour>= 12 and hour<16:
		speak("Good Afternoon Sir !") 

	else:
		speak("Good Evening Sir !") 

	assname =("vahi")
	speak("I am your Assistant")
	speak(assname)
	

def username():
    speak("What should i call you sir")
    uname = takeCommand()
    speak("Welcome Mister")
    speak(uname)
    columns = shutil.get_terminal_size().columns
    
    print("#####################".center(columns))
    print("Welcome Mr.", uname.center(columns))
    print("#####################".center(columns))
    
    speak("How can i Help you, Sir")


def takeCommand():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening")
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        
        # Set a shorter pause threshold to capture quicker speech
        r.pause_threshold = 1
        
        audio = r.listen(source)

    try:
        print("Recognizing...")
        speak("Recognizing")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e) 
        print("Unable to Recognize your voice.") 
        speak("Unable to Recognize your voice.")
        return "None"         

    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    
    # Enable low security in gmail
    server.login('your email id', 'your email password')
    server.sendmail('your email id', to, content)
    server.close()

def get_current_location_address(api_key):
    # Geolocation API endpoint
    url = f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&fields=geo"
    
    try:
        # Send GET request to the Geolocation API
        response = requests.get(url)
        
        # Check if response is successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                # Extract address from the response
                address = data.get('location', {}).get('address', 'Address not found')
                return address
            else:
                return "Location not found"
        else:
            return f"Error fetching location: {response.status_code}"
    except Exception as e:
        print("Error:", e)
        return "Error fetching location"


if __name__ == '__main__':
    clear = lambda: os.system('cls')
    
    # This Function will clean any
    # command before execution of this python file
    clear()
    wishMe()
    username()
    
    while True:
        
        query = takeCommand().lower()
        
        # All the commands said by user will be 
        # stored here in 'query' and will be
        # converted to lower case for easily 
        # recognition of command
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 3)
            speak("According to Wikipedia")
            print(results)
            speak(results) 

        elif 'play music' in query or "play song" in query:
            speak("Here you go with music")
            # music_dir = "G:\\Song"
            webbrowser.open("https://www.youtube.com/watch?v=pVkDZueTBpY&list=RDpVkDZueTBpY&start_radio=1")
            

        elif 'the time' in query:
            current_time = datetime.datetime.now()
            # Format the current time as desired (e.g., HH:MM:SS)
            formatted_time = current_time.strftime("%H:%M:%S")
            speak(f"Sir, the time is {formatted_time}")
            print(formatted_time)


        elif 'email to' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "Receiver email address"
                sendEmail(to, content)
                speak("Email has been sent !")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'send a mail' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("To whom should i send?")
                to = input() 
                sendEmail(to, content)
                speak("Email has been sent !")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you, Sir")

        elif 'fine' in query or "good" in query:
            speak("It's good to know that your fine")

        elif "change my name to" in query:
            query = query.replace("change my name to", "")
            assname = query

        elif "change your name" in query:
            speak("What would you like to call me, Sir ")
            assname = takeCommand()
            speak("Thanks for naming me")

        elif "what's your name" in query or "What is your name" in query:
            speak("My friends call me")
            speak(assname)
            print("My friends call me", assname)

        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()

        elif "who made you" in query or "who created you" in query: 
            speak("I have been created by the Team 'Schrodingers Cat'")
            
        elif 'joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)
            
        elif "calculate" in query: 
            try:
                
                client = wolframalpha.Client(keys.api1)
                indx = query.lower().split().index('calculate') 
                query = query.split()[indx + 1:] 
                res = client.query(' '.join(query)) 
                answer = next(res.results).text
                print("The answer is " + answer) 
                speak("The answer is " + answer) 

            except Exception:
                speak("Give Values to Calculate")
                print("Give Values to Calculate")

        elif 'search' in query or 'play' in query or 'open' in query:
            
            query = query.replace("search", "").strip() 
            query = query.replace("play", "").strip()
            query = query.replace("open", "").strip()   
            # Encode the query for the URL
            search_query = query.replace(" ", "+")
            # Format the search URL (using Google as an example)
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url) 

        elif "who am i" in query:
            speak("If you talk then definitely you are a human.")

        elif "why you came to this world" in query:
            speak("Thanks to Team 'Schrodingers Cat'. Further it's a secret")


        elif 'is love' in query:
            speak("It is 7th sense that destroy all other senses")

        elif "who are you" in query:
            speak("I am your virtual assistant created by Team Schrodinger's Cat")

        elif 'reason for you' in query:
            speak("I was created as a Minor project by the Team Schrodinger's Cat")

        elif 'change background' in query:
            ctypes.windll.user32.SystemParametersInfoW(20, 
                                                        0, 
                                                        "Location of wallpaper",
                                                        0)
            speak("Background changed successfully")


        elif 'news' in query:
            
            try: 
                # BBC news api
                # following query parameters are used
                # source, sortBy and apiKey
                query_params = {
                "source": "bbc-news",
                "sortBy": "top",
                "apiKey": keys.api2
                }
                main_url = " https://newsapi.org/v1/articles"
            
                # fetching data in json format
                res = requests.get(main_url, params=query_params)
                open_bbc_page = res.json()
            
                # getting all articles in a string article
                article = open_bbc_page["articles"]
            
                # empty list which will 
                # contain all trending news
                results = []
                
                for ar in article:
                    results.append(ar["title"])
                    
                for i in range(len(results)):
                    
                    # printing all trending news
                    print(i + 1, results[i])
            
                #to read the news out loud for us
                from win32com.client import Dispatch
                speak = Dispatch("SAPI.Spvoice")
                speak.Speak(results)                 
 
            except Exception as e:
                
                print(str(e))


        elif 'lock window' in query:
                speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
                

        elif 'shutdown system' in query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call(['shutdown', '/s', '/t', '0'])
                

        elif "don't listen" in query or "stop listening" in query or "stop" in query:
            speak("Stopping listening for commands.")
            exit()

        elif "pause listening" in query or "pause" in query or "wait" in query:
            speak("For how many seconds would you like me to stop listening?")
            try:
                seconds = int(takeCommand())
                speak(f"Pausing listening for {seconds} seconds.")
                time.sleep(seconds)
                speak("Listening resumed.")

            except ValueError:
                speak("Invalid input. Please say a number.")
            
        elif "locate" in query:
            query = query.replace("locate", "")
            location = query
            speak("User asked to Locate")
            speak(location)
            webbrowser.open("https://www.google.com/maps/place/" +location+ "/@8.9040623,76.5950733,13z?entry=ttu" + "")

        
        elif "current location" in query or "location" in query:
            # Replace 'YOUR_API_KEY' with your actual API key from the Geolocation API provider
            api_key = keys.api3

            # Get and print the current location address
            current_address = get_current_location_address(api_key)
            print("Current Location Address:", current_address)
        
        elif "camera" in query or "take a photo" in query:
            ec.capture(0, "Jarvis Camera ", "img.jpg")

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
            
        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown / h")

        elif "log off" in query or "sign out" in query:
            speak("Make sure all the application are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif "write a note" in query or "open Notepad" in query:
            try:
                # Open Notepad using subprocess
                subprocess.Popen(["notepad.exe"])
                print("Notepad opened successfully")
                speak("Notepad opened successfully")  # Assuming 'speak' function is defined elsewhere

            except Exception as e:
                print(f"An error occurred while opening Notepad: {e}")
                speak("An error occurred while opening Notepad")  # Assuming 'speak' function is defined elsewhere
                
                    
        # NPPR9-FWDCX-D2C8J-H872K-2YT43

        elif "weather" in query:
            
            # Google Open weather website
            # to get API of Open weather 
            api_key = keys.api4
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            speak(" City name ")
            print("City name : ")
            city_name = takeCommand()
            # complete_url variable to store
            # complete url address
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            
            # get method of requests module
            # return response object
            response = requests.get(complete_url)
            
            # json method of response object 
            # convert json format data into
            # python format data
            x = response.json()
            
            # Now x contains list of nested dictionaries
            # Check the value of "cod" key is equal to
            # "404", means city is found otherwise,
            # city is not found
            if x["cod"] != "404":
            
                # store the value of "main"
                # key in variable y
                y = x["main"]
            
                # store the value corresponding
                # to the "temp" key of y
                current_temperature = y["temp"]
            
                # store the value corresponding
                # to the "pressure" key of y
                current_pressure = y["pressure"]
            
                # store the value corresponding
                # to the "humidity" key of y
                current_humidity = y["humidity"]
            
                # store the value of "weather"
                # key in variable z
                z = x["weather"]
            
                # store the value corresponding 
                # to the "description" key at 
                # the 0th index of z
                weather_description = z[0]["description"]
            
                # print following values
                print(" Temperature (in kelvin unit) = " +
                                str(current_temperature) +
                    "\n atmospheric pressure (in hPa unit) = " +
                                str(current_pressure) +
                    "\n humidity (in percentage) = " +
                                str(current_humidity) +
                    "\n description = " +
                                str(weather_description))
                
                speak(" Temperature (in kelvin unit) = " +
                                str(current_temperature) +
                    "\n atmospheric pressure (in hPa unit) = " +
                                str(current_pressure) +
                    "\n humidity (in percentage) = " +
                                str(current_humidity) +
                    "\n description = " +
                                str(weather_description))

            else: 
                speak(" City Not Found ")
            
        elif "send message " in query:
                # You need to create an account on Twilio to use this service
                account_sid = 'Account Sid key'
                auth_token = 'Auth token'
                client = Client(account_sid, auth_token)

                message = client.messages \
                                .create(
                                    body = takeCommand(),
                                    from_='Sender No',
                                    to ='Receiver No'
                                )

                print(message.sid)

        elif "open wikipedia" in query:
            webbrowser.open("wikipedia.com")

        elif "Good Morning" in query:
            speak("A warm" +query)
            speak("How are you Mister")
            speak(assname)

        # most asked question from google Assistant
        elif "will you be my gf" in query or "will you be my bf" in query: 
            speak("I'm not sure about, may be you should give me some time")

        elif "how are you" in query:
            speak("I'm fine, glad you me that")

        elif "i love you" in query:
            speak("It's hard to understand")


        else :
            genai.configure(api_key=keys.api6)

            def get_gemini_response(prompt, image=None):
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                response = model.generate_content(contents=[prompt])
                
                # Extract the text content from the response
                text_response = response.candidates[0].content.parts[0].text
                return text_response
                # Extract and join the text parts from the response
                text_response = "".join([part.text for part in response.candidates[0].parts])
                return text_response

            response = get_gemini_response(query)
            print(response)
            speak(response)



                # You can choose to ask the user to select an option here'''

        
        # elif "" in query:
            # Command go here
            # For adding more commands++++
#return 'Python code for voice assistant is running'

if __name__ == '__main__':
    app.run(debug=True)
