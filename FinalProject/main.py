from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from databaseconn import initialize_database, add_user, check_login
import time
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

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
            self.manager.current = 'signin'
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
    """Screen for user to find pet wanted."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = [f"Breed {i}" for i in range(1, 151)]  # Example list of 150 items
        self.populate_dropdown()

    def populate_dropdown(self):
        """Populate the dropdown menu."""
        dropdown = self.ids.dropdown
        grid = self.ids.options_grid  # Reference the GridLayout inside the dropdown

        for item in self.items:
            btn = Button(text=item, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn, item=item: self.select_pet_option(item))
            grid.add_widget(btn)

    def select_pet_option(self, option_text):
        """Handle selecting a pet option from the dropdown."""
        print(f"Selected pet: {option_text}")
        self.ids.main_button.text = option_text  # Update the main button's text
        self.ids.dropdown.dismiss()  # Close the dropdown
    
    def on_search(self, search_query):
        """Search logic (mock)."""
        # Example search results
        mock_results = [
            {"name": "Buddy", "image": "dog_image.jpg"},
            {"name": "Kitty", "image": "cat_image.jpg"},
        ]
        pet_selector_screen = self.manager.get_screen("pet_selector")
        self.manager.current = "pet_selector"


    def fetch_pets(self, query):
        pass

class PetSelectorScreen(Screen):
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
        sm.add_widget(PetSelectorScreen(name="pet_selector"))
        return sm


if __name__ == "__main__":
    MyApp().run()
