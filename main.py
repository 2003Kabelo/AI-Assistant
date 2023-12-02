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

#Configure browser
#Set the path
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chrome_path))

#Wolfram alpha client
appId = '5R57JY-7TYLVYREU4'
wolframClient = wolframalpha.Client(appId)
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

#Search Method
def search_wikipedia(query=''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print("No wikipedia results")
        return 'No result received'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error :
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def listOrDict(var):
    if isinstance(var,list):
        return var[0]['plaintext']
    else:
        return var['plaintext']
def search_wolframAlpha(query=''):
    response = wolframClient.query(query)
    if response['@success'] == 'false':
        return 'Could not compute'
    # Query resolved
    else:
        result = ''
        # Question
        pod0 = response['pod'][0]
        pod1 = response['pod'][1]
        # May contain the answer , has the highest confidence level
        if (('result') in pod1['@title'].lower() or (pod1.get('@primary','false')=='true') or ('definition' in pod1['@title'].lower())):
            result = listOrDict(pod1['subpod'])
            return result.split('(')[0]
        else:
            question = listOrDict(pod0['subpod'])
            return question.split('(')[0]
            speak('Computation Failed , Querying universal databank')
            return search_wikipedia(question)


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
        #Navigation
        if query[0] == 'go' and query[1] == 'to':
            speak("Opening....")
            query = ''.join(query)
            webbrowser.get('chrome').open_new(query)
        #Wikipedia
        if query[0] == 'wikipedia':
            query = ''.join(query[1:])
            speak('Quering the Universal databank.')
            result = search_wikipedia(query)
            speak(result)
        #Wolfram alpha
        if query[0] == 'compute' or query[0] == 'computer':
            query = ''.join(query[1:])
            speak('Computing')
            try:
                result = search_wolframAlpha(query)
                speak(result)
            except:
                speak("Unable to compute.")

        #Note Taking
        if query[0] == 'log':
            speak('Ready to record your note')
            newNote = parseCommand().lower()
            now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            with open('note_%s.txt'%now,w) as newFile :
                newFile.write(newNote)
            speak('Note Written')
        if query[0] == 'exit':
            speak('Good bye Fellas , Danko ')
            break





