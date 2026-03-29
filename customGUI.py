import customtkinter as ctk
import tkinter as tk
import requests
import webbrowser
import io
import json
import os
from io import BytesIO
from PIL import Image
from datetime import datetime
from CTkListbox import *
from CTkScrollableDropdown import *
from script import fetch_trending_anime
from random import choice

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# list of genres to filter search
genres = [
    "Any",
    "Action",
    "Adventure",
    "Comedy",
    "Drama",
    "Ecchi",
    "Fantasy",
    "Hentai",
    "Horror",
    "Mahou Shoujo",
    "Mecha",
    "Music",
    "Mystery",
    "Psychological",
    "Romance",
    "Sci-Fi",
    "Slice of Life",
    "Sports",
    "Supernatural",
    "Thriller",
]

# --- Persistent favorites storage ---
FAVORITES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "favorites.json")


def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_favorites():
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites_list, f, indent=2)


favorites_list = load_favorites()

# global anime list variable for accessing query information across different functions
global_anime_list = []

# reference to the My List window and its scrollable content frame
my_list_window = None
my_list_scroll_frame = None


# --- Favorites helpers ---

def is_in_favorites(title):
    return any(a["title"] == title for a in favorites_list)


def update_heart_button():
    title = random_title.cget("text")
    if title and title not in ("", "No more anime to suggest.") and is_in_favorites(title):
        heart_button.configure(text="\u2665")  # filled heart
    else:
        heart_button.configure(text="\u2661")  # empty heart


def toggle_favorite():
    title = random_title.cget("text")
    if not title or title == "No more anime to suggest.":
        return

    if is_in_favorites(title):
        favorites_list[:] = [a for a in favorites_list if a["title"] != title]
    else:
        anime = next((a for a in global_anime_list if a["title"] == title), None)
        if anime:
            favorites_list.append({
                "title": anime["title"],
                "coverImage": anime["coverImage"],
                "anilistUrl": anime["anilistUrl"],
                "completed": False,
                "rating": "Not Rated",
            })

    save_favorites()
    update_heart_button()
    refresh_my_list()


# --- My List window ---

def make_rating_handler(idx):
    def handler(value):
        favorites_list[idx]["rating"] = value
        save_favorites()
    return handler


def make_completed_handler(var, idx):
    def handler():
        favorites_list[idx]["completed"] = var.get()
        save_favorites()
    return handler


def make_title_link_handler(url):
    def handler(event=None):
        webbrowser.open(url)
    return handler


def make_remove_handler(title):
    def handler():
        for i, a in enumerate(favorites_list):
            if a["title"] == title:
                del favorites_list[i]
                break
        save_favorites()
        update_heart_button()
        refresh_my_list()
    return handler


def refresh_my_list():
    global my_list_scroll_frame
    if my_list_window is None or not my_list_window.winfo_exists():
        return
    if my_list_scroll_frame is None:
        return

    for widget in my_list_scroll_frame.winfo_children():
        widget.destroy()

    if not favorites_list:
        ctk.CTkLabel(
            my_list_scroll_frame,
            text="No saved anime yet.",
            font=("Bahnschrift", 14),
        ).pack(pady=20)
        return

    rating_options = ["Not Rated"] + [str(i) for i in range(1, 11)]

    for i, anime in enumerate(favorites_list):
        row = ctk.CTkFrame(my_list_scroll_frame)
        row.pack(fill="x", padx=5, pady=3)

        # × remove button — pack right-most first so rating sits beside it
        remove_btn = ctk.CTkButton(
            row,
            text="\u00d7",
            width=30,
            height=30,
            command=make_remove_handler(anime["title"]),
            fg_color="#125645",
            hover_color="#3bcba6",
            font=("Bahnschrift", 16),
        )
        remove_btn.pack(side="right", padx=(4, 8), pady=6)

        # rating dropdown — right-justified, left of remove button
        rating_var = tk.StringVar(value=anime.get("rating", "Not Rated"))
        rating_combo = ctk.CTkOptionMenu(
            row,
            values=rating_options,
            variable=rating_var,
            command=make_rating_handler(i),
            font=("Bahnschrift", 12),
            fg_color="#125645",
            button_color="#125645",
            button_hover_color="#3bcba6",
            width=110,
            height=28,
        )
        rating_combo.pack(side="right", padx=(4, 4), pady=6)

        # watched checkbox — left-most
        completed_var = tk.BooleanVar(value=anime.get("completed", False))
        watched_cb = ctk.CTkCheckBox(
            row,
            text="",
            variable=completed_var,
            command=make_completed_handler(completed_var, i),
            fg_color="#125645",
            hover_color="#3bcba6",
            width=20,
        )
        watched_cb.pack(side="left", padx=(19, 0), pady=6)

        # cover image — clickable link to anilist page
        image_label = ctk.CTkLabel(row, text="")
        image_label.pack(side="left", padx=(30, 0), pady=6)
        try:
            img_data = Image.open(io.BytesIO(requests.get(anime["coverImage"]).content))
            photo = ctk.CTkImage(img_data, size=(40, 55))
            image_label.configure(image=photo, cursor="hand2")
            image_label.image = photo
            image_label.bind("<Button-1>", make_title_link_handler(anime["anilistUrl"]))
        except Exception:
            pass

        # title
        title_label = ctk.CTkLabel(
            row,
            text=anime["title"],
            font=("Bahnschrift", 13),
            anchor="nw",
            wraplength=210,
            justify="left",
        )
        title_label.pack(side="left", padx=(10, 5), pady=6)


