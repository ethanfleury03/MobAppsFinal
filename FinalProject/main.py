from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.carousel import Carousel
from kivymd.uix.card import MDCard
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

class PetCarousel(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.effect_cls = ScrollEffect
        self.scroll_type = ['bars', 'content']
        self.bar_width = 0
        self.scroll_wheel_distance = 100
        self.container = BoxLayout(orientation='horizontal', size_hint_x=None, spacing=20)
        self.add_widget(self.container)

    def add_card(self, card):
        self.container.add_widget(card)
        self.container.width += card.width + self.container.spacing

class PetCard(MDCard):
    def __init__(self, pet_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint = (0.8, 0.8)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.padding = 10

        name_label = Label(text=pet_data["name"], font_size=24, size_hint_y=0.2)
        image = Image(source=pet_data["image"], size_hint_y=0.8)

        self.add_widget(name_label)
        self.add_widget(image)

class PetFinderScreen(Screen):
    """Screen for user to find pet wanted."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.carousel = PetCarousel(size_hint=(0.9, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.add_widget(self.carousel)
        

    def populate_dropdown(self):
        """Populate the dropdown menu."""
        dropdown = self.ids.dropdown
        grid = self.ids.options_grid  # Reference the GridLayout inside the dropdown

        for item in self.items:
            btn = Button(text=item, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn, item=item: self.select_breed_option(item))
            grid.add_widget(btn)

    def select_breed_option(self, option_text):
        """Handle selecting a Breed option from the dropdown."""
        print(f"Selected Breed: {option_text}")
        self.ids.main_button.text = option_text  # Update the main button's text
        self.ids.dropdown.dismiss()  # Close the dropdown
    

    def populate_cards(self, search_results):
        self.carousel.container.clear_widgets()
        for pet in search_results:
            card = PetCard(pet)
            self.carousel.add_card(card)

    def on_search(self, search_query):
        """Search logic (mock)."""
        # Example search results
        pet_results = self.fetch_pets(search_query)
        if pet_results:
            self.populate_cards(pet_results)
        else:
            print("No pets found.")

    def format_pet_data(self, pet):
        return {
            "name": pet.get('name', 'N/A'),
            "image": pet.get('large_results_photo_url', 'default_image.jpg'),
            "breed": pet.get('breed', 'N/A'),
            "age": pet.get('age', 'N/A'),
            "sex": pet.get('sex', 'N/A')
        }
    
    def fetch_pets(self, query):
        BASE_URL = "https://api-staging.adoptapet.com/search/pet_search"
        API_KEY = "hg4nsv85lppeoqqixy3tnlt3k8lj6o0c"

        city_or_zip = query
        geo_range = self.radius_input.text or "50"
        species = "dog" if self.ids.dog_toggle.state == "down" else "cat"
        sex = "m" if self.ids.male_toggle.state == "down" else "f" if self.ids.female_toggle.state == "down" else ""
        breed = self.ids.main_button.text if self.ids.main_button.text != "Breed" else ""

        if self.ids.age_0_2_toggle.state == "down":
            age_range = "0-2"
        elif self.ids.age_3_7_toggle.state == "down":
            age_range = "3-7"
        elif self.ids.age_8plus_toggle.state == "down":
            age_range = "8+"
        else:
            age_range = ""

        start_number = 1
        end_number = 10

        url = f"{BASE_URL}?key={API_KEY}&v=3&output=json&city_or_zip={city_or_zip}&geo_range={geo_range}&species={species}&breed={breed}&sex={sex}&age={age_range}&start_number={start_number}&end_number={end_number}"
        
        headers = {
            'Accept': 'application/json; charset=UTF8'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            pets_data = response.json()
            if 'pet' in pets_data:
                return [self.format_pet_data(pet) for pet in pets_data['pet']]
            else:
                print("No pets found in the response")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []   
    
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
