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
        self.dropdown = DropDown()
        
    def update_breed_dropdown(self):
        self.dropdown.clear_widgets()
        
        dog_breeds = [
    "Affenpinscher", "Afghan Hound", "African Hunting Dog", "Airedale Terrier",
    "Akita", "Alaskan Malamute", "American Bulldog", "American Cocker Spaniel",
    "American Pit Bull Terrier", "American Staffordshire Terrier", "Anatolian Shepherd Dog",
    "Aspin Dog", "Australian Cattle Dog", "Australian Kelpie", "Australian Shepherd",
    "Australian Silky Terrier", "Australian Stumpy Tail Cattle Dog", "Australian Terrier",
    "Basenji", "Basset Fauve De Bretagne", "Basset Hound", "Beagle", "Bearded Collie",
    "Bedlington Terrier", "Belgian Malinois", "Belgian Shepherd", "Belgian Sheepdog",
    "Belgian Tervuren", "Bergamasco Sheepdog", "Bernese Mountain Dog", "Bichon Frise",
    "Black and Tan Coonhound", "Black Russian Terrier", "Bloodhound", "Border Collie",
    "Border Terrier", "Borzoi", "Boston Terrier", "Bouvier Des Flandres", "Boxer",
    "Boykin Spaniel", "Bracco Italiano", "Briard", "British Bulldog", "Brittany",
    "Brussels Griffon", "Bull Terrier", "Bulldog", "Bullmastiff", "Cairn Terrier",
    "Cavalier King Charles Spaniel", "Chesapeake Bay Retriever", "Chihuahua",
    "Chinese Crested Dog", "Chinese Shar-Pei", "Chow Chow", "Clumber Spaniel",
    "Cocker Spaniel", "Collie", "Coonhound", "Corgi (Cardigan)", "Corgi (Pembroke)",
    "Curly Coated Retriever", "Dachshund", "Dalmatian", "Dandie Dinmont Terrier",
    "Danish Spitz", "Danish–Swedish Farmdog", "Deerhound", "Dikkulak", "Dingo",
    "Dobermann", "Dogo Argentino", "Dogo Sardesco", "Dogue Brasileiro",
    "Dogue de Bordeaux", "Donggyeongi", "Drentse Patrijshond", "Drever", "Dunker",
    "Dutch Shepherd", "Dutch Smoushond", "East European Shepherd",
    "East Siberian Laika", "Ecuadorian Hairless Dog", "English Cocker Spaniel",
    "English Foxhound", "English Mastiff", "English Setter", "English Shepherd",
    "English Springer Spaniel", "English Toy Terrier (Black & Tan)",
    "Entlebucher Mountain Dog", "Erbi Txakur", "Estonian Hound",
    "Estrela Mountain Dog", "Eurasier", "Faroese Sheepdog", "Field Spaniel",
    "Fila Brasileiro", "Finnish Hound", "Finnish Lapphund", "Finnish Spitz",
    "Flat-coated Retriever", "Florida Brown Dog", "French Bulldog", "French Spaniel",
    "Galgo Español", "Gascon Saintongeois", "Gaucho sheepdog", "German Shepherd",
    "German Short-Haired Pointer", "German Wirehaired Pointer", "Golden Retriever",
    "Gordon Setter", "Great Dane", "Greyhound", "Griffon Bruxellois", "Hungarian Vizsla",
    "Irish Setter", "Irish Terrier", "Irish Water Spaniel", "Irish Wolfhound",
    "Italian Greyhound", "Jack Russell", "Japanese Chin", "Japanese Spitz", "Keeshond",
    "King Charles Spaniel", "Labrador", "Labrador Retriever", "Lagotto Romagnolo",
    "Lài", "Lakeland Terrier", "Lancashire Heeler", "Landseer", "Lapponian Herder",
    "Large Münsterländer", "Leonberger", "Levriero Sardo", "Lhasa Apso", "Liangshan Dog",
    "Lithuanian Hound", "Lobito Herreño", "Löwchen", "Lucas Terrier", "Lupo Italiano",
    "Mackenzie River Husky", "Magyar Agár", "Mahratta Hound", "Majorca Shepherd Dog",
    "Maltese", "Manchester Terrier", "Maneto", "Maremma Sheepdog", "Markiesje",
    "Maremmano-Abruzzese Sheepdog", "Mastiff", "McNab", "Miniature American Shepherd",
    "Miniature Bull Terrier", "Miniature Fox Terrier", "Miniature Pinscher",
    "Miniature Schnauzer", "Molossus of Epirus", "Mongrel",
    "Montenegrin Mountain Hound", "Moscow Watchdog", "Mountain Cur", "Mountain Feist",
    "Mudhol Hound", "Mudi", "Munsterlander", "Neapolitan Mastiff",
    "Nenets Herding Laika", "New Guinea singing dog", "New Zealand Heading Dog",
    "Newfoundland", "Norfolk Terrier", "Norrbottenspets", "Northern Inuit Dog",
    "Norwegian Buhund", "Nova Scotia Duck Tolling Retriever", "Old English Sheep Dog",
    "Papillon", "Pekingese", "Petit Basset Griffon Vendéen", "Pharaoh Hound",
    "Pointer", "Pomeranian", "Poodle", "Portuguese Water Dog", "Pug", "Puli",
    "Pyrenean Mountain Dog", "Rhodesian Ridgeback", "Rottweiler", "Saint Bernard",
    "Saluki", "Samoyed", "Schipperke", "Schnauzer", "Scottish Terrier",
    "Sealyham Terrier", "Shar Pei", "Shetland Sheepdog", "Shih Tzu", "Siberian Husky",
    "Skye Terrier", "Soft Coated Wheaten Terrier", "Staffordshire Bull Terrier",
    "Sussex Spaniel", "Swedish Vallhund", "Tibetan Spaniel", "Tibetan Terrier",
    "Weimaraner", "Welsh Corgi", "Welsh Springer Spaniel", "West Highland White Terrier",
    "Whippet", "Yorkshire Terrier"
]
        cat_breeds = [
    "Abyssinian", "Aegean", "American Bobtail", "American Curl", "American Ringtail",
    "American Shorthair", "American Wirehair", "Arabian Mau", "Asian", 
    "Asian Longhair (Tiffany)", "Australian Mist", "Balinese", "Bambino", 
    "Bengal", "Birman", "Bombay", "Bramble", "Brazilian Shorthair", 
    "British Longhair", "British Shorthair", "Burmese", "Burmilla",
    "California Spangled (extinct)", "Chantilly-Tiffany", "Chartreux",
    "Chausie", "Cheetoh", "Cornish Rex", "Cymric (Longhaired Manx)", 
    "Desert Lynx", "Devon Rex", "Donskoy (Don Sphynx)", 
    "Dragon Li (Chinese Li Hua)", "Egyptian Mau", 
    "European Shorthair", "Exotic Shorthair", 
    "FoldEx (Scottish Fold x Exotic)", 
    "German Rex", "Havana Brown",
    "Highlander (Highland Lynx)", 
    "Himalayan (Colorpoint Persian)", 
    "Japanese Bobtail", 
    "Javanese (Colorpoint Longhair)", 
    "Jungle Curl",
    "Khao Manee", 
    "Korat",
    "Kurilian Bobtail",
    "LaPerm",
    "Lambkin",
    "Lykoi",
    "Maine Coon",
    "Mandalay",
    "Manx",
    "Minskin",
    "Minuet (Napoleon)",
    "Mojave Spotted",
    "Munchkin",
    "Nebelung",
    "Norwegian Forest Cat",
    "Ocicat",
    "Oriental Longhair",
    "Oriental Shorthair",
    "Persian (including Exotic Longhair)",
    "Peterbald",
    "Pixie-Bob",
    "Raas (Busok)",
    "Ragdoll",
    "Ragamuffin",
    "Russian Blue",
    "Russian White, Black, and Tabby",
    "Safari",
    "Sam Sawet",
    "Savannah",
    "Scottish Fold",
    "Selkirk Rex",
    "Serengeti",
    "Serrade Petit",
    "Siamese",
    "Siberian Forest Cat (Siberian)",
    "Singapura",
    "Skookum",
    "Snowshoe",
    "Sokoke",
    "Somali",
    "Sphynx",
    "Suphalak",
    "Thai (Traditional Siamese)",
    "Tonkinese",
    "Toyger",
    "Turkish Angora",
    "Turkish Van"
]

        if self.ids.dog_toggle.state == "down":
            items = dog_breeds
        else:
            items = cat_breeds

        for item in items:
            btn = Button(text=item, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn, item=item: self.select_breed_option(item))
            self.dropdown.add_widget(btn)

        self.dropdown.open(self.ids.main_button)

    def select_item(self, text):
        # Update the button text with the selected item
        self.ids.main_button.text = text
        self.dropdown.dismiss()

    def select_breed_option(self, option_text):
        """Handle selecting a Breed option from the dropdown."""
        print(f"Selected Breed: {option_text}")
        self.ids.main_button.text = option_text  # Update the main button's text
        self.ids.dropdown.dismiss()  # Close the dropdown
    


    def on_search(self):
        """Search logic (mock)."""
        city_or_zip = self.ids.city_or_zipid.text
        geo_range = self.ids.radius_input.text
        species = "dog" if self.ids.dog_toggle.state == "down" else "cat"
        sex = "m" if self.ids.male_toggle.state == "down" else "f" 
        breed = self.ids.main_button.text if self.ids.main_button.text != "Breed" else ""
        age_range = ""
        if self.ids.age_0_2_toggle.state == "down":
            age_range = "0-2"
        elif self.ids.age_3_7_toggle.state == "down":
            age_range = "3-7"
        elif self.ids.age_8plus_toggle.state == "down":
            age_range = "8+"

        print(f"Search parameters:")
        print(f"  City/Zip: {city_or_zip}")
        print(f"  Radius: {geo_range} miles")
        print(f"  Species: {species}")
        print(f"  Sex: {sex}")
        print(f"  Breed: {breed}")
        print(f"  Age Range: {age_range}")

        petcard_screen = self.manager.get_screen('petcard')
        petcard_screen.city_or_zip = city_or_zip
        petcard_screen.geo_range = geo_range
        petcard_screen.species = species
        petcard_screen.sex = sex
        petcard_screen.breed = breed
        petcard_screen.age_range = age_range
        self.manager.current = "petcard"
      

