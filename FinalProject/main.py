from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from databaseconn import initialize_database, add_user, check_login

# Ethan and Adam
class SignUpScreen(Screen):
    # References to UI elements
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    confirm_input = ObjectProperty(None)
    feedback_label = ObjectProperty(None)

    def check_password_match(self):
        """Check if password and confirm password match."""
        password = self.password_input.text
        confirm_password = self.confirm_input.text

        if password == confirm_password and password:
            self.feedback_label.text = "Passwords match."
            self.feedback_label.color = (0, 1, 0, 1)  # Green
        else:
            self.feedback_label.text = "Passwords do not match."
            self.feedback_label.color = (1, 0, 0, 1)  # Red

    def sign_up(self):
        """Handle sign-up logic."""
        username = self.username_input.text
        password = self.password_input.text
        confirm_password = self.confirm_input.text

        if not username or not password or not confirm_password:
            self.feedback_label.text = "All fields are required."
            self.feedback_label.color = (1, 0, 0, 1)  # Red
            return

        if password != confirm_password:
            self.feedback_label.text = "Passwords do not match."
            self.feedback_label.color = (1, 0, 0, 1)  # Red
            return

        # Attempt to add the user
        if add_user(username, password):
            self.feedback_label.text = "Sign-up successful!"
            self.feedback_label.color = (0, 1, 0, 1)  # Green
        else:
            self.feedback_label.text = "Sign-up failed. Try a different username."
            self.feedback_label.color = (1, 0, 0, 1)  # Red


class SignInScreen(Screen):
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    feedback_label = ObjectProperty(None)

    def sign_in(self):
        """Handle sign-in logic."""
        username = self.username_input.text
        password = self.password_input.text

        if not username or not password:
            self.feedback_label.text = "Both fields are required."
            self.feedback_label.color = (1, 0, 0, 1)  # Red
            return

        # Check login credentials
        if check_login(username, password):
            self.manager.current = "petfinder"  # Navigate to the next screen
        else:
            self.feedback_label.text = "Invalid username or password."
            self.feedback_label.color = (1, 0, 0, 1)  # Red


class PetFinderScreen(Screen):
    pass


class MyApp(App):
    def build(self):
        # Initialize the database
        initialize_database()

        # Set up the screen manager
        sm = ScreenManager()
        sm.add_widget(SignUpScreen(name="signup"))
        sm.add_widget(SignInScreen(name="signin"))
        sm.add_widget(PetFinderScreen(name="petfinder"))
        return sm


if __name__ == "__main__":
    MyApp().run()
