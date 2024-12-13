from kivy.graphics import Rectangle
from kivy.uix.floatlayout import FloatLayout


class BackgroundFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_image = 'background.png'  # Chemin de l'image de fond

        with self.canvas.before:  # Dessiner avant les widgets
            if self.background_image:
                self.rect = Rectangle(source=self.background_image, size=self.size, pos=self.pos)
            else:
                self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        """Met à jour la taille et la position du fond."""
        self.rect.size = self.size
        self.rect.pos = self.pos