def open_my_list():
    global my_list_window, my_list_scroll_frame

    if my_list_window is not None and my_list_window.winfo_exists():
        my_list_window.focus()
        return

    my_list_window = ctk.CTkToplevel(app)
    my_list_window.title("Anime Suggestionizer")
    my_list_window.geometry("660x500")
    my_list_window.resizable(False, True)

    ctk.CTkLabel(
        my_list_window,
        text="My List",
        font=("Bahnschrift", 22),
        text_color="#3bcba6",
    ).pack(pady=(15, 5))

    # column headers — padx mirrors scroll frame (15 left, +14 right for scrollbar)
    header_frame = ctk.CTkFrame(my_list_window, fg_color="transparent")
    header_frame.pack(fill="x", padx=(20, 29), pady=(2, 0))

    # pack right-side headers first to mirror data row packing order
    ctk.CTkLabel(
        header_frame, text="", width=46, font=("Bahnschrift", 11)
    ).pack(side="right")  # spacer for × button
    ctk.CTkLabel(
        header_frame, text="Rating", width=118, font=("Bahnschrift", 11),
        text_color="#888888", anchor="center",
    ).pack(side="right")
    ctk.CTkLabel(
        header_frame, text="Completed", width=20, font=("Bahnschrift", 11),
        text_color="#888888", anchor="center",
    ).pack(side="left", padx=(7, 0))
    ctk.CTkLabel(
        header_frame, text="Anime Title", font=("Bahnschrift", 11),
        text_color="#888888", anchor="w",
    ).pack(side="left", padx=(70, 0))

    ctk.CTkFrame(my_list_window, height=1, fg_color="#333333").pack(
        fill="x", padx=15, pady=(3, 0)
    )

    my_list_scroll_frame = ctk.CTkScrollableFrame(my_list_window)
    my_list_scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    refresh_my_list()


# --- Core app functions ---

def highlight_in_listbox(title):
    for idx in range(listbox.size()):
        if listbox.get(idx) == title:
            listbox.select(idx)
            break


def on_listbox_select(selected_title):
    anime = next((a for a in global_anime_list if a["title"] == selected_title), None)
    if anime is None:
        return
    random_title.configure(text=selected_title)
    display_cover_image(anime["coverImage"], anime["anilistUrl"], cover_image_label)
    update_heart_button()


# function that fetches top 50 trending anime according to user selections from API
def on_submit():
    global global_anime_list
    year = year_combo.get()
    season = season_combo.get()
    genre = genre_combo.get()
    animeFormat = format_combo.get()
    global_anime_list = fetch_trending_anime(year, season, genre, animeFormat)

    # check for error: no results found
    if not global_anime_list:
        error_label.configure(
            text="No results found. Please select different filter options."
        )
        listbox.delete(0, ctk.END)
        # clear suggestion label and cover image in case no results error triggers
        random_title.configure(text="")
        cover_image_label.configure(image="")
        update_heart_button()
        return

    error_label.configure(text="")

    # clear listbox of any items
    listbox.delete(0, ctk.END)
    # loop to fill listbox with anime from script query
    for anime in global_anime_list:
        listbox.insert(ctk.END, anime["title"])

    random_anime = choice(global_anime_list)
    random_title.configure(text=f"{random_anime['title']}")
    display_cover_image(
        random_anime["coverImage"], random_anime["anilistUrl"], cover_image_label
    )
    update_heart_button()
    highlight_in_listbox(random_anime["title"])


