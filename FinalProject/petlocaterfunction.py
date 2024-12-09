import requests
import sys
# All dog breeds
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

# Set the default encoding for printing to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Define the base URL for Adopt-a-Pet API
BASE_URL = "https://api-staging.adoptapet.com/search/pet_search"

# API Key (replace with your actual key)
API_KEY = "hg4nsv85lppeoqqixy3tnlt3k8lj6o0c"

# Function to search for pets (with raw response print for debugging)
def search_pets_simple(city_or_zip, geo_range, species, start_number=1, end_number=50):
    url = f"{BASE_URL}?key={API_KEY}&v=3&output=json&city_or_zip={city_or_zip}&geo_range={geo_range}&species={species}&start_number={start_number}&end_number={end_number}"
    
    headers = {
        'Accept': 'application/json; charset=UTF8'
    }
    
    # Send GET request to the API
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Successful request, parse the JSON response
        pets_data = response.json()
        
        # Print the entire raw response to check what is being returned
        print("Raw Response Data:")
        print(pets_data)
        
        # Check if pets data is available
        if 'pet' in pets_data:
            return pets_data['pet']  # Return the list of pets found
        else:
            print("No pets found.")
            return []
    else:
        # If request failed, print the error
        print(f"Failed to fetch data: {response.status_code}")
        return []

# Example search for dogs
city_or_zip = "14305"  # Example ZIP code
geo_range = 50  # Search within 50 miles
species = "dog"  # Searching for dogs
start_number = 1  # Starting from pet number 1
end_number = 10  # Limiting the number of results to 10

# Fetch the pets
pets = search_pets_simple(city_or_zip, geo_range, species, start_number, end_number)

if pets:
    # Print the results
    for pet in pets:
        print(f"Name: {pet.get('name', 'N/A')}, Age: {pet.get('age', 'N/A')}, Breed: {pet.get('breed', 'N/A')}, Sex: {pet.get('sex', 'N/A')}")
else:
    print("No pets found.")