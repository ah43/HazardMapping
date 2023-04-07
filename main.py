import tkinter as tk
from map_utils import create_germany_map

def submit():
    lat = float(lat_entry.get())
    lng = float(lng_entry.get())
    name = name_entry.get()
    create_germany_map(lat, lng, name)
    root.destroy()

# Create a simple tkinter GUI
root = tk.Tk()
root.title("Map Coordinates Input")

tk.Label(root, text="Latitude:").grid(row=0, column=0, sticky="e")
tk.Label(root, text="Longitude:").grid(row=1, column=0, sticky="e")
tk.Label(root, text="Name:").grid(row=2, column=0, sticky="e")

lat_entry = tk.Entry(root)
lng_entry = tk.Entry(root)
name_entry = tk.Entry(root)

lat_entry.grid(row=0, column=1)
lng_entry.grid(row=1, column=1)
name_entry.grid(row=2, column=1)

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=3, columnspan=2)

root.mainloop()
