import requests
import sys

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