# function to allow user to delete selected show from provided top 50 trending anime
def delete_selected_anime():
    global global_anime_list

    selected_indices = listbox.curselection()

    # check if selected_indices is iterable
    if isinstance(selected_indices, int):
        selected_indices = [selected_indices]

    if not selected_indices:
        return

    # get current suggestion before any deletion
    current_suggestion = random_title.cget("text")

    # flag to determine if the current suggestion is being deleted
    suggestion_deleted = False

    for index in reversed(selected_indices):
        item_to_delete = listbox.get(index)
        if item_to_delete == current_suggestion:
            suggestion_deleted = True
        listbox.delete(index)

    # if current suggestion was deleted, generate a new suggestion
    if suggestion_deleted:
        # filter global anime list to only include anime still in the listbox
        updated_anime_list = [listbox.get(idx) for idx in range(listbox.size())]
        available_anime = [
            anime for anime in global_anime_list if anime["title"] in updated_anime_list
        ]

        if available_anime:
            new_anime = choice(available_anime)
            new_title = new_anime["title"]
            new_coverImage_url = new_anime["coverImage"]
            new_anilistUrl = new_anime["anilistUrl"]

            random_title.configure(text=f"{new_title}")
            display_cover_image(new_coverImage_url, new_anilistUrl, cover_image_label)
            highlight_in_listbox(new_title)
        else:
            random_title.configure(text="No more anime to suggest.")
            cover_image_label.configure(image="")

        update_heart_button()


# function to reroll suggested anime
def reroll_suggestion():
    # no results found error handling
    if not global_anime_list:
        error_label.configure(
            text="No results found. Please select different filter options."
        )
        return

    # get current list of shows (with or without deletions)
    listbox_items = [listbox.get(i) for i in range(listbox.size())]

    # filter global_anime_list to only include anime that are still in the listbox
    available_anime = [
        anime for anime in global_anime_list if anime["title"] in listbox_items
    ]

    if available_anime:
        new_anime = choice(available_anime)
        new_title = new_anime["title"]
        new_coverImage_url = new_anime["coverImage"]
        new_anilistUrl = new_anime["anilistUrl"]

        random_title.configure(text=f"{new_title}")
        display_cover_image(new_coverImage_url, new_anilistUrl, cover_image_label)
        highlight_in_listbox(new_title)
    else:
        random_title.configure(text="No more anime to suggest.")
        cover_image_label.configure(image="")

    update_heart_button()


# function to generate a list of years to provide as options in year filter
def generate_year_list(start_year, end_year):
    return [str(year) for year in range(start_year, end_year - 1, -1)]


# function to allow user to go to anime's web page on anilist by clicking on cover image
def on_coverImage_click(event=None, url="https://anilist.co"):
    webbrowser.open(url)


# function to display cover image of suggested anime
def display_cover_image(image_url, anime_url, target_label):
    response = requests.get(image_url)
    image_data = Image.open(io.BytesIO(response.content))
    photo = ctk.CTkImage(image_data, size=(120, 160))
    target_label.configure(image=photo)
    target_label.image = photo

    # unbind any previous anime urls
    target_label.unbind("<Button-1>")

    # define and bind click event handler
    def on_click(event):
        webbrowser.open(anime_url)

    # bind anime url to cover image
    target_label.bind("<Button-1>", on_click)

    # change cursor to pointer when hovering over the cover image
    target_label.configure(cursor="hand2")


# main window
app = ctk.CTk()
app.title("Anime Suggestionizer")
app.geometry("800x820")
app.resizable(False, False)

# frame for filters at top of gui
filters_frame = ctk.CTkFrame(app)
filters_frame.pack(pady=(15, 20), padx=20)

# label for filters frame at top of gui
filters_label = ctk.CTkLabel(
    filters_frame, text="Filters", text_color="#3bcba6", font=("Bahnschrift", 20)
).pack(side="top")

# subframe for year and season filters
year_season_frame = ctk.CTkFrame(filters_frame)
year_season_frame.pack(pady=(5, 5))

# subframe for genre and format filters
genre_format_frame = ctk.CTkFrame(filters_frame)
genre_format_frame.pack(pady=(5, 10), padx=10)

# generate year list for year_combobox filter
start_year = datetime.now().year
end_year = 1971
year_options = ["Any"] + generate_year_list(start_year, end_year)

# year selection
ctk.CTkLabel(year_season_frame, text="Select a Year:", font=("Bahnschrift", 16)).pack(
    side="left", padx=(5, 10)
)
year_combo = ctk.CTkComboBox(year_season_frame, height=30, font=("Bahnschrift", 12))
CTkScrollableDropdown(
    year_combo,
    values=year_options,
    height=300,
    justify="left",
    scrollbar=False,
    autocomplete=True,
)
year_combo.pack(side="left", padx=(0, 10))