class PetCard(MDCard):
    name = StringProperty("")
    image = StringProperty("")

    def __init__(self, pet_data, **kwargs):
        super().__init__(**kwargs)
        self.name = pet_data.get("name", "Unknown")  # Default name if not provided
        self.image = pet_data.get("image", "")  # Default image if not provided

        # Debug image path
        print("Image path:", self.image)

        # Set MDCard properties
        self.orientation = "vertical"
        self.padding = dp(10)
        self.size_hint = (None, None)
        self.size = (dp(150), dp(200))  # Fixed size for the card
        self.radius = [10]

        # Create a BoxLayout to hold the image and label
        content = BoxLayout(orientation="vertical", spacing=dp(10))
        
        # Add the Image widget
        image_widget = Image(
            source=self.image,
            allow_stretch=True,
            size_hint_y=0.7  # Image takes 70% of the card height
        )
        content.add_widget(image_widget)

        # Add the Label widget
        label_widget = Label(
            text=self.name,
            font_size=dp(16),
            halign="center",
            size_hint_y=0.3  # Label takes 30% of the card height
        )
        content.add_widget(label_widget)

        # Add the content to the card
        self.add_widget(content)

class PetCardScreen(Screen ):
    city_or_zip = StringProperty("")
    geo_range = StringProperty("")
    species = StringProperty("")
    sex = StringProperty("")
    breed = StringProperty("")
    age_range = StringProperty("")

    def on_enter(self):
        pets = self.fetch_pets
        self.populate_cards(pets)

    def populate_cards(self, pets):
        print("IDs:", self.ids)  # This will show all available ids
        print("Scrollable Layout:", self.ids.scrollable_layout)
        scrollable_layout = self.ids.scrollable_layout
        scrollable_layout.card_grid.clear_widget(card)
        for pet in pets:
            card = PetCard(pet_data=pet)
            scrollable_layout.card_grid.add_widget(card)

    def fetch_pets(self):
        BASE_URL = "https://api-staging.adoptapet.com/search/pet_search"
        API_KEY = "hg4nsv85lppeoqqixy3tnlt3k8lj6o0c"

        city_or_zip = self.city_or_zip
        geo_range = self.geo_range
        species = self.species
        sex = self.sex
        breed = self.breed
        age_range = self.age_range

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