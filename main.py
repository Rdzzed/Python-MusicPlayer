import pygame
from kivy import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from home import HomeScreen
from music import MusicScreen

Config.set('graphics', 'width', '350')
Config.set('graphics', 'height', '600')

pygame.mixer.init()



# Gestionnaire d'écran
class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_song_index = 0
        self.add_widget(HomeScreen(name='home'))
        self.add_widget(MusicScreen(name='music'))


# Application principale
class MyApp(App):
    title = 'Music Player IOS'
    icon = 'icone.png'

    def build(self):
        return MyScreenManager()


if __name__ == '__main__':
    MyApp().run()
