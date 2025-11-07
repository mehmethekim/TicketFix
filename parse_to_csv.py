from bs4 import BeautifulSoup
import pandas as pd

with open("network_data.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
entries = soup.find_all("a", class_="map-sidebar-result")

data = []
for entry in entries:
    title = entry.find("span", class_="result-title")
    category = entry.find("span", class_="result-category")
    address = entry.find("span", class_="result-address")
    phone = entry.find("span", class_="result-phone")
    icon_style = entry.find("span", class_="result-left")["style"]

    # Extract image URL from style="background-image:url(...);"
    icon_url = None
    if "url(" in icon_style:
        icon_url = icon_style.split("url(")[1].split(")")[0]

    data.append({
        "name": title.get_text(strip=True) if title else "",
        "category": category.get_text(strip=True) if category else "",
        "address": address.get_text(strip=True) if address else "",
        "phone": phone.get_text(strip=True) if phone else "",
        "icon_url": icon_url
    })

# --------------------------------------------------------------------
# 3️⃣ Save to CSV
# --------------------------------------------------------------------
df = pd.DataFrame(data)
df.to_csv("edenred_restaurants.csv", index=False, encoding="utf-8-sig")

print("✅ Parsed", len(df), "entries.")
print(df)