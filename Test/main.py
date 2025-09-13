from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.uix.button import Button

DEFAULT_SCREEN_WIDTH: int = 1280
DEFAULT_SCREEN_HEIGHT: int = 720

MINIMUM_NAVIGATION_MENU_WIDTH: int = 120

Config.set('graphics', 'width', str(DEFAULT_SCREEN_WIDTH))
Config.set('graphics', 'height', str(DEFAULT_SCREEN_HEIGHT))

from kivy.app import App
from kivy.graphics import Rectangle, Line, Color
from kivy.uix.boxlayout import BoxLayout


class MainWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

    def on_size(self, *args):
        pass


class LeftSideLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(LeftSideLayout, self).__init__(**kwargs)
        self.id = "LeftSideLayout"
        self.spirit = None
        self.pos = 0, 0
        self.size_hint = None, 1
        self.width = Window.width * .15
        self.height = Window.height
        self.orientation = 'vertical'
        Window.bind(size=self.on_size)


    def on_size(self, *args):

        global MINIMUM_NAVIGATION_MENU_WIDTH

        if MINIMUM_NAVIGATION_MENU_WIDTH > self.width:
            Window.unbind(size=self.on_size)
            Window.bind(size=self.size_binder)

        self.width = Window.width * .15

        with self.canvas:
            Color(1, 1, 1, 1)
            try:
                self.spirit.size = self.size
            except AttributeError:
                self.spirit = Rectangle(pos=self.pos, size=(self.width, self.height))

    def size_binder(self, *args):
        if MINIMUM_NAVIGATION_MENU_WIDTH < Window.width * .15:
            Window.unbind(size=self.size_binder)
            Window.bind(size=self.on_size)


class NavigationMenu(BoxLayout):

    def __init__(self, **kwargs):
        super(NavigationMenu, self).__init__(**kwargs)
        self.id = "NavigationMenu"
        self.border = None
        self.width = Window.width * .15
        self.height = Window.height * .8
        self.size_hint = None, None
        self.orientation = 'vertical'
        Window.bind(width=self.on_width)

    def on_width(self, *args):

        global MINIMUM_NAVIGATION_MENU_WIDTH

        if MINIMUM_NAVIGATION_MENU_WIDTH > self.width:
            Window.unbind(width=self.on_width)
            Window.bind(width=self.width_binder)

        self.width = Window.width * .15

        with self.canvas:
            Color(1, 1, 0, 1)
            try:
                self.border.points = self.width, 0, self.width, Window.height
            except AttributeError:
                self.border = Line(points=(self.width, 0, self.width, Window.height), width=2)

    def width_binder(self, *args):
        if MINIMUM_NAVIGATION_MENU_WIDTH < Window.width * .15:
            Window.unbind(width=self.width_binder)
            Window.bind(width=self.on_width)

    def step_hide(self, dt, speed: int = 3):
        self.x -= speed
        self.border.points = self.x + self.width, 0, self.x + self.width, Window.height
        for child in self.children:
            child.pos[0] -= 1
        if self.x + self.width < 0:
            Clock.unschedule(self.step_hide)


    class HamburgerMenuToggleButton(BoxLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.id = "HamburgerMenuToggleButton"
            self.toggled = BooleanProperty(True)
            self.pixels_hidden = 0
            self.size_hint = None, None
            self.width = dp(90)
            self.pos_hint = { 'center_x': Window.width * 0.00055, 'y': Window.height * .75 }

        def on_touch_down(self, *args):
            self.toggled = not self.toggled
            Clock.schedule_interval(self.parent.step_hide, 1 / 30)
            # Clock.schedule_interval()


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
        self.id = "MainMenuLink"
        self.text = "Main menu"
        self.font_size = dp(15)
        self.color = 0, 0, 0


class MySchedulesLink(Link):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = "MySchedulesLink"
        self.text = "My schedules"
        self.font_size = dp(15)
        self.color = 0, 0, 0


class MyActivitiesLink(Link):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = "MyActivitiesLink"
        self.text = "My activities"
        self.font_size = dp(15)
        self.color = 0, 0, 0


class TestApp(App):
    pass


if __name__ == '__main__':
    TestApp().run()
