import tkinter as tk
from tkinter import ttk
import pandas as pd

# ----------------------------------------------------------------
# Load CSV
# ----------------------------------------------------------------
CSV_PATH = "edenred_restaurants.csv"
df = pd.read_csv(CSV_PATH)

# Drop URL (optional)
if "icon_url" in df.columns:
    df = df.drop(columns=["icon_url"])

# ----------------------------------------------------------------
# Main window
# ----------------------------------------------------------------
root = tk.Tk()
root.title("Edenred Restaurant Browser")
root.geometry("800x500")

# ----------------------------------------------------------------
# Functions
# ----------------------------------------------------------------
def update_restaurant_list(*args):
    """When category is selected, update the listbox"""
    selected_category = category_var.get()
    filtered = df[df["category"] == selected_category]
    restaurant_list.delete(0, tk.END)

    # Store filtered dataframe globally for lookup
    global current_filtered
    current_filtered = filtered.reset_index(drop=True)

    for _, row in filtered.iterrows():
        # Show shortened address for clarity
        short_addr = row["address"].split(",")[0][:40]
        display_name = f"{row['name']} – {short_addr}"
        restaurant_list.insert(tk.END, display_name)

def show_details(event):
    """Show full details when a restaurant is selected"""
    try:
        index = restaurant_list.curselection()[0]
    except IndexError:
        return
    row = current_filtered.iloc[index]

    info = (
        f"🏢 {row['name']}\n\n"
        f"📍 {row['address']}\n"
        f"📞 {row['phone']}"
    )
    details_text.set(info)

# ----------------------------------------------------------------
# GUI Layout
# ----------------------------------------------------------------
# Category selector
tk.Label(root, text="Select Category:", font=("Arial", 12, "bold")).pack(pady=5)
category_var = tk.StringVar()
categories = sorted(df["category"].unique())
category_menu = ttk.Combobox(root, textvariable=category_var, values=categories, state="readonly", width=50)
category_menu.pack()
category_menu.bind("<<ComboboxSelected>>", update_restaurant_list)

# List of restaurants
tk.Label(root, text="Restaurants:", font=("Arial", 12, "bold")).pack(pady=5)
frame = tk.Frame(root)
frame.pack(pady=5, fill="both", expand=True)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

restaurant_list = tk.Listbox(frame, height=12, width=80, yscrollcommand=scrollbar.set)
restaurant_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
restaurant_list.bind("<<ListboxSelect>>", show_details)

scrollbar.config(command=restaurant_list.yview)

# Details area
details_text = tk.StringVar()
details_label = tk.Label(root, textvariable=details_text, font=("Arial", 11), justify="left", wraplength=750, anchor="w")
details_label.pack(pady=10, fill="both")

# ----------------------------------------------------------------
# Start the GUI
# ----------------------------------------------------------------
root.mainloop()
