import customtkinter as ctk
import tkinter as tk
import requests
import webbrowser
import io
from io import BytesIO
from PIL import Image
from datetime import datetime
from CTkListbox import *
from CTkScrollableDropdown import *
from script import fetch_trending_anime
from random import choice
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

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

    #check for error: no results found
    if not global_anime_list:
        error_label.configure(text="No results found. Please select different filter options.")
        listbox.delete(0, ctk.END)
        #clear suggestion label and cover image in case no results error triggers
        random_title.configure(text="")
        cover_image_label.configure(image="")
        return
    
    error_label.configure(text="")

    #clear listbox of any items
    listbox.delete(0, ctk.END)
    #loop to fill listbox with anime from script query
    for anime in global_anime_list:
        listbox.insert(ctk.END, anime['title'])
    
    random_anime = choice(global_anime_list)
    random_title.configure(text=f"{random_anime['title']}")
    display_cover_image(random_anime['coverImage'], random_anime['anilistUrl'], cover_image_label)

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
    current_suggestion = random_title.cget("text")

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
            new_anilistUrl = new_anime['anilistUrl']

            random_title.configure(text=f"{new_title}")
            display_cover_image(new_coverImage_url, new_anilistUrl, cover_image_label)
        else:
            random_title.configure(text="No more anime to suggest.")
            cover_image_label.configure(image="")

#function to reroll suggested anime
def reroll_suggestion():
    #no results found error handling
    if not global_anime_list:
        error_label.configure(text="No results found. Please select different filter options.")
        return

    #get current list of shows (with or without deletions)
    listbox_items = [listbox.get(i) for i in range(listbox.size())]
    
    #filter global_anime_list to only include anime that are still in the listbox
    available_anime = [anime for anime in global_anime_list if anime['title'] in listbox_items]

    if available_anime:
        new_anime = choice(available_anime)
        new_title = new_anime['title']
        new_coverImage_url = new_anime['coverImage']
        new_anilistUrl = new_anime['anilistUrl']

        random_title.configure(text=f"{new_title}")
        display_cover_image(new_coverImage_url, new_anilistUrl, cover_image_label)
    else:
        random_title.configure(text="No more anime to suggest.")
        cover_image_label.configure(image="")

#function to generate a list of years to provide as options in year filter
def generate_year_list(start_year, end_year):
    return [str(year) for year in range(start_year, end_year - 1, -1)]

#function to allow user to go to anime's web page on anilist by clicking on cover image
def on_coverImage_click(event=None, url="https://anilist.co"):
    webbrowser.open(url)

#function to display cover image of suggested anime
def display_cover_image(image_url, anime_url, target_label):
    response = requests.get(image_url)
    image_data = Image.open(io.BytesIO(response.content))
    photo = ctk.CTkImage(image_data, size=(120, 160))
    target_label.configure(image=photo)
    target_label.image = photo

    #unbind any previous anime urls
    target_label.unbind("<Button-1>")

    #define and bind click event handler
    def on_click(event):
        webbrowser.open(anime_url)

    #bind anime url to cover image
    target_label.bind("<Button-1>", on_click)

    #change cursor to pointer when hovering over the cover image
    target_label.configure(cursor="hand2")

#main window
app = ctk.CTk()
app.title("Anime Suggestionizer")
app.geometry("800x800")
app.resizable(False, False)

#frame for filters at top of gui
filters_frame = ctk.CTkFrame(app)
filters_frame.pack(pady=(15, 20), padx=20)

#label for filters frame at top of gui
filters_label = ctk.CTkLabel(filters_frame, text="Filters", text_color="#3bcba6", font=("Bahnschrift", 20)).pack(side="top")

#subframe for year and season filters
year_season_frame = ctk.CTkFrame(filters_frame)
year_season_frame.pack(pady=(5, 5))

#subframe for genre and format filters
genre_format_frame = ctk.CTkFrame(filters_frame)
genre_format_frame.pack(pady=(5, 10), padx=10)

