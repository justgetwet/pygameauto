import pygame
import os
from mutagen.mp3 import MP3
from gtts import gTTS
import uuid
from time import sleep

class Tts:

    def tts_save(self, txt, mp3_filepath):
        tts = gTTS(txt, lang='en')
        tts.save(mp3_filepath)
        while not os.path.isfile(mp3_filepath):
            sleep(1)
    
    def sound_play(self, mp3_filepath):
        pygame.mixer.init(frequency = 44100)
        pygame.mixer.music.load(mp3_filepath)
        pygame.mixer.music.play()
        mp3_length = MP3(mp3_filepath).info.length
        sleep(mp3_length + 0.25)
        pygame.mixer.music.stop()

    def talk(self, txt):
        filename = str(uuid.uuid4())
        p = f"./sounds/{filename}.mp3"
        self.tts_save(txt, p)
        self.sound_play(p)

if __name__=='__main__':

    tts = Tts()
    tts.talk("hello python")