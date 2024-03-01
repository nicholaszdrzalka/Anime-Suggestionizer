import customtkinter as ctk
import tkinter as tk
from tkinter import Listbox, Scrollbar, VERTICAL
from script import fetch_trending_anime
from random import choice
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def on_submit():
    year = int(year_entry.get())
    season = season_combo.get()
    anime_list = fetch_trending_anime(year, season)
    for item in listbox.get(0, ctk.END):
        listbox.delete(0)
    for anime in anime_list:
        listbox.insert(ctk.END, anime)
    suggestion_label.configure(text=f"Suggested show: {choice(anime_list)}")

def delete_selected_show():
    selected_indices = listbox.curselection()
    if not selected_indices:
        return
    
    for index in selected_indices:
        listbox.delete(index)
    
    updated_anime_list = listbox.get(0, ctk.END)

    if updated_anime_list:
        new_suggestion = choice(updated_anime_list)
        suggestion_label.configure(text=f"Suggested show: {new_suggestion}")
    else:
        suggestion_label.configure(text="No more anime to suggest.")

def reroll_suggestion():
    #get current list of shows (with or without deletions)
    listbox_items = listbox.get(0, ctk.END)

    if listbox_items:
        new_suggestion = choice(listbox_items)
        suggestion_label.configure(text=f"Suggested show: {new_suggestion}")
    else:
        suggestion_label.configure(text="No more anime to suggest.")

#main window
app = ctk.CTk()
app.title("Anime Suggestionizer")
app.geometry("300x500")

#year selection
ctk.CTkLabel(app, text="Enter a Year:").pack(pady=10)
year_entry = ctk.CTkEntry(app, placeholder_text="1940 - 2024")
year_entry.pack()

#season selection
ctk.CTkLabel(app, text="Select Season:").pack(pady=10)
season_combo = ctk.CTkComboBox(app, values=["Winter", "Spring", "Summer", "Fall"])
season_combo.pack()

#button to fetch and display anime
submit_button = ctk.CTkButton(app, text="search", command=on_submit)
submit_button.pack(pady=20)

#list box to display anime in tkinter with scrollbar in a frame
frame = tk.Frame(app)
scrollbar = Scrollbar(frame, orient=VERTICAL)
listbox = Listbox(frame, yscrollcommand=scrollbar.set, width=50, height=10)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side="right", fill="y")
listbox.pack(side="left", fill="both", expand=True)
frame.pack(padx=10, pady=10)

#label for random anime suggestion
suggestion_label = ctk.CTkLabel(app, text="Suggested Show:")
suggestion_label.pack(pady=10)

#frame for delete and reroll buttons
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=20)

#button to delete selected show from list if already watched
delete_button = ctk.CTkButton(button_frame, text="delete", command=delete_selected_show)
delete_button.pack(side="left", padx=10)

#button to re-roll suggestion based on current list of shows (before and after any deletion)
reroll_button = ctk.CTkButton(button_frame, text="re-roll", command=reroll_suggestion)
reroll_button.pack(side="left", padx=10)

app.mainloop()