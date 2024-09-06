import json
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from tqdm import tqdm
import time

def get_city_name(lat, lon, max_retries=3, timeout=2):
    geolocator = Nominatim(user_agent="my_app", timeout=timeout)
    
    for attempt in range(max_retries):
        try:
            location = geolocator.reverse(f"{lat}, {lon}")
            address = location.raw['address']
            country_code = address.get('country_code', '')
            # print(country_code)
            city = address.get('city', '')
            if not city:
                city = address.get('town', '')
            city_name = city + ", " + country_code
            # print(city_name)
            return city_name or 'Unknown'
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            if attempt == max_retries - 1:
                print(f"Failed to get city name for {lat}, {lon}: {e}")
                return 'Unknown'
            # time.sleep(2)  # Wait for 2 seconds before retrying
        except Exception as e:
            print(f"Unexpected error for {lat}, {lon}: {e}")
            return 'Unknown'



def get_city_center(city_name):
    geolocator = Nominatim(user_agent="my_app")
    try:
        location = geolocator.geocode(city_name, exactly_one=True)
        if location:
            return location.latitude, location.longitude
        return None
    except Exception as e:
        print(f"Error getting center for {city_name}: {e}")
        return None

def plot_geo_locations_on_world_map(json_file):
    # Read the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Create a map centered on the mean of all coordinates
    world_map = folium.Map()
    unique_locations = set()
    # Create a MarkerCluster
    marker_cluster = MarkerCluster().add_to(world_map)

    for entry in tqdm(data, desc="Processing entries", unit="entry"):
        if 'visit' in entry and 'topCandidate' in entry['visit']:
            place_location = entry['visit']['topCandidate'].get('placeLocation', '')

            if place_location.startswith('geo:'):
                lat, lon = place_location[4:].split(',')
                lat, lon = float(lat), float(lon)
                
                city_name = get_city_name(lat, lon)
                if city_name not in unique_locations:
                    unique_locations.add(city_name)
                    city_center = get_city_center(city_name)

                    if city_center:
                        folium.Marker(
                            location=city_center,
                            popup=f"{city_name}",
                            tooltip=city_name
                        ).add_to(marker_cluster)
                    else:
                        print(f"Couldn't find center for {city_name}, using original coordinates")
                        folium.Marker(
                            location=[lat, lon],
                            popup=f"{city_name}",
                            tooltip=city_name
                        ).add_to(marker_cluster)

    # Fit the map to the bounds of all markers
    world_map.fit_bounds(world_map.get_bounds())

    # Save the map as an HTML file
    world_map.save("interactive_world_map2.html")

# Usage
plot_geo_locations_on_world_map('location-history.json')