from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty
from databaseconn import connect_to_database, add_user, check_login

class SignUpScreen(Screen):
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

    def login(self):
        email = self.ids["email_input"].text
        password = self.password_input.text

        if check_login(email, password):
            self.manager.current = "second"

        else:
            self.feedback_label

class SignInScreen(Screen):
    pass

class PetFinderScreen(Screen):
    pass

class PetLocaterScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LogInScreen(name="login"))
        sm.add_widget(SecondScreen(name="second"))
        sm.add_widget(ThirdScreen(name="third"))
        return sm

if __name__ == "__main__":
    MyApp().run()
