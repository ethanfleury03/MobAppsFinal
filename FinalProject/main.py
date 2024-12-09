from kivymd.app import MDApp
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.carousel import Carousel
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.effects.scroll import ScrollEffect
from databaseconn import initialize_database, add_user, check_login
import time, requests, sys

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
        
    def on_search(self):
        """Search logic (mock)."""
        city_or_zip = self.ids.city_or_zipid.text
        geo_range = self.ids.radius_input.text
        species = "dog" if self.ids.dog_toggle.state == "down" else "cat"
        sex = "m" if self.ids.male_toggle.state == "down" else "f" 
        age_range = ""
        if self.ids.age_0_2_toggle.state == "down":
            age_range = "puppy"
        elif self.ids.age_3_7_toggle.state == "down":
            age_range = "young"
        elif self.ids.age_8plus_toggle.state == "down":
            age_range = "adult"

        print(f"Search parameters:")
        print(f"  City/Zip: {city_or_zip}")
        print(f"  Radius: {geo_range} miles")
        print(f"  Species: {species}")
        print(f"  Sex: {sex}")
        print(f"  Age Range: {age_range}")

        petcard_screen = self.manager.get_screen('petcard')
        petcard_screen.city_or_zip = city_or_zip
        petcard_screen.geo_range = geo_range
        petcard_screen.species = species
        petcard_screen.sex = sex
        petcard_screen.age_range = age_range
        self.manager.current = "petcard"
      

class PetCard(MDCard):
    pet_name = StringProperty("")
    pet_image = StringProperty("")
    pet_age = StringProperty("")
    pet_sex = StringProperty("")
    pet_location = StringProperty("")

    def __init__(self, pet_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(10)
        self.spacing = dp(5)
        self.size_hint = (None, None)
        self.size = (dp(150), dp(200))  # Fixed size for the card
        self.radius = [10]
        self.elevation = 2

class PetCardScreen(Screen):
    city_or_zip = StringProperty("")
    geo_range = StringProperty("")
    species = StringProperty("")
    sex = StringProperty("")
    age_range = StringProperty("")

    def on_enter(self):
        pets = self.fetch_pets()
        self.populate_cards(pets)

    def populate_cards(self, pets):
        scrollable_layout = self.ids.scrollable_layout
        scrollable_layout.clear_cards()

        for pet in pets:
            card = PetCard(pet_data=pet)
            scrollable_layout.add_card(card)

    def fetch_pets(self):
        BASE_URL = "https://api-staging.adoptapet.com/search/pet_search"
        API_KEY = "hg4nsv85lppeoqqixy3tnlt3k8lj6o0c"

        city_or_zip = self.city_or_zip
        geo_range = self.geo_range
        species = self.species
        sex = self.sex
        # breed = self.breed
        age_range = self.age_range

        start_number = 1
        end_number = 30

        url = f"{BASE_URL}?key={API_KEY}&v=3&output=json&city_or_zip={city_or_zip}&geo_range={geo_range}&species={species}&sex={sex}&age={age_range}&start_number={start_number}&end_number={end_number}"
        
        headers = {
            'Accept': 'application/json; charset=UTF8'
        }
        print(f"Request URL: {url}")
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            print("Response content:", response.text)
            pets_data = response.json()
            print(f"Response Data: {pets_data}")
            if 'pet' in pets_data:
                return [self.format_pet_data(pet) for pet in pets_data['pet']]
            else:
                print("No pets found in the response")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []
        
    def format_pet_data(self, pet):
        return {
            'image_url': pet.get('large_results_photo_url', ''),
            'name': pet.get('pet_name', ''),
            'age': pet.get('age', ''),
            'sex': pet.get('sex', ''),
            'location': f"{pet.get('addr_city', '')}, {pet.get('addr_state_code', '')}"
        }


class ScrollableCardLayout(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.card_grid = GridLayout(
            cols=4,
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None,
        )
        self.card_grid.bind(minimum_height=self.card_grid.setter('height'))
        self.add_widget(self.card_grid)

    def add_card(self, card):
        self.card_grid.add_widget(card)
    
    def clear_cards(self):
        self.card_grid.clear_widgets()


class MyApp(MDApp):
    def build(self):
        # Initialize the database
        initialize_database()

        # Set up the screen manager
        sm = ScreenManager()
        sm.add_widget(SignUpScreen(name="signup"))
        sm.add_widget(SignInScreen(name="signin"))
        sm.add_widget(PetFinderScreen(name="petfinder"))
        sm.add_widget(PetCardScreen(name="petcard"))
        return sm


if __name__ == "__main__":
    MyApp().run()