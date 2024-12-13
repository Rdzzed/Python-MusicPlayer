import pygame
from mutagen.mp3 import MP3
from pygame import mixer
pygame.mixer.init()

class AudioPlayer:
    def __init__(self, song_path):
        self.song_path = song_path
        # Si vous utilisez pygame, par exemple, initialisez-le
        pygame.mixer.music.load(song_path)

    def play(self):
        pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()

    def get_position(self):
        try:
            position = pygame.mixer.music.get_pos() / 1000.0  # Retour en secondes
            if position < 0:  # Cas où pygame retourne -1 quand rien n'est joué
                position = 0
            return position
        except Exception as e:
            print(f"[ERREUR] Impossible d'obtenir la position : {e}")
            return 0

    def set_position(self,new_time):
        return pygame.mixer.music.set_pos(new_time)  # Position en secondes

    def get_audio_length(self):
        """Récupère la durée du fichier MP3"""
        try:
            audio = MP3(self.song_path)
            return audio.info.length  # Retourne la durée du fichier en secondes
        except Exception as e:
            print(f"[ERREUR] Impossible d'obtenir la durée du fichier : {e}")
            return 0


