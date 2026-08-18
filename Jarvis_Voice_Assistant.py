import datetime
import asyncio
import tempfile
import os
import requests
import webbrowser
import speech_recognition as sr
import edge_tts
from pygame import mixer
 
mixer.init()

VOICE = "en-IN-PrabhatNeural"  # Change to en-IN-NeerjaNeural for female voice


def speak(text):
    async def _speak():
        communicate = edge_tts.Communicate(text, VOICE)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            filename = f.name
        await communicate.save(filename)
        mixer.music.load(filename)
        mixer.music.play()
        while mixer.music.get_busy():
            await asyncio.sleep(0.1)
        mixer.music.unload()
        os.remove(filename)
    asyncio.run(_speak())


def wishMe():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning bro")
    elif hour < 17:
        speak("Good afternoon")
    elif hour < 19:
        speak("Good evening")
    else:
        speak("Good night")
    speak("I am your assistant. Please tell me how may I help you.")


def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1) as source:
        print("Listening...")
        r.dynamic_energy_threshold = True
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source, timeout=5, phrase_time_limit=6)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print("User said:", query)
        return query.lower()
    except Exception as e:
        print(e)
        return "none"


def search_wikipedia(query):
    search = query
    for w in ["wikipedia", "who is", "what is", "tell me about", "search"]:
        search = search.replace(w, "")
    search = search.strip().title()
    if not search:
        speak("Please tell me what to search.")
        return
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{search.replace(' ', '_')}"
    try:
        r = requests.get(url, headers={"User-Agent": "JarvisVoiceAssistant/1.0"}, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if "extract" in data:
                print(data["extract"])
                speak("According to Wikipedia")
                speak(data["extract"])
            else:
                speak("No summary found.")
        else:
            speak("Sorry, I could not find that page on Wikipedia.")
    except Exception as e:
        print(e)
        speak("Something went wrong while searching Wikipedia.")


if __name__ == "__main__":
    wishMe()
    while True:
        query = TakeCommand()
        if query == "none":
            continue
        if any(x in query for x in ["wikipedia", "who is", "what is", "tell me about"]):
            search_wikipedia(query)
        elif any(x in query for x in ["youtube", "open youtube"]):
            webbrowser.open("youtube.com")  
        elif any(x in query for x in ["google", "open google", "give ans"]):
            webbrowser.open("google.com")  
        elif any(x in query for x in ["song","play song"]):
            music_dir = 'E:\music'
            songs = os.listdir(music_dir) 
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        elif any(x in query for x in ["date", "time", "current time", "what is the time"]):
            current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
            print(f"Current Time: {current_time}")
            speak(f"The current time is {current_time}")
        elif query in ("exit", "quit", "stop"):
            speak("Goodbye.")
            break