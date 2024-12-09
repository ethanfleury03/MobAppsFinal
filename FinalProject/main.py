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
import folium
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, requests, sys, os

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

        self.pet_name = pet_data.get('name', 'Unknown')
        self.pet_image = pet_data.get('image_url', '')
        self.pet_age = pet_data.get('age', 'Unknown')
        self.pet_sex = pet_data.get('sex', 'Unknown')
        self.pet_location = pet_data.get('location', 'Unknown')

    def make_background(self, zip):
        maps_dir = "maps"
    
        # Ensure the 'maps' directory exists
        if not os.path.exists(maps_dir):
            os.makedirs(maps_dir)
        
        # Geocode the ZIP code
        geolocator = Nominatim(user_agent="petfinder")
        location = geolocator.geocode(zip)
        
        if not location:
            print(f"Invalid ZIP code: {zip}")
            return "default_image.png"  # Fallback to a default image
        
        lat, lon = location.latitude, location.longitude
        
        # Create a Folium map centered at the location
        m = folium.Map(location=[lat, lon], zoom_start=15)
        folium.Marker(location=[lat, lon], popup=self.pet_name).add_to(m)
        
        # Save the map as an HTML file
        map_file = f"maps/{self.pet_name}.html"
        m.save(map_file)

        # Convert the HTML map to an image
        image_file = f"maps/{self.pet_name}.png"
        
        # Ensure the map file is saved and exists
        if not os.path.exists(map_file):
            print(f"Error: Map file not found at {map_file}")
            return "default_image.png"
        
        # Setup Selenium WebDriver with WebDriverManager
        options = Options()
        options.headless = True  
        options.add_argument('--disable-gpu') 
        options.add_argument('--no-sandbox')  
        options.add_argument('--remote-debugging-port=9222')
        
        # Use WebDriverManager to automatically download and setup ChromeDriver
        service = Service(ChromeDriverManager().install())  # WebDriverManager handles the chromedriver
        with webdriver.Chrome(service=service, options=options) as driver:
            # Use absolute path for the map HTML file
            absolute_map_path = os.path.abspath(map_file)
            file_url = f"file:///{absolute_map_path}"

            # Load the map HTML file
            driver.get(file_url)
            try:
                # Wait until a marker is visible on the map (can be any element you want to wait for)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'leaflet-marker-icon'))  # Wait for marker to load
                )
            except Exception as e:
                print(f"Error waiting for the map to load: {e}")
                return "default_image.png"
            
            # Save a screenshot of the map as an image
            driver.save_screenshot(image_file)
        
        print(f"Map image saved to {image_file}")
        return image_file
    
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
        layout = self.ids.card_layout 
        layout.clear_widgets()

        for pet in pets:
            card = PetCard(pet_data=pet)
            layout.add_widget(card)

    def fetch_pets(self):
        BASE_URL = "https://api-staging.adoptapet.com/search/pet_search"
        API_KEY = "hg4nsv85lppeoqqixy3tnlt3k8lj6o0c"

        city_or_zip = self.city_or_zip
        geo_range = self.geo_range
        species = self.species
        sex = self.sex
        age_range = self.age_range

        start_number = 1
        end_number = 8

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
            if pets_data.get("status") == "ok" and "pets" in pets_data:
                pets = pets_data["pets"]
                return [self.format_pet_data(pet) for pet in pets]  # Format pet data to be used
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