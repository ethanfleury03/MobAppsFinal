from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty


class MainScreen(Screen):
    password_input = ObjectProperty(None)
    confirm_input = ObjectProperty(None)
    feedback_label = ObjectProperty(None)

    def check_password_match(self):

        password = self.password_input.text
        confirm_password = self.confirm_input.text

        if password == confirm_password and password:
            self.feedback_label.text = "Password Matches"
            self.feedback_label.color = (0, 1, 0, 1)
        else:
            self.feedback_label.text = "Password does not match"
            self.feedback_label.color = (1, 0, 0, 1)

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

