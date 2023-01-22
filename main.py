import bs4
import os
import playsound
import re
import requests
import urllib.request
import webbrowser
import platform
import speech_recognition as sr
from gtts import gTTS


class CustomError(Exception):
    pass


class Exit(Exception):
    pass


def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)



r = sr.Recognizer()
operatingSys = platform.system()
if operatingSys == "Darwin":
    mode = 'macosx'
elif operatingSys == "Windows":
    mode = "windows-default"


with sr.Microphone() as source:
    print('Hello, welcome to Adibot!')


    def wholecode():
        global CustomError
        inputsuccess = False
        while not inputsuccess:
            print(
                'What would you like to search?:\n\n\tGoogle (end sentence with "direct" to open the first link)\n\tYoutube\n\tWeather(city)\n\nsearch as "(platform) search or say "exit"')
            try:
                x = False
                while not x:
                    try:
                        tsearch = r.recognize_google(r.listen(source, timeout=10))
                        x = True
                    except:
                        print('Didnt get that, speak again.')
                        speak('Didnt get that, try again.')

                tsearch = tsearch.split()
                site = tsearch.pop(0)

                if site.lower() == 'google':
                    inputsuccess = True

                    if tsearch[-1].lower() == 'direct':
                        direct = True
                        tsearch.pop(-1)
                        gsearch = ' '.join(tsearch)
                    else:
                        direct = False
                        gsearch = ' '.join(tsearch)

                    print(f"searching '{gsearch}'...")

                    if direct:
                        speak('launching google in direct mode.')
                        webbrowser.get(mode).open(
                            f"https://www.google.com/search?q={'+'.join(gsearch.split())}&btnI")
                    else:
                        speak('launching google.')
                        webbrowser.get(mode).open(f"https://www.google.com/search?q={'+'.join(gsearch.split())}")

                elif site.lower() == 'youtube':
                    inputsuccess = True

                    ytsearch = '+'.join(tsearch)
                    print(f'searching {" ".join(tsearch)}')
                    print('launching youtube')
                    speak('launching youtube')
                    webbrowser.get(mode).open(f"https://youtube.com/results?search_query={ytsearch}")

                elif site.lower() == 'weather':
                    inputsuccess = True
                    wsearch = ''.join(tsearch)
                    try:
                        req = requests.get(
                            f'https://www.weather-forecast.com/locations/{wsearch.lower()}/forecasts/latest')
                        soup = bs4.BeautifulSoup(req.text, 'lxml')
                        wforc = soup.select('.b-forecast__table-description-content')[0].text.split()

                    except:
                        raise CustomError

                    print(f'searching {wsearch}...')
                    speak(f"finding weather for {wsearch}")

                    words = {'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday', 'Mon': 'Monday', 'Tue': 'Tuesday',
                             'Wed': 'Wednesday', 'Thu': 'Thursday', 'W': 'west', 'N': 'north', 'S': 'south', 'E': 'East'}
                    for word in range(len(wforc)):
                        if wforc[word] in words:
                            wforc[word] = words[wforc[word]]

                    print(' '.join(wforc))
                    speak(' '.join(wforc))

                elif site.lower() == 'exit':
                    inputsuccess = True
                    raise Exit

            except CustomError:
                print('Not a city. Try again')
                speak('Not a city. Try again')
                wholecode()

            except Exit:
                pass

            except:
                print('\nDidnt quite get that :/\nTry again')
                speak('Didnt quite get that, Try again')
                wholecode()


    wholecode()
