from kivy.clock import Clock
from kivy.config import Config
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button

DEFAULT_SCREEN_WIDTH: int = 1280
DEFAULT_SCREEN_HEIGHT: int = 720

Config.set('graphics', 'width', str(DEFAULT_SCREEN_WIDTH))
Config.set('graphics', 'height', str(DEFAULT_SCREEN_HEIGHT))

from kivy.app import App
from kivy.graphics import Rectangle, Line, Color
from kivy.uix.boxlayout import BoxLayout


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)


class NavigationMenu(BoxLayout):

    def __init__(self, **kwargs):
        super(NavigationMenu, self).__init__(**kwargs)
        self.dimensions = 0, 0
        with self.canvas:
            self.spirit = Rectangle(pos=(0, 0), size=self.dimensions)

    minimum_width = 120

    def on_size(self, *args):

        self.dimensions = self.width, self.height

        if self.minimum_width > self.width:
            self.width = self.minimum_width

        with self.canvas:
            self.spirit.size = self.dimensions


class HamburgerMenuLine:
    def __init__(self, *, points: tuple, color: tuple, **kwargs):
        self.points = points
        self.color = color
        self.width, self.height = 80, 2

    def __call__(self, *args, **kwargs):
        with self.canvas:
            Color(*self.color)
            return Line(rounded_rectangle=(self.points[0], self.points[1], self.width, self.height, 20, 20, 10, 10))


class HamburgerMenuToggleButton(AnchorLayout):
    def __init__(self, **kwargs):
        super(HamburgerMenuToggleButton, self).__init__(**kwargs)
        self.topline = HamburgerMenuLine(points=(self.x + 5, self.top - 5))

    def on_size(self, *args):
        self.topline = HamburgerMenuLine(points=(self.x + 5, self.top - 5), color=(1, 1, 1, 1))


class Link(Button):

    minimum_x = 2
    background_color = 1, 1, 1, 0

    def __init__(self, **kwargs):
        super(Link, self).__init__(**kwargs)
        self.height *= 2
        self.pos[0] = self.minimum_x

    def on_pos(self, *args):
        if self.pos[0] < self.minimum_x:
            self.pos[0] = self.minimum_x


class MainMenuLink(Link):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Main menu"


class MySchedulesLink(Link):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "My schedules"


class MyActivitiesLink(Link):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "My activities"


class TestApp(App):
    pass


if __name__ == '__main__':
    TestApp().run()
