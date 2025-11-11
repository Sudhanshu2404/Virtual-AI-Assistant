import speech_recognition as sr
import google.generativeai as genai
import API_KEY as api
import pyttsx3
import webbrowser
import time
import env as ev
import os
from rich import print
from rich.panel import Panel


class PersonalAssistance:
    #Google gemine AI method

    #write function
    def read_file(self):
        self.say('Please provide the path of the file:')
        path= input(str('Please provide the path of the file:').strip())
        if os.path.exists(path):
            file= open(path,'r')
            content= file.read()
            return content
        else:
            print('Unable to find. Please check.')
            self.say('Unable to find. Please check.')
            return False

    def create_log(self,name):
        self.path=f'logfile_{name}.txt'
        try:
            if not os.path.exists(self.path):  
                with open(self.path, 'w') as file:
                    file.write('This is log file')
            else:
                with open(self.path, 'a') as file:
                    file.write(f" \n\n\t {time.strftime(time.strftime('%D %T'))} \n")
        except Exception as e:
            print("[bold yellow]Exception in creating_log:[/bold yellow]", e)

    def write_log(self,text):
        path=self.path
        try:
            with open(path, 'a') as file:
                    file.write(text)
        except Exception as e:
            print("[bold yellow]Exception in writing_log:[/bold yellow]", e)


    def chat_with_AI(self,command):
        try:
            client = genai.configure(api_key=api.API_KEY)
            model= genai.GenerativeModel('gemini-2.5-flash')
            chat=model.start_chat()
            while True:
                user_input= command
                if user_input:
                    self.response=chat.send_message(user_input)
                    print(Panel(f"[green]{self.response.text}[/green]"))
                    self.write_log(f'\n{ev.SpeakerName['AI']}: {self.response.text}\n')
                    print(f'[bold blue]{ev.SpeakerName['AI']}[/bold blue]: Do you want me to read it out. So, please say "read"')
                    self.say('if you want me to read out please say read')
                    readit=self.taking_command(5,3)
                    print(f'[bold blue]{ev.SpeakerName['AI']}[/bold blue]:Listening...')
                    if 'read'.lower() in readit:
                        print(f'[bold blue]{ev.SpeakerName['AI']}[/bold blue]: Reading...')
                        self.say(self.response.text)
                        break
                    else:
                        break
                else:
                    self.say("I didn't hear anything. Please try again.")
                    break
        except KeyboardInterrupt:
                    print("\n[bold red]Jarvis is Shutting down...[/bold red]")
                    self.say(f"Goodbye!")
                    exit()
        except Exception as e:
            print('[bold red]Error in AI[/bold red]', e)
            return None

    #Taking Command
    def say(self,command):
        try:
            engine= pyttsx3.init()
            engine.say(command)
            engine.runAndWait()

        except KeyboardInterrupt:
                    print("\n[bold red]Jarvis is Shutting down...[/bold red]")
                    self.say(f"Goodbye!")
                    exit()
        except Exception as e:
            print('[bold red]Error in say method:[/bold red] ',e)

    #Command Processing
    def command_process(self, command):
        try:

            if 'search' in command.lower() and 'google' in command.lower():
                print(f'[bold blue]{ev.SpeakerName['Agent']}[/bold blue]:Searching...')
                self.write_log(f'\n{ev.SpeakerName['Agent']}:Searching...')
                self.say('Searching...')
                new_str=command.split(' ')
                search=''
                for i, v in enumerate(new_str):
                    if v.lower()=='search':
                        search+=" ".join(new_str[i+1:])
                self.write_log(f'\n{ev.SpeakerName['Agent']}: https://www.google.com/search?q={search}')
                webbrowser.open(f'https://www.google.com/search?q={search}')

            elif 'youtube' in command:
                self.say('Opening Youtube')
                self.write_log(f'\n{ev.SpeakerName['Agent']}: https://youtube.com')
                webbrowser.open('https://youtube.com')

            elif 'linkedin' in command:
                self.say('Opening Linkedin')
                self.write_log(f'\n{ev.SpeakerName['Agent']}: https://linkedin.com')
                webbrowser.open('https://linkedin.com')

            elif "hello" in command:
                print(f"[bold blue]{ev.SpeakerName['Agent']}[/bold blue]: Hello! How can I help you?")
                self.write_log(f"\n{ev.SpeakerName['Agent']}: Hello! How can I help you?")
                self.say("Hello! How can I help you?")

            elif "how are you" in command:
                print(f"[bold blue]{ev.SpeakerName['Agent']}[/bold blue]: I am doing good. How can I assist you?")
                self.write_log(f"\n{ev.SpeakerName['Agent']}: I am doing good. How can I assist you?")
                self.say("I am doing good. How can I assist you?")

            elif "time" in command:
                current_time = time.strftime("%I:%M %p")
                print(f"[bold blue]{ev.SpeakerName['Agent']}[/bold blue]: The current time is {current_time}")
                self.write_log(f"\n{ev.SpeakerName['Agent']}: The current time is {current_time}")
                self.say(f"The current time is {current_time}")

            elif "weather" in command:
               self.write_log(f"\n{ev.SpeakerName['Agent']}: I don't have weather information yet, but I'm working on it!")
               self.say(" I don't have weather information yet, but I'm working on it!")

            elif "stop" in command or "exit" in command or "quit" in command:
                print(f"[bold blue]{ev.SpeakerName['Agent']}:[/bold blue] Goodbye! See you later!")
                self.write_log(f"\n{ev.SpeakerName['Agent']}: Goodbye! See you later!")
                self.say("Goodbye! See you later!")
                exit()
            
            elif "document" in command or "file" in command:
                prompt=self.read_file()
                if prompt:
                    print('Founded. What you want to do with it')
                    self.say('Founded. What you want to do with it')
                while prompt:
                    task=self.taking_command()
                    if 'read' in task:
                        self.say(prompt)
                        print('Listening...')
                    elif f'{ev.SpeakerName['Agent']}'.lower() in task:
                        print(f'[bold blue]{ev.SpeakerName['Agent']}[/bold blue]: Yes, How can I assist you')
                        self.say('Yes, How can I assist you')
                        print(f'[bold yellow]{ev.SpeakerName['Agent']}: Waiting...[bold yellow]')
                        new_command=self.taking_command(10,10)
                        self.command_process(new_command)
                    else:
                        self.chat_with_AI(f'{prompt}. {task}')



            else:
                print(f"[bold blue]{ev.SpeakerName['Agent']}[/bold blue]: Searching...")
                self.write_log(f"\n{ev.SpeakerName['Agent']}: Searching...")
                self.say(f"Searching...")
                self.chat_with_AI(command)

        except Exception as e:
            self.write_log('\nError in Command Processing Method:', e)
            print('Error in Command Processing Method:', e)
            return False
        return True
    

    #Listener Method
    def taking_command(self,timeout=5,phrase_time_limit=10):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("[bold yellow]Listening...[/bold yellow]")
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print('[bold yellow]Rcoginizing...[/bold yellow]')
            output=recognizer.recognize_google(audio)
            print(f"[bold green]{ev.SpeakerName['User']}[/bold green]: {output}")
            self.write_log(f'\n{ev.SpeakerName['User']}: {output}')
            return output.lower()
        except sr.WaitTimeoutError:
            print("[bold red]Listening timeout[/bold red]")
            return None
        except sr.UnknownValueError:
            print("[bold red]Could not understand audio[/bold red]")
            return None
        except sr.RequestError as e:
            print(f"[bold red]Google Speech Recognition error[/bold red]: {e}")
            return None
        except Exception as e:
            print('[bold red]Error in Taking_command:[/bold red]', e)
            exit()

    #Main methond
    def main(self):
            print('='*80)
            print('\t\t\t\t[bold underline red]VIRTUAL ASSISTANT[/bold underline red]\t\t\t\t')
            print('='*80)
            # print('Intializing your Assistant')
            self.say('Initializing')
            # print('Initialized')
            self.say('Initialized')
            print(f'[bold underline yellow]Say {ev.SpeakerName['Agent']} for activating me[/bold underline yellow]')
            self.say(f'Say {ev.SpeakerName['Agent']} for activating me')
            while True:
                try:
                    activate=self.taking_command(10,10)

                    if activate is None:
                        continue

                    if f'{ev.SpeakerName['Agent']}'.lower() in activate:
                        print(f'[bold blue]{ev.SpeakerName['Agent']}[/bold blue]: Yes, How can I assist you')
                        self.say('Yes, How can I assist you')
                        print(f'[bold yellow]{ev.SpeakerName['Agent']}: Waiting...[bold yellow]')
                        command=self.taking_command(10,10)
                        if command:
                            should_continue=self.command_process(command)
                            if not should_continue:
                                break
                        else:
                            self.say("I didn't hear anything. Please try again.")
                    elif "stop" in activate or "exit" in activate:
                        self.say("Shutting down. Goodbye!")
                        break
                except KeyboardInterrupt:
                    print("\n[bold red]Jarvis is Shutting down...[bold red]")
                    self.say(f"Goodbye!")
                    break
                except Exception as e:
                    print("[bold red]Error in Main method: [bold red]", e)


if __name__=='__main__':
    obj=PersonalAssistance()
    obj.create_log(f'{time.strftime(time.strftime('%d%m%y%I%M%S'))}')
    obj.main()

