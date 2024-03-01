import tkinter as tk
from tkinter import ttk
import random
from script import fetch_trending_anime

#function to update anime list and suggestion based on the selected season and year
def update_list():
    season = season_combobox.get()
    year = int(year_entry.get())
    anime_list = fetch_trending_anime(year, season)
    listbox.delete(0, tk.END)
    for anime in anime_list:
        listbox.insert(tk.END, anime)
    suggest_random_anime(anime_list)

#function to suggest a random show from list of trending 50 from selected year
def suggest_random_anime(anime_list):
    random_anime = random.choice(anime_list)
    suggestion_label.config(text=f"Suggested Anime: {random_anime}")

#main window
root = tk.Tk()
root.title("Anime Suggester")
style = ttk.Style(root)
style.theme_use('alt')

#season selection
season_label = tk.Label(root, text="Season: ")
season_label.pack()
season_combobox = ttk.Combobox(root, values=["Winter", "Spring", "Summer", "Fall"])
season_combobox.pack()

#year selection
year_label = tk.Label(root, text="Year: ")
year_label.pack()
year_entry = tk.Entry(root)
year_entry.pack()

#button to fetch and display anime
fetch_button = tk.Button(root, text="Fetch Trending Anime", command=update_list)
fetch_button.pack()

#list box to display anime
listbox = tk.Listbox(root, width=50, height=20)
listbox.pack()

#Label for random anime suggestion
suggestion_label = tk.Label(root, text="Suggested show: ")
suggestion_label.pack()

root.mainloop()