from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout


class MainScreen(Screen):
    pass

class SecondScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SecondScreen(name="second"))
        return sm

if __name__ == "__main__":
    MyApp().run()

