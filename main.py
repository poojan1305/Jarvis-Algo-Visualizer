import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pywhatkit as kit
import webbrowser
import os
import smtplib  
import pygame
import sys
import re
from tkinter import *
from tkinter import messagebox
from threading import * 


WIDTH = 500

root=Tk()
root.title('Jarvis')
root.geometry("1020x507")

def printgui(string) :
    lab = Label(root , text ="" , width = 30)
    lab.place(x = 10 , y = 20)
    lab = Label(root , text = string , width = 30)
    lab.place(x = 10 , y = 20)

def user_said(string) : 
    lab = Label(root , text = "" , width = 50)
    lab.place(x = 10 , y = 45)
    lab = Label(root , text = string, width = 50)
    lab.place(x = 10 , y = 45)   

def deb(string) : 
    lab = Label(root , text = "" , width = 30)
    lab.place(x = 10 , y = 100)
    lab = Label(root , text = string , width = 30)
    lab.place(x = 10 , y = 100)

txt = Text(root , height = 4 , width = 20)
txt.pack()


''' sapi5 is an inbuilt voice provided for windows users '''

engine = pyttsx3.init('sapi5')                   #initializing text to speech engine
voices = engine.getProperty('voices')            #for getting details of current voice
engine.setProperty('voice', voices[0].id)         # 2 voices available 0 - male ; 1 - female


def speak(audio):
    ''' This function speaks out the text 
    passed as a parameter to the function'''
    engine.say(audio)        #pywhatkit
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour > 0 and hour < 12:
        speak("Good Morning ")

    elif hour > 12 and hour < 18:
        speak("Good afternoon")

    else:
        speak("Good Evening")

    speak("I am Jarvis. How may I help you")            

def takeCommand():
    ''' This command uses Speech recognition module to understand
        our command and print a string to the output
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        printgui("Listening ...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        printgui("Recognizing...")
        query = r.recognize_google(audio, language="en-in")    #google is used for voice recognition
        user_said(f"User said : {query}\n")

    except Exception as e:
        #print(e)

        printgui("Say that again Please")
        return "None"

    return query            




class bool : 
    def __init__(self) : 
        self.val = False

def start(b):

    ''' This is used so that when we create a different
        module and import this module then we can
        access only the functions of it not the other code'''

    wishMe()
    while 1:
        if b.val == True : 
            break 
        query = takeCommand().lower()

        if 'wikipedia' in query:
            query = query.replace('wikipedia','')
            speak("Searching Wikipedia..")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia ")
            deb(results)
            speak(results)

        if 'google' in query : 
            query = query.replace('google' ,'')
            speak("searching Google...")
            result = kit.search(query)

        if 'a star' in query:
            speak("Ok Implementing Astar Now")
            import Astar as a
            a.astar_main(a.WIN, WIDTH)

            speak("What do you want to do next?")

            query = takeCommand().lower()    

            if 'close' in query:
                pygame.quit()

        if 'dj' in query:
            speak("Ok Implementing Dijkstra Now")
            import Dijkstra as d
            d.dijkstra_main(d.WIN, WIDTH)

            speak("What do you want to do next?")

            query = takeCommand().lower()    

            if 'close' in query:
                pygame.quit()        

        if 'whatsapp' in query:
            speak("Whom do you want to send message ? ")
            r = takeCommand().lower()
            print("Here is " , r)
            while r == "none" : 
                speak("Please say that again..")
                r = takeCommand().lower()
            speak("What message do you want to send ? ")
            msg = takeCommand().lower()
            reciever = r.split()

            hr = int(datetime.datetime.now().hour)   

            file = open("contacts.txt" , 'r')
            data = file.read() 
            file.close()
            add = 2 
            for name in reciever :
                srch = re.search(rf'\b{name}' ,data) 
                if srch == None  : 
                    speak(f"Do you want to save {name} as contact")
                    yn = takeCommand().lower()
                    if yn == 'no' :
                        continue 
                    else : 
                        speak(f"Enter the {name}'s number with country code :")
                        save = input()
                        file = open('contacts.txt' , 'a+')
                        file.write(f"\n{name} : {save}")
                        file.seek(0) 
                        data = file.read() 
                        file.close()
                    
                        speak("Contact saved.")

                pattern = re.findall(rf'\b{name}\s:\s\d+\b',data)
                
                
                
                num = re.findall(rf'\b\d+\b',pattern[0])
                number = '+' + num[0]
                minute = ( int(datetime.datetime.now().minute) + add)%60
                add += 2
                print(number, msg, hr , minute )
                t = Thread(target = kit.sendwhatmsg , args = (number , msg , hr , minute , 30))
                t.start()
                speak("Your Message will be sent within 5 minutes")

            print("Message sent !!!!!")  
        
        if 'mail' in query : 
            file = open("mail.txt" , 'r')
            data = file.read()
            file.close() 
            if data == "" : 
                speak("Please register yourself first")
                mail = input("Enter your mail : ")
                password = input("Enter your password")
                file = open("mail.txt" , 'w')
                string = f"{mail}\n{password}"
                file.write(string)
                file.close()
            
            speak("Whom do you want to send the mail")
            r = takeCommand().lower()
            while r == "none" : 
                speak("Please repeat")
                r = takeCommand().lower()

            file = open("mail.txt" , 'r')
            data = file.read() 
            file.seek(0) 
            mail = file.readline() 
            password = file.readline()
            print("Mail" , mail)
            print("password" , password)
            file.close()
            receiver = r.split()
            
            for name in receiver : 
                if re.search(rf"\b{name}\b",data) == None :
                    speak(f"{name} is not present in the mail list")
                    speak("Enter his mail-id : ")
                    em = input("Enter mail : ")
                    file = open("mail.txt" , 'a')
                    file.write(f"\n{name} : {em}")
                file = open("mail.txt" , 'r')
                data = file.read() 
                file.close()
                pattern = re.findall(rf'\b{name}\s:\s\w.+\b',data)
                print("Pattern : " , pattern)
                mail_id = re.findall(r'\s\b\w.+\b' ,pattern[0])
                actual = mail_id[0]
                actual = actual[1:]
                print(actual , "mail")
                speak("What should be the subject of Mail")
                subject = takeCommand()
                speak("Write your message : ")
                msg = input("Message : ")
                try : 
                    kit.send_mail(mail , password , subject , msg , actual)
                except Exception as e : 
                    print("Something went wrong")
                    print(e)


        if 'close' in query or b.val == True:
            deb("Thread Killed")
            break        

class count : 
    def __init__(self) : 
        self.cnt = 0 

def clicked(c , b) :  
    
    if c.cnt % 2 != 0 : 
        t = Thread(target = start , args = (b ,))
        t.start()
        b.val = False
        print("started")
    else : 
        b.val = True 
      

def counter(c , b) : 
    c.cnt += 1 
    print("Print cnt variable" , c.cnt)
    clicked(c , b)

bg = PhotoImage(file = "vc.png")
label1 = Label( root, image = bg,bg='coral')
label1.place(x = 0, y =0 )
c = count()

b = bool()

mybutton=Button(root,text="ACTIVATE JARVIS" , borderwidth = 0,bg='yellow',bd=6, width=14,height=2,command=lambda : counter(c , b))

mybutton.place(x=449,y=377)

mainloop()




        


