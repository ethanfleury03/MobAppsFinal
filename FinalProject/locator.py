# This file will make function used to direct users to location
'''
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_distance(user_address, closest_location):
    geolocater = Nominatim(user_agent="my_app") 

    homeAddress = geolocater.geocode(user_address)
    adoption_center = geolocater.geocode(closest_location)

    if homeAddress and adoption_center:
        distance = geodesic(
            (homeAddress.latitude, homeAddress.longitude),
            (adoption_center.latitude, adoption_center.longitude)
        ).miles
        return f"{distance:.2f} miles"



    else:
        return "Failure to load address'"   

a = "2942 Mckoon Ave, Niagara Falls, NY 14305"
b = "2100 Lockport Rd, Niagara Falls, NY 14304"

distance = get_distance(a, b)
print(distance)

'''
import requests

def geocode_address(api_key, address):
    base_url = "https://api.openrouteservice.org/geocode/search"
    params = {
        "api_key": api_key,
        "text": address
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['features']:
            return data['features'][0]['geometry']['coordinates']
    return None


def get_driving_distance(start_address, end_address):
    # Base URL for OpenRouteService API
    base_url = "https://api.openrouteservice.org/v2/directions/driving-car"
    api_key = "5b3ce3597851110001cf62484c86d098c7ea47449985215309168b0d" 

    # Geocode the addresses
    start_coords = geocode_address(api_key, start_address)
    end_coords = geocode_address(api_key, end_address)

    if not start_coords or not end_coords:
        return "Unable to geocode one or both addresses."

    # Parameters for the routing request
    params = {
        "api_key": api_key,
        "start": f"{start_coords[0]},{start_coords[1]}",
        "end": f"{end_coords[0]},{end_coords[1]}"
    }

    # Make the request
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Extract distance in meters and convert to miles
        distance_miles = data['features'][0]['properties']['segments'][0]['distance'] / 1609.34
        return f"{distance_miles:.2f} miles"
    else:
        return f"Error: {response.status_code}, {response.text}"


# # Example usage
# start_address = "2942 Mckoon Ave, Niagara Falls, NY 14305"
# end_address = "8 chenango st, Oxford, NY 13830"

# distance = get_driving_distance(start_address, end_address)
# print(f"The driving distance between the two addresses is: {distance}")