#generate year list for year_combobox filter
start_year = datetime.now().year
end_year = 1971
year_options = ["Any"] + generate_year_list(start_year, end_year)

#year selection
ctk.CTkLabel(year_season_frame, text="Select a Year:", font=("Bahnschrift", 16)).pack(side="left", padx=(5, 10))
year_combo = ctk.CTkComboBox(year_season_frame, height=30, font=("Bahnschrift", 12))
CTkScrollableDropdown(year_combo, values=year_options, height=300, justify="left", scrollbar=False, autocomplete=True)
year_combo.pack(side="left", padx=(0, 10))

#season selection
ctk.CTkLabel(year_season_frame, text="Select Season:", font=("Bahnschrift", 16)).pack(side="left", padx=(10, 5))
season_combo = ctk.CTkComboBox(year_season_frame, height=30, font=("Bahnschrift", 12))
CTkScrollableDropdown(season_combo, values=["Any", "Winter", "Spring", "Summer", "Fall"], height=200, justify="left", scrollbar=False, autocomplete=True)
season_combo.pack(side="left", padx=(0, 5))

#button to fetch and display anime
submit_button = ctk.CTkButton(app, text="search", width=160, height=40, command=on_submit, fg_color="#125645", hover_color="#3bcba6", font=("Bahnschrift", 14))
submit_button.pack(pady=(0, 10))

#label for error message if no results are found in search
error_label = ctk.CTkLabel(app, text="", text_color="red", font=("Bahnschrift", 14))
error_label.pack()

#list box to display anime in a frame
frame = ctk.CTkFrame(app)
listbox = CTkListbox(frame, height=200, hover_color="#125645", highlight_color="#125645", font="Bahnschrift")
listbox.pack(side="left", fill="both", expand=True)
frame.pack(fill="x", pady=(0, 5), padx=20)

#label for random anime suggestion text
suggestion_label = ctk.CTkLabel(app, text="Suggested Anime:", font=("Bahnschrift", 20), text_color="#3bcba6")
suggestion_label.pack()

#label for the random anime suggestion title
random_title = ctk.CTkLabel(app, text="", font=("Bahnschrift", 14), text_color="#3bcba6")
random_title.pack(pady=(0, 5))

#label for cover image for random anime suggestion
cover_image_label = ctk.CTkLabel(app, text="")
cover_image_label.pack()

#frame for delete and reroll buttons
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=(20, 0))

#button to delete selected anime from list if already watched
delete_button = ctk.CTkButton(button_frame, text="delete", width=160, height=40, command=delete_selected_anime, fg_color="#125645", hover_color="#3bcba6", font=("Bahnschrift", 14))
delete_button.pack(side="left", padx=(5, 20), pady=(5,5))

#button to re-roll suggestion based on current list of shows (before and after any deletion)
reroll_button = ctk.CTkButton(button_frame, text="re-roll", width=160, height=40, command=reroll_suggestion, fg_color="#125645", hover_color="#3bcba6", font=("Bahnschrift", 14))
reroll_button.pack(side="left", padx=(0, 5), pady=(5,5))

#genre selection
ctk.CTkLabel(genre_format_frame, text="Select Genre:", font=("Bahnschrift", 16)).pack(side="left", padx=(5, 10))
genre_combo = ctk.CTkComboBox(genre_format_frame, height=30, font=("Bahnschrift", 12))
CTkScrollableDropdown(genre_combo, values=genres, justify="left", height=300, scrollbar=False, autocomplete=True)
genre_combo.pack(side="left", padx=(0, 10))

#format selection
ctk.CTkLabel(genre_format_frame, text="Select Anime Format:", font=("Bahnschrift", 16)).pack(side="left", padx=(10, 5))
format_combo = ctk.CTkComboBox(genre_format_frame, height=30, font=("Bahnschrift", 12))
CTkScrollableDropdown(format_combo, values=["Any", "TV", "MOVIE"], justify="left", height=150, scrollbar=False, autocomplete=True)
format_combo.pack(side="left", padx=(0, 5))

app.mainloop()