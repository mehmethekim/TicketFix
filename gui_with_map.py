import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import folium
import webbrowser
import random

# ----------------------------------------------------------
# Load your CSV file
# ----------------------------------------------------------
CSV_PATH = "edenred_restaurants.csv"
df = pd.read_csv(CSV_PATH)

# If dataset has no coordinates, create dummy random ones near Ankara
if "latitude" not in df.columns or "longitude" not in df.columns:
    df["latitude"] = 39.9 + (pd.Series(range(len(df))) * 0.002) % 0.05
    df["longitude"] = 32.85 + (pd.Series(range(len(df))) * 0.002) % 0.05

if "icon_url" in df.columns:
    df = df.drop(columns=["icon_url"])

# ----------------------------------------------------------
# Tkinter setup
# ----------------------------------------------------------
root = tk.Tk()
root.title("Edenred Restaurant Map (Multi-Pin Folium)")
root.geometry("900x550")

# ----------------------------------------------------------
# Functions
# ----------------------------------------------------------
def update_restaurant_list(*args):
    """When a category is selected, update listbox"""
    selected = category_var.get()
    filtered = df[df["category"] == selected]
    restaurant_list.delete(0, tk.END)
    global current_filtered
    current_filtered = filtered.reset_index(drop=True)
    for _, row in current_filtered.iterrows():
        short_addr = row["address"].split(",")[0][:45]
        restaurant_list.insert(tk.END, f"{row['name']} – {short_addr}")
    details_text.set(f"{len(filtered)} restaurants found in this category.")

def show_details(event):
    """Show details for selected restaurant(s)"""
    selections = restaurant_list.curselection()
    if not selections:
        return
    idx = selections[0]
    row = current_filtered.iloc[idx]
    details_text.set(f"🏢 {row['name']}\n📍 {row['address']}\n📞 {row['phone']}")

def open_map():
    """Create a Folium map showing all selected restaurants as pins"""
    selections = restaurant_list.curselection()
    if not selections:
        messagebox.showinfo("No selection", "Select at least one restaurant.")
        return

    selected_df = current_filtered.iloc[list(selections)]

    # Create Folium map centered on selected locations
    m = folium.Map(
        location=[selected_df["latitude"].mean(), selected_df["longitude"].mean()],
        zoom_start=13
    )

    # Add all selected restaurants as pins
    for _, row in selected_df.iterrows():
        popup_html = f"<b>{row['name']}</b><br>{row['address']}<br>{row['phone']}"
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup_html,
            icon=folium.Icon(color="blue", icon="cutlery", prefix="fa")
        ).add_to(m)

    # Save to file and open in browser
    map_path = "selected_restaurants_map.html"
    m.save(map_path)
    webbrowser.open(map_path)

# ----------------------------------------------------------
# GUI Layout
# ----------------------------------------------------------
tk.Label(root, text="Select Category:", font=("Arial", 12, "bold")).pack(pady=5)

category_var = tk.StringVar()
categories = sorted(df["category"].unique())
menu = ttk.Combobox(root, textvariable=category_var, values=categories, state="readonly", width=50)
menu.pack()
menu.bind("<<ComboboxSelected>>", update_restaurant_list)

tk.Label(root, text="Restaurants (Ctrl/Shift to select multiple):",
         font=("Arial", 11, "bold")).pack(pady=5)

restaurant_list = tk.Listbox(root, selectmode=tk.EXTENDED, height=15, width=90)
restaurant_list.pack(pady=5)
restaurant_list.bind("<<ListboxSelect>>", show_details)

details_text = tk.StringVar()
tk.Label(root, textvariable=details_text, justify="left", wraplength=850).pack(pady=10)

tk.Button(root, text="🗺️ Open Folium Map (Multiple Pins)", command=open_map, width=35).pack(pady=5)

root.mainloop()
