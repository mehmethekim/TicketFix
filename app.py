import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# ----------------------------------------------------------
# Load CSV
# ----------------------------------------------------------
CSV_PATH = "edenred_restaurants.csv"
df = pd.read_csv(CSV_PATH)

# Create dummy coordinates if not available
if "latitude" not in df.columns or "longitude" not in df.columns:
    import random
    df["latitude"] = 39.9 + (pd.Series(range(len(df))) * 0.002) % 0.05
    df["longitude"] = 32.85 + (pd.Series(range(len(df))) * 0.002) % 0.05

# Drop URL column if exists
if "icon_url" in df.columns:
    df = df.drop(columns=["icon_url"])

# ----------------------------------------------------------
# Streamlit layout
# ----------------------------------------------------------
st.set_page_config(page_title="Edenred Restaurant Map", layout="wide")

st.title("🍽️ Edenred Restaurant Map Viewer")
st.markdown("Select category and one or more restaurants to view them on the map.")

# Category selector
categories = sorted(df["category"].unique())
selected_category = st.selectbox("Select a category", categories)

# Filter by category
filtered_df = df[df["category"] == selected_category]

# Restaurant multi-selector
selected_restaurants = st.multiselect(
    "Select restaurants (you can choose multiple)",
    options=filtered_df["name"] + " – " + filtered_df["address"].str[:40],
    default=None
)

# Filter actual data
selected_df = pd.DataFrame()
if selected_restaurants:
    names = [r.split(" – ")[0] for r in selected_restaurants]
    selected_df = filtered_df[filtered_df["name"].isin(names)]
else:
    selected_df = filtered_df.head(0)

# ----------------------------------------------------------
# Map generation
# ----------------------------------------------------------
if not selected_df.empty:
    # Center on mean lat/lon
    m = folium.Map(
        location=[selected_df["latitude"].mean(), selected_df["longitude"].mean()],
        zoom_start=13
    )

    # Add pins
    for _, row in selected_df.iterrows():
        popup_html = f"<b>{row['name']}</b><br>{row['address']}<br>{row['phone']}"
        folium.Marker(
            [row["latitude"], row["longitude"]],
            popup=popup_html,
            icon=folium.Icon(color="blue", icon="cutlery", prefix="fa")
        ).add_to(m)

    # Render map
    st_data = st_folium(m, width=1000, height=600)
else:
    st.info("Select one or more restaurants to see them on the map.")

# Optional: display restaurant info
if not selected_df.empty:
    st.subheader("📋 Selected Restaurants")
    st.dataframe(selected_df[["name", "category", "address", "phone"]])
