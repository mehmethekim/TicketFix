import requests
from bs4 import BeautifulSoup
import pandas as pd
import folium
from urllib.parse import urljoin

# --------------------------------------------
# 1. Define target URL
# --------------------------------------------
BASE_URL = "https://www.edenred.com.tr/"
LIST_URL = "https://www.edenred.com.tr/yerler/ankara/cankaya"

# --------------------------------------------
# 2. Fetch and parse HTML
# --------------------------------------------
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}
response = requests.get(LIST_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# --------------------------------------------
# 3. Extract data blocks
# Each restaurant is typically inside a <div> with class containing 'result-content'
# --------------------------------------------
restaurants = []

for item in soup.find_all("div", class_="result-content"):
    try:
        name = item.find("span", class_="result-title").get_text(strip=True)
    except AttributeError:
        name = None
    try:
        category = item.find("span", class_="result-category").get_text(strip=True)
    except AttributeError:
        category = None
    try:
        address = item.find("span", class_="result-address").get_text(strip=True)
    except AttributeError:
        address = None
    try:
        phone = item.find("span", class_="result-phone").get_text(strip=True)
    except AttributeError:
        phone = None

    restaurants.append({
        "name": name,
        "category": category,
        "address": address,
        "phone": phone
    })

# --------------------------------------------
# 4. Convert to DataFrame
# --------------------------------------------
df = pd.DataFrame(restaurants)
print(df.head())

# --------------------------------------------
# 5. Optional: Clean/filter by tag
# Example: filter all "Kebap/Türk Mutfağı"
# --------------------------------------------
df_filtered = df[df['category'].str.contains("Kebap", na=False)]

# # --------------------------------------------
# # 6. Optional: Geocode (convert address → lat/lon)
# # Uses Nominatim (OpenStreetMap) — rate limited, so cache results for large datasets
# # --------------------------------------------
# from geopy.geocoders import Nominatim
# from time import sleep

# geolocator = Nominatim(user_agent="edenred_scraper")
# coords = []

# for addr in df_filtered['address']:
#     try:
#         loc = geolocator.geocode(addr + ", Ankara, Turkey", timeout=10)
#         if loc:
#             coords.append((loc.latitude, loc.longitude))
#         else:
#             coords.append((None, None))
#     except Exception:
#         coords.append((None, None))
#     sleep(1)  # avoid rate limiting

# df_filtered[['latitude', 'longitude']] = pd.DataFrame(coords, index=df_filtered.index)

# # --------------------------------------------
# # 7. Create interactive map with Folium
# # --------------------------------------------
# m = folium.Map(location=[39.93, 32.85], zoom_start=12)  # Ankara center

# for _, row in df_filtered.dropna(subset=['latitude']).iterrows():
#     popup = f"<b>{row['name']}</b><br>{row['category']}<br>{row['address']}<br>{row['phone']}"
#     folium.Marker(
#         [row['latitude'], row['longitude']],
#         popup=popup,
#         tooltip=row['name']
#     ).add_to(m)

# m.save("edenred_cankaya_map.html")
# print("✅ Map saved to edenred_cankaya_map.html")
