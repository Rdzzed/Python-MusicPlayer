from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from music import *
from list import list_of_title, list_of_songs, list_of_cover




class ColoredFloatLayout(FloatLayout):

    def __init__(self, color=(0.48, 0.48, 0.48, 1), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:  # Dessin avant les widgets
            Color(*color)  # Définir la couleur
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos



# Écran d'accueil
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = ColoredFloatLayout(color=(0.26, 0.26, 0.26, 0.5))

        label = Label(text="Music Player", font_size=35, line_height=2, pos_hint={'center_x': 0.23, 'center_y': 0.965})
        layout.add_widget(label)

        scroll_view = ScrollView(size_hint=(1, 0.85), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        box_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        box_layout.bind(minimum_height=box_layout.setter('height'))

        for i, (titre, cover, song) in enumerate(zip(list_of_title, list_of_cover, list_of_songs)):
            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)
            image = Image(source=cover, size_hint=(None, 1), width=60, allow_stretch=True)
            button = Button(text=titre, font_size=18, color=(1, 1, 1, 1), background_color=(0.36, 0.36, 0.36, 1),height=60,size_hint_y=None)
            button.bind(on_press=lambda instance, song=song, cover=cover: self.go_to_music_screen(song, cover))

            item_layout.add_widget(image)
            item_layout.add_widget(button)
            box_layout.add_widget(item_layout)

        scroll_view.add_widget(box_layout)
        layout.add_widget(scroll_view)

        self.mini_bar_container = FloatLayout(size_hint=(1, None), height=60, pos_hint={'center_x': 0.5, 'y': 0})
        self.mini_bar_container.opacity = 0  # Initialement masquée

        # Ajouter l'image de fond
        self.mini_bar_background = Image(source='fond.png', size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.mini_bar_container.add_widget(self.mini_bar_background)

        # Ajouter la BoxLayout vide mais masquée pour l'instant
        self.mini_bar = BoxLayout(orientation='horizontal',size_hint=(1, None), height=60, pos_hint={'center_x': 0.5, 'y': 0},spacing=10)
        self.mini_bar_container.add_widget(self.mini_bar)

        self.mini_bar_cover = Image(size_hint=(None, 0.8), width=60, allow_stretch=False,pos_hint={'center_x': 0.5, 'y': 0.1})
        self.mini_bar.add_widget(self.mini_bar_cover)

        self.mini_bar_button = Button(text='',halign='left',valign='middle',size_hint=(1,1),background_normal='fond.png')
        self.mini_bar_button.text_size = (self.mini_bar_button.width, None)  # Largeur du bouton, hauteur automatique
        self.mini_bar_button.bind(size=self.update_text_size)
        self.mini_bar_button.bind(on_press=self.handle_mini_bar_press)
        self.mini_bar.add_widget(self.mini_bar_button)
        self.mini_bar_button.opacity = 0


        self.mini_bar_play_pause = Button(size_hint=(None, 0.7), width=40, background_normal='sign/play.png',background_color=(1,1,1,1),pos_hint={'center_x':0.8,'center_y':0.5},
                                          border=(0, 0, 0, 0))
        self.mini_bar_play_pause.bind(on_press=self.toggle_play_pause)
        self.mini_bar_container.add_widget(self.mini_bar_play_pause)

        self.mini_bar_next = Button(size_hint=(None,0.8),width=35,background_color=(1,1,1, 1),background_normal='sign/next.png',border=(0,0,0,0),pos_hint={'center_x':0.925,'center_y':0.5})
        self.mini_bar_next.bind(on_press=self.mini_next)
        self.mini_bar_container.add_widget(self.mini_bar_next)

        layout.add_widget(self.mini_bar_container)

        self.add_widget(layout)
        self.current_song = None
        self.current_cover = None


    def update_text_size(self, instance, value):
        instance.text_size = (instance.width, None)  # Largeur actuelle du bouton, hauteur automatique

    def go_to_music_screen(self, song, cover):
        self.manager.current_song_index = list_of_songs.index(song)

        music_screen = self.manager.get_screen('music')
        self.manager.transition = SlideTransition(direction='up')

        # Vérifier si la chanson est déjà en cours de lecture ou en pause
        if music_screen.current_song_path == song:
            if music_screen.is_playing:
                # Si la musique est déjà en cours, juste afficher l'écran de musique
                music_screen.show_music_screen(cover)
                music_screen.resume_music()
            else:
                # Si la musique est en pause, reprendre la lecture
                music_screen.pause_music()
            self.manager.current = 'music'
        else:
            # Sinon, démarrer la nouvelle musique
            music_screen.play_music(song, cover)
            self.manager.current = 'music'

    def handle_mini_bar_press(self, instance):
        """Gérer le clic sur le bouton de la mini-bar."""
        if self.current_song and self.current_cover and not self.is_playing:
            music_screen = self.manager.get_screen('music')

            # Basculer sur l'écran de musique
        self.manager.transition = SlideTransition(direction='up')
        self.manager.current = 'music'

            # Synchroniser les boutons Play/Pause avec l'état actuel
        self.update_play_pause_buttons()

    def update_play_pause_buttons(self):
        """Mettre à jour les icônes Play/Pause des boutons en fonction de l'état de lecture."""
        music_screen = self.manager.get_screen('music')

        # Mettre à jour l'icône sur la mini-bar
        self.mini_bar_play_pause.background_normal = 'sign/pause.png' if music_screen.is_playing else 'sign/play.png'

        # Mettre à jour l'icône sur l'écran de musique
        music_screen.play_pause_button.background_normal = 'sign/pause.png' if music_screen.is_playing else 'sign/play.png'

    def show_mini_bar(self,cover,song_title):
        self.mini_bar_container.opacity = 1
        self.mini_bar_button.opacity = 1
        self.mini_bar_cover.source = cover
        self.mini_bar_button.text = song_title # Affiche le titre de la chanson
        self.mini_bar_button.color = (1,1,1,1)  # Affiche la couverture

        self.current_song = list_of_songs[list_of_cover.index(cover)]
        self.current_cover = cover

        self.is_playing = self.manager.get_screen('music').is_playing
        self.mini_bar_play_pause.background_normal = 'sign/pause.png' if self.is_playing else 'sign/play.png'

    def hide_mini_bar(self):
        self.mini_bar_container.opacity = 0
        self.mini_bar_button.opacity = 0
        self.current_song = None
        self.current_cover = None

    def toggle_play_pause(self, instance):
        """Gérer le bouton Play/Pause depuis la mini-bar."""
        music_screen = self.manager.get_screen('music')

        if music_screen.is_playing:
            # Mettre la musique en pause
            music_screen.pause_music()
        else:
            # Reprendre la musique
            music_screen.resume_music()

        # Synchroniser les icônes
        self.update_play_pause_buttons()

    def mini_next(self, instance):
        self.manager.current_song_index = (self.manager.current_song_index + 1) % len(list_of_songs)

        # Accède à l'écran 'music' et appelle la méthode play_music
        music_screen = self.manager.get_screen('music')
        music_screen.play_music(list_of_songs[self.manager.current_song_index], list_of_cover[self.manager.current_song_index])

        # Optionnel: Mets à jour la mini bar avec la nouvelle chanson
        self.show_mini_bar(list_of_cover[self.manager.current_song_index], list_of_title[self.manager.current_song_index])