# season selection
ctk.CTkLabel(year_season_frame, text="Select Season:", font=("Bahnschrift", 16)).pack(
    side="left", padx=(10, 5)
)
season_combo = ctk.CTkComboBox(year_season_frame, height=30, font=("Bahnschrift", 12))
CTkScrollableDropdown(
    season_combo,
    values=["Any", "Winter", "Spring", "Summer", "Fall"],
    height=200,
    justify="left",
    scrollbar=False,
    autocomplete=True,
)
season_combo.pack(side="left", padx=(0, 5))

# button to fetch and display anime
submit_button = ctk.CTkButton(
    app,
    text="search",
    width=160,
    height=40,
    command=on_submit,
    fg_color="#125645",
    hover_color="#3bcba6",
    font=("Bahnschrift", 14),
)
submit_button.pack(pady=(0, 10))

# label for error message if no results are found in search
error_label = ctk.CTkLabel(app, text="", text_color="red", font=("Bahnschrift", 14))
error_label.pack()

# subtle "My List" button above the listbox, right-aligned
listbox_header = ctk.CTkFrame(app, fg_color="transparent")
listbox_header.pack(fill="x", padx=20, pady=(0, 4))
my_list_button = ctk.CTkButton(
    listbox_header,
    text="My List",
    width=80,
    height=26,
    command=open_my_list,
    fg_color="transparent",
    hover_color="#125645",
    border_width=1,
    border_color="#3bcba6",
    text_color="#3bcba6",
    font=("Bahnschrift", 12),
)
my_list_button.pack(side="right")

# list box to display anime in a frame
frame = ctk.CTkFrame(app)
listbox = CTkListbox(
    frame,
    height=200,
    hover_color="#125645",
    highlight_color="#125645",
    font="Bahnschrift",
    command=on_listbox_select,
)
listbox.pack(side="left", fill="both", expand=True)
frame.pack(fill="x", pady=(0, 5), padx=20)

# label for random anime suggestion text
suggestion_label = ctk.CTkLabel(
    app, text="Suggested Anime:", font=("Bahnschrift", 20), text_color="#3bcba6"
)
suggestion_label.pack()

# label for the random anime suggestion title
random_title = ctk.CTkLabel(
    app, text="", font=("Bahnschrift", 14), text_color="#3bcba6"
)
random_title.pack(pady=(0, 5))

# label for cover image for random anime suggestion
cover_image_label = ctk.CTkLabel(app, text="")
cover_image_label.pack()

# frame for action buttons
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=(15, 0))

# button to delete selected anime from list if already watched
delete_button = ctk.CTkButton(
    button_frame,
    text="delete",
    width=160,
    height=40,
    command=delete_selected_anime,
    fg_color="#125645",
    hover_color="#3bcba6",
    font=("Bahnschrift", 14),
)
delete_button.pack(side="left", padx=(5, 15), pady=(5, 5))

# heart button to save/unsave current suggestion to favorites
heart_button = ctk.CTkButton(
    button_frame,
    text="\u2661",  # empty heart; filled when in favorites
    width=55,
    height=40,
    command=toggle_favorite,
    fg_color="transparent",
    hover_color="#125645",
    border_width=0,
    font=("Bahnschrift", 20),
)
heart_button.pack(side="left", padx=(1, 14), pady=(5, 5))

# button to re-roll suggestion based on current list of shows (before and after any deletion)
reroll_button = ctk.CTkButton(
    button_frame,
    text="re-roll",
    width=160,
    height=40,
    command=reroll_suggestion,
    fg_color="#125645",
    hover_color="#3bcba6",
    font=("Bahnschrift", 14),
)
reroll_button.pack(side="left", padx=(0, 6), pady=(5, 5))

# genre selection
ctk.CTkLabel(genre_format_frame, text="Select Genre:", font=("Bahnschrift", 16)).pack(
    side="left", padx=(5, 10)
)
genre_combo = ctk.CTkComboBox(genre_format_frame, height=30, font=("Bahnschrift", 12))
CTkScrollableDropdown(
    genre_combo,
    values=genres,
    justify="left",
    height=300,
    scrollbar=False,
    autocomplete=True,
)
genre_combo.pack(side="left", padx=(0, 10))

# format selection
ctk.CTkLabel(
    genre_format_frame, text="Select Anime Format:", font=("Bahnschrift", 16)
).pack(side="left", padx=(10, 5))
format_combo = ctk.CTkComboBox(genre_format_frame, height=30, font=("Bahnschrift", 12))
CTkScrollableDropdown(
    format_combo,
    values=["Any", "TV", "MOVIE"],
    justify="left",
    height=150,
    scrollbar=False,
    autocomplete=True,
)
format_combo.pack(side="left", padx=(0, 5))

app.mainloop()
