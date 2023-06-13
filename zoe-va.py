import tkinter as tk
from PIL import ImageTk, Image
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pyjokes
import random

class Zoe:
    def __init__(self, widget):
        self.MASTER = "Arvind"
        self.widget = widget
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        self.r = sr.Recognizer()

    def speak(self, text):  # text to speech
        self.engine.say(text)
        self.engine.runAndWait()

    def wishMe(self):
        hour = datetime.datetime.now().hour

        if hour < 12:
            self.speak(f"Good morning {self.MASTER}")
        elif 12 <= hour < 18:
            self.speak(f"Good afternoon {self.MASTER}")
        else:
            self.speak(f"Good evening {self.MASTER}")

        self.speak("This is Zoe. How may I help you?")

    def takeCommand(self):   # voice to text
        with sr.Microphone() as source:
            self.widget.update_user_text("Listening...")
            self.widget.root.update()
            audio = self.r.listen(source)

        try:
            self.widget.update_user_text("Recognizing...")
            self.widget.root.update()
            query = self.r.recognize_google(audio, language='en-in')
            self.widget.update_user_text(f"You said: {query}")
            self.widget.root.update()
            return query.lower()
        except Exception as e:
            self.widget.update_user_text("Sorry, I didn't catch that.")
            self.widget.root.update()
            return None

    def search_wikipedia(self, query):
        self.speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            self.speak(results)
            print(results)

        except wikipedia.exceptions.DisambiguationError as e:
            self.speak("Multiple results found. Please specify your query.")

    def open_website(self, url):
        webbrowser.open(url)
    
    def get_jokes(self):
        joke = pyjokes.get_joke(language='en', category='neutral')
        self.speak(joke)

    def play_music(self):
        songs_dir = "C:\\Users\\91790\\Music"
        songs = os.listdir(songs_dir)
        rd = random.choice(songs)
        os.startfile(os.path.join(songs_dir, rd))

    def play_video(self):
        videos_dir = "C:\\Users\\91790\\Videos"
        videos = os.listdir(videos_dir)
        os.startfile(os.path.join(videos_dir, videos[0]))

    def get_current_time(self):
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        self.speak(f"{self.MASTER}, the time is {strTime}")

    def open_code_editor(self):
        codePath = "C:\\Users\\91790\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code\\Visual Studio Code.lnk"
        os.startfile(codePath)

    def send_email(self):
        try:
            self.speak("Whom should I send the email to?")
            self.widget.update_user_text("Whom should I send the email to?")
            to = self.widget.userText.get()  # Retrieve user input from the GUI
            self.speak("What should I send?")
            self.widget.update_user_text("What should I send?")
            content = self.widget.userText.get()  # Retrieve user input from the GUI

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login('ak041026@gmail.com', password='p@$$w0rd2o23')
            server.sendmail("rajkumarmahto450@gmail.com", to, content)
            server.close()

            self.speak("Email has been sent to the recipient.")
        except Exception as e:
            self.speak("Sorry, I couldn't send the email. Please try again later.")

    def process_query(self, query):
        if 'wikipedia' in query:
            self.search_wikipedia(query)
        elif 'your name' in query:
            self.speak("Hello Sir, my name is Zoe")
        elif 'open youtube' in query:
            self.open_website("https://www.youtube.com")
        elif 'open google' in query:
            self.open_website("https://www.google.com")
        elif 'open stackoverflow' in query:
            self.open_website("https://stackoverflow.com")
        elif 'open whatsapp web' in query:
            self.open_website("https://web.whatsapp.com")
        elif 'read joke' in query:
            self.get_jokes()
        elif 'play music' in query:
            self.play_music()
        elif 'play video' in query:
            self.play_video()
        elif 'the time' in query:
            self.get_current_time()
        elif 'open code' in query:
            self.open_code_editor()
        elif 'send email to' in query:
            self.send_email()
        elif 'search location' in query:
            location = self.speak("what is your location?")
            url = 'https://www.google.com/maps/search/?api=1&parameter'
            self.open_website.get().open(url)
            self.speak('Here is location' + location)
        elif 'exit' in query:
            self.speak("Thank you,Have good day")
            self.widget.root.destroy()
        else:
            self.speak("Sorry, I didn't understand your command.")

    def run(self):
        self.speak("Initializing Zoe...")
        self.wishMe()
        while True:
            query = self.takeCommand()
            if query is not None:
                self.process_query(query)


class Widget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("520x320")
        img = ImageTk.PhotoImage(Image.open("C:\\Users\\91790\\Downloads\\Zoe-assistants-img.png"))
        panel = tk.Label(self.root,image=img)
        panel.pack(side='right',fill='both',expand='no')
        self.root.title("Zoe - Virtual Assistant")

        self.userText = tk.StringVar()
        self.userText.set("Zoe Virtual Assistant")
        userFrame = tk.LabelFrame(self.root, text='Zoe',font=('Helvetica',20,'bold'))
        userFrame.pack(fill='both',expand='yes')

        top = tk.Message(userFrame, textvariable=self.userText,bg='Sky Blue',fg='white')
        top.config(font=("Arial",25,'bold'))
        top.pack(side='left',fill='both',expand='yes')

        self.label = tk.Label(self.root, text='Tell me what you want to search!...', font=("Helvetica", 14), wraplength=580)
        self.label.pack(side='top', fill='both', expand='yes')

        self.btn = tk.Button(self.root, text='Speak', font=('Helvetica', 12, 'bold'), bg='red', fg='white',
                             command=self.clicked)
        self.btn.pack(fill='x', expand='no')

        self.btn2 = tk.Button(self.root, text='Close', font=('Helvetica', 12, 'bold'), bg='yellow', fg='black',
                              command=self.root.destroy)
        self.btn2.pack(fill='x', expand='no')

        self.root.mainloop()

    def update_user_text(self, text):
        self.userText.set(text)

    def clicked(self):
        self.update_user_text("Listening...")
        self.root.update()
        zoe = Zoe(self)
        zoe.wishMe()
        while True:
            query = zoe.takeCommand()
            if query is not None:
                self.update_user_text(f"You said: {query}")
                self.root.update()
                zoe.process_query(query)
            else:
                self.update_user_text("Sorry, I didn't catch that.")
                self.speak(self.update_user_tex)
                self.root.update()


if __name__ == "__main__":
    widget = Widget()

