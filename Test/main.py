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

        self.spirit = None
        self.pos = 0, 0
        self.size_hint = None, 1
        self.width = Window.width * .15
        self.height = Window.height
        self.spirit_width = Window.width * .15
        self.spirit_height = Window.height

        self.orientation = 'vertical'

        Window.bind(size=self.on_size)


    def on_size(self, *args):

        global MINIMUM_NAVIGATION_MENU_WIDTH

        if MINIMUM_NAVIGATION_MENU_WIDTH > self.width:
            Window.unbind(size=self.on_size)
            Window.bind(size=self.size_binder)

        self.spirit_width = Window.width * .15
        self.spirit_height = Window.height

        with self.canvas:

            Color(1, 1, 1, 1)

            try:
                self.spirit.size = self.size
            except AttributeError:
                self.spirit = Rectangle(pos=self.pos, size=(self.spirit_width, self.spirit_height))

    def size_binder(self, *args):
        if MINIMUM_NAVIGATION_MENU_WIDTH < Window.width * .15:
            Window.unbind(size=self.size_binder)
            Window.bind(size=self.on_size)

    def step_hide(self, dt, speed: int = 10):
        global navigation_menu_sliding_in_process

        if self.spirit_width > 0:
            self.spirit_width -= speed
            self.spirit.size = self.spirit_width, self.spirit_height
        else:
            Clock.unschedule(self.step_hide)
            navigation_menu_sliding_in_process = False

    def step_show(self, dt, speed: int = 10):
        global navigation_menu_sliding_in_process

        if self.spirit_width <= Window.width * .15:
            self.spirit_width += speed
            self.spirit.size = self.spirit_width, self.spirit_height
        else:
            Clock.unschedule(self.step_show)
            navigation_menu_sliding_in_process = False


class NavigationMenu(BoxLayout):

    def __init__(self, **kwargs):
        super(NavigationMenu, self).__init__(**kwargs)

        self.border = None

        self.width = Window.width * .15
        self.height = Window.height * .8
        self.size_hint = None, None

        self.orientation = 'vertical'

        Window.bind(width=self.on_width)

    def on_size(self, *args):
        self.size[1] = Window.height * .8 - dp(60)

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

    def step_hide(self, dt, speed: int = 10):
        global navigation_menu_sliding_in_process

        self.x -= speed
        self.border.points = self.x + self.width, 0, self.x + self.width, Window.height

        for child in self.children:
            child.pos[0] -= speed
        if self.x + self.width < 0:
            Clock.unschedule(self.step_hide)
            navigation_menu_sliding_in_process = False

    def step_show(self, dt, speed: int = 10):
        global navigation_menu_sliding_in_process

        self.x += speed
        self.border.points = self.x + self.width, 0, self.x + self.width, Window.height

        for child in self.children:
            child.pos[0] += speed
        if self.x > 0:
            Clock.unschedule(self.step_show)
            navigation_menu_sliding_in_process = False


class HamburgerMenuToggleButton(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = None, None
        self.width = Window.width * .1

        self.toggled = BooleanProperty(True)
        self.pixels_hidden = 0

        Window.bind(size=self.on_size)

        with self.canvas:
            Color(128 / 255, 128 / 255, 128 / 255, 1)
            self.topline = Line(points=(self.x + Window.width * .025, Window.height * .85, Window.width * .125,
                                        Window.height * .85), width=2)
            self.midline = Line(points=(self.x + Window.width * .025, Window.height * .825, Window.width * .125,
                                        Window.height * .825), width=2)
            self.bottline = Line(points=(self.x + Window.width * .025, Window.height * .8, Window.width * .125,
                                         Window.height * .8), width=2)

    def on_size(self, *args):
        self.x = Window.width * .05
        self.y = Window.height * .75

        with self.canvas:
            Color(128 / 255, 128 / 255, 128 / 255, 1)

            self.topline.points = self.x, Window.height * .85, Window.width * .1, Window.height * .85
            self.midline.points = self.x, Window.height * .825, Window.width * .1, Window.height * .825
            self.bottline.points = self.x, Window.height * .8, Window.width * .1, Window.height * .8
            print(self.x)


    def on_touch_down(self, touch):
        global navigation_menu_sliding_in_process

        self.x = Window.width * .05
        self.y = Window.height * .75

        if self.x < touch.x < self.x + self.width and self.y < touch.y < self.y + self.height:
            self.toggled = not self.toggled
            if not navigation_menu_sliding_in_process:
                if self.toggled:
                    Clock.schedule_interval(self.parent.children[1].step_show, 1 / 60)
                    Clock.schedule_interval(self.parent.step_show, 1 / 60)
                else:
                    Clock.schedule_interval(self.parent.children[1].step_hide, 1 / 60)
                    Clock.schedule_interval(self.parent.step_hide, 1 / 60)
                navigation_menu_sliding_in_process = True


class Link(Button):

    minimum_x = 2
    background_color = 1, 1, 1, 0

    def __init__(self, **kwargs):
        super(Link, self).__init__(**kwargs)

        self.height = Window.height * .8 / 3
        self.pos[0] = self.minimum_x

    def on_size(self, *args):
        pass


class MainMenuLink(Link):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.text = "Main menu"
        self.font_size = dp(15)
        self.color = 0, 0, 0


class MySchedulesLink(Link):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.text = "My schedules"
        self.font_size = dp(15)
        self.color = 0, 0, 0


class MyActivitiesLink(Link):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.text = "My activities"
        self.font_size = dp(15)
        self.color = 0, 0, 0


class TestApp(App):
    pass


navigation_menu_sliding_in_process: bool = False


if __name__ == '__main__':
    TestApp().run()
