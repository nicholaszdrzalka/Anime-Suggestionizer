import customtkinter as ctk
import tkinter as tk
from tkinter import Listbox, Scrollbar, VERTICAL
from script import fetch_trending_anime
from random import choice
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

#list of genres to filter search
genres = ['Any', 'Action', 'Adventure', 'Comedy', 'Drama', 'Ecchi', 'Fantasy', 'Hentai', 'Horror', 'Mahou Shoujo', 'Mecha', 'Music', 'Mystery', 'Psychological', 'Romance', 'Sci-Fi', 'Slice of Life', 'Sports', 'Supernatural', 'Thriller']

#function that fetches top 50 trending anime according to user selections from API
def on_submit():
    year = int(year_entry.get())
    season = season_combo.get()
    genre = genre_combo.get()
    # rating = rating_slider.get()
    animeFormat = format_combo.get()
    anime_list = fetch_trending_anime(year, season, genre, animeFormat)
    for item in listbox.get(0, ctk.END):
        listbox.delete(0)
    for anime in anime_list:
        listbox.insert(ctk.END, anime)
    suggestion_label.configure(text=f"Suggested show: {choice(anime_list)}")

#function to allow user to delete selected show from provided top 50 trending anime
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

#function to reroll suggested anime
def reroll_suggestion():
    #get current list of shows (with or without deletions)
    listbox_items = listbox.get(0, ctk.END)

    if listbox_items:
        new_suggestion = choice(listbox_items)
        suggestion_label.configure(text=f"Suggested show: {new_suggestion}")
    else:
        suggestion_label.configure(text="No more anime to suggest.")

#function to update the label of the format value filter
        #VOID
# def rating_value_label(value):
#     rating_value = "Any" if int(value) == 0 else int(value)
#     rating_value_label.configure(text=f"format: {rating_value}")

#main window
app = ctk.CTk()
app.title("Anime Suggestionizer")
app.geometry("600x500")

#frame for filters at top of gui
filters_frame = ctk.CTkFrame(app)
filters_frame.pack(pady=15, padx=20, fill="x")

#label for filters frame at top of gui
filters_label = ctk.CTkLabel(filters_frame, text="Filters", text_color="#3bcba6", font=("default_font", 16)).pack(side="top")

#subframe for year and season filters
year_season_frame = ctk.CTkFrame(filters_frame)
year_season_frame.pack(pady=(0, 5))

#subframe for genre and format filters
genre_format_frame = ctk.CTkFrame(filters_frame)
genre_format_frame.pack(fill="x", pady=(5, 0), padx=10)

#year selection
ctk.CTkLabel(year_season_frame, text="Enter a Year:").pack(side="left", padx=(0, 10))
year_entry = ctk.CTkEntry(year_season_frame, placeholder_text="1971 - 2024")
year_entry.pack(side="left")

#season selection
ctk.CTkLabel(year_season_frame, text="Select Season:").pack(side="left", padx=(20, 10))
season_combo = ctk.CTkComboBox(year_season_frame, values=["Winter", "Spring", "Summer", "Fall"])
season_combo.pack(side="left")

#button to fetch and display anime
submit_button = ctk.CTkButton(app, text="search", command=on_submit, fg_color="#125645", hover_color="#3bcba6")
submit_button.pack()

#list box to display anime in tkinter with scrollbar in a frame
frame = tk.Frame(app)
scrollbar = Scrollbar(frame, orient=VERTICAL)
listbox = Listbox(frame, yscrollcommand=scrollbar.set, width=50, height=10)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side="right", fill="y")
listbox.pack(side="left", fill="both", expand=True)
frame.pack(fill="x", pady=10, padx=20)

#label for random anime suggestion
suggestion_label = ctk.CTkLabel(app, text="Suggested Show:", font=("default_font", 14))
suggestion_label.pack(pady=5)

#frame for delete and reroll buttons
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

#button to delete selected show from list if already watched
delete_button = ctk.CTkButton(button_frame, text="delete", command=delete_selected_show, fg_color="#125645", hover_color="#3bcba6")
delete_button.pack(side="left", padx=(0, 20))

#button to re-roll suggestion based on current list of shows (before and after any deletion)
reroll_button = ctk.CTkButton(button_frame, text="re-roll", command=reroll_suggestion, fg_color="#125645", hover_color="#3bcba6")
reroll_button.pack(side="left")

#combo box for genre selection as search filter
ctk.CTkLabel(genre_format_frame, text="Select Genre:").pack(side="left", padx=(5, 10))
genre_combo = ctk.CTkComboBox(genre_format_frame, values=genres)
genre_combo.pack(side="left", padx=(0, 10))

#combo box for format selection as search filter
ctk.CTkLabel(genre_format_frame, text="Select Anime Format:").pack(side="left", padx=(10, 5))
format_combo = ctk.CTkComboBox(genre_format_frame, values=["TV Show", "Movie"])
format_combo.pack(side="left", padx= 5)

#slider for rating selection as search filter
#VOID
# ctk.CTkLabel(genre_format_frame, text="Minimum format:").pack(side="left", padx=(10, 5))
# rating_slider = ctk.CTkSlider(genre_format_frame, from_=0, to=10, number_of_steps=10)
# rating_slider.set(0) #start at "any" format
# rating_slider.pack(side="left", padx=5)

#format value label for slider
#VOID
# rating_value_label = ctk.CTkLabel(filters_frame, text="format: Any")
# rating_slider.configure(command=rating_value_label)
# rating_value_label.pack(side="right", padx=(0, 100), pady=(0, 5))

app.mainloop()