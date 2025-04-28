import requests
import pandas as pd
import folium
import os

# Center coordinates for Hyderabad
lat_center = 17.3850
lon_center = 78.4867
radius_m = 100000  # 100 km radius (in meters)

# Overpass API endpoint
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# Overpass QL query to search for petrol stations
query = f"""
[out:json];
node
  ["amenity"="fuel"]
  (around:{radius_m},{lat_center},{lon_center});
out center;
"""

# Send POST request
response = requests.post(OVERPASS_URL, data={'data': query})
response.raise_for_status()

# Parse JSON response
data = response.json()

# Extract petrol station information
petrol_stations = []
for element in data['elements']:
    station_info = {
        'Name': element.get('tags', {}).get('name', 'Unknown Station'),
        'Latitude': element['lat'],
        'Longitude': element['lon'],
        'Address Info': element.get('tags', {})
    }
    petrol_stations.append(station_info)

# Save to DataFrame
df = pd.DataFrame(petrol_stations)

# Save the petrol stations to a CSV file
# Specify the full path where you want to save the file
output_path = r"C:\Users\Nalamati Yasaswini\Documents\tcs\EV-LOCATOR\hyderabad_petrol_stations_overpass.csv"

# Save the dataframe to the specified file path
df.to_csv(output_path, index=False)

# Print confirmation message
print(f"File saved successfully at: {output_path}")

# Create a map centered around Hyderabad
map_hyderabad = folium.Map(location=[lat_center, lon_center], zoom_start=12)

# Add markers for each petrol station
for idx, row in df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Name']}<br>Latitude: {row['Latitude']}<br>Longitude: {row['Longitude']}",
        icon=folium.Icon(color='blue', icon='cloud')  # Blue icon for petrol stations
    ).add_to(map_hyderabad)

# Save the map as an HTML file
map_hyderabad.save("hyderabad_petrol_stations_map.html")
print("Map saved as hyderabad_petrol_stations_map.html")
