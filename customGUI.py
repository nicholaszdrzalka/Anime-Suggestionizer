import customtkinter as ctk
import tkinter as tk
import requests
import io
from io import BytesIO
from PIL import Image, ImageTk
from datetime import datetime
from CTkListbox import *
from script import fetch_trending_anime
from random import choice
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

#list of genres to filter search
genres = ['Any', 'Action', 'Adventure', 'Comedy', 'Drama', 'Ecchi', 'Fantasy', 'Hentai', 'Horror', 'Mahou Shoujo', 'Mecha', 'Music', 'Mystery', 'Psychological', 'Romance', 'Sci-Fi', 'Slice of Life', 'Sports', 'Supernatural', 'Thriller']

#global anime list variable for accessing query information across different functions
global_anime_list = []

#function that fetches top 50 trending anime according to user selections from API
def on_submit():
    global global_anime_list
    year = year_combo.get()
    season = season_combo.get()
    genre = genre_combo.get()
    animeFormat = format_combo.get()
    global_anime_list = fetch_trending_anime(year, season, genre, animeFormat)

    #clear listbox of any items
    listbox.delete(0, ctk.END)
    #loop to fill listbox with anime from script query
    for anime in global_anime_list:
        listbox.insert(ctk.END, anime['title'])
    
    random_anime = choice(global_anime_list)
    suggestion_label.configure(text=f"Suggested anime: {random_anime['title']}")
    display_cover_image(random_anime['coverImage'], cover_image_label)

#function to allow user to delete selected show from provided top 50 trending anime
def delete_selected_anime():
    global global_anime_list

    selected_indices = listbox.curselection()

    #check if selected_indices is iterable
    if isinstance(selected_indices, int):
        selected_indices = [selected_indices]

    if not selected_indices:
        return
    
    #get current suggestion before any deletion
    current_suggestion = suggestion_label.cget("text").replace("Suggested anime: ", "")

    #flag to determine if the current suggestion is being deleted
    suggestion_deleted = False

    for index in reversed(selected_indices):
        item_to_delete = listbox.get(index)
        if item_to_delete == current_suggestion:
            suggestion_deleted = True
        listbox.delete(index)

    #if current suggestion was deleted, generate a new suggestion
    if suggestion_deleted:
        #filter global anime list to only include anime still in the listbox
        updated_anime_list = [listbox.get(idx) for idx in range(listbox.size())]
        available_anime = [anime for anime in global_anime_list if anime['title'] in updated_anime_list]

        if available_anime:
            new_anime = choice(available_anime)
            new_title = new_anime['title']
            new_coverImage_url = new_anime['coverImage']

            suggestion_label.configure(text=f"Suggested anime: {new_title}")
            display_cover_image(new_coverImage_url, cover_image_label)
        else:
            suggestion_label.configure(text="No more anime to suggest.")
            cover_image_label.configure(text="")

#function to reroll suggested anime
def reroll_suggestion():
    #get current list of shows (with or without deletions)
    listbox_items = [listbox.get(i) for i in range(listbox.size())]
    
    #filter global_anime_list to only include anime that are still in the listbox
    available_anime = [anime for anime in global_anime_list if anime['title'] in listbox_items]

    if available_anime:
        new_anime = choice(available_anime)
        new_title = new_anime['title']
        new_coverImage_url = new_anime['coverImage']

        suggestion_label.configure(text=f"Suggested anime: {new_title}")
        display_cover_image(new_coverImage_url, cover_image_label)
    else:
        suggestion_label.configure(text="No more anime to suggest.")
        cover_image_label.configure(text="")

#function to generate a list of years to provide as options in year filter
def generate_year_list(start_year, end_year):
    return [str(year) for year in range(start_year, end_year + 1)]

#function to display cover image of suggested anime
def display_cover_image(image_url, target_label):
    response = requests.get(image_url)
    image_data = Image.open(io.BytesIO(response.content))
    photo = ctk.CTkImage(image_data, size=(120, 160))
    target_label.configure(image=photo)
    target_label.image = photo

#main window
app = ctk.CTk()
app.title("Anime Suggestionizer")
app.geometry("600x700")
app.resizable(False, False)

#frame for filters at top of gui
filters_frame = ctk.CTkFrame(app)
filters_frame.pack(pady=(15, 10), padx=20, fill="x")

#label for filters frame at top of gui
filters_label = ctk.CTkLabel(filters_frame, text="Filters", text_color="#3bcba6", font=("default_font", 16)).pack(side="top")

#subframe for year and season filters
year_season_frame = ctk.CTkFrame(filters_frame)
year_season_frame.pack(pady=(0, 5))

#subframe for genre and format filters
genre_format_frame = ctk.CTkFrame(filters_frame)
genre_format_frame.pack(fill="x", pady=(5, 10), padx=10)

#generate year list for year_combobox filter
start_year = 1971
end_year = datetime.now().year
year_options = ["Any"] + generate_year_list(start_year, end_year)

#year selection
ctk.CTkLabel(year_season_frame, text="Select a Year:").pack(side="left", padx=(0, 10))
year_combo = ctk.CTkComboBox(year_season_frame, values=year_options, height=20)
year_combo.pack(side="left")

#season selection
ctk.CTkLabel(year_season_frame, text="Select Season:").pack(side="left", padx=(20, 10))
season_combo = ctk.CTkComboBox(year_season_frame, values=["Any", "Winter", "Spring", "Summer", "Fall"], height=20)
season_combo.pack(side="left")

#button to fetch and display anime
submit_button = ctk.CTkButton(app, text="search", command=on_submit, fg_color="#125645", hover_color="#3bcba6")
submit_button.pack()

#list box to display anime in a frame
frame = ctk.CTkFrame(app)
listbox = CTkListbox(frame, width=50, height=200, hover_color="#125645", highlight_color="#125645")
listbox.pack(side="left", fill="both", expand=True)
frame.pack(fill="x", pady=(10, 5), padx=20)

#label for random anime suggestion
suggestion_label = ctk.CTkLabel(app, text="Suggested Anime:", font=("default_font", 16), text_color="#3bcba6")
suggestion_label.pack(pady=(0, 5))

#label for cover image for random anime suggestion
cover_image_label = ctk.CTkLabel(app, text="")
cover_image_label.pack()

#frame for delete and reroll buttons
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

#button to delete selected anime from list if already watched
delete_button = ctk.CTkButton(button_frame, text="delete", command=delete_selected_anime, fg_color="#125645", hover_color="#3bcba6")
delete_button.pack(side="left", padx=(5, 20), pady=(5,5))

#button to re-roll suggestion based on current list of shows (before and after any deletion)
reroll_button = ctk.CTkButton(button_frame, text="re-roll", command=reroll_suggestion, fg_color="#125645", hover_color="#3bcba6")
reroll_button.pack(side="left", padx=(0, 5), pady=(5,5))

#combo box for genre selection as search filter
ctk.CTkLabel(genre_format_frame, text="Select Genre:").pack(side="left", padx=(5, 10))
genre_combo = ctk.CTkComboBox(genre_format_frame, values=genres, height=20)
genre_combo.pack(side="left", padx=(0, 10))

#combo box for format selection as search filter
ctk.CTkLabel(genre_format_frame, text="Select Anime Format:").pack(side="left", padx=(10, 5))
format_combo = ctk.CTkComboBox(genre_format_frame, values=["Any", "TV", "MOVIE"], height=20)
format_combo.pack(side="left")

app.mainloop()