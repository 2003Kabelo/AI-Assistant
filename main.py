from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha

#Speech Initialisation
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
activationWord = 'computer'

def speak(text,rate=120):
    engine.setProperty('rate',rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    listener = sr.Recognizer()
    print("Listening for a command")

    with sr.Microphone() as source:
        listener.pause_threshold = 2
        input_speech = listener.listen(source)
    try:
        print('Recognizing speech.....')
        query = listener.recognize_google(input_speech,language='en_gb')
        print(f'The input speech was :{query}')
    except Exception as exc:
        print("I did not hear that ")
        speak('I did not hear that')
        print(exc)
        return 'None'
    return query
#Main loop

if __name__=='__main__':
    speak('Welcome to Kabelo Mashapa system , how can i help ? .')
    while True:

        #Parse as a list
        query = parseCommand().lower().split()
        if query[0] == activationWord:
            query.pop(0)
            #List commands
            if query[0] == 'say':
                speak('Greetings, South African people')
            else:
                query.pop(0) #Remove the Say
                speech = ''.join(query)
                speak(speech)




