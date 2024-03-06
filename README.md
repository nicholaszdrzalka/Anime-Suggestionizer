
# Anime Suggestionizer

The Anime Suggestionizer is a Python-based application designed to connect anime enthusiasts with the top trending anime according to their preferences. Utilizing a custom-built GUI created with customtkinter, the app offers a set of optional filters that users can apply to refine their search. Upon selection, the app queries AniList's API to fetch and display a list of trending anime that match the specified filters.

In addition to listing the results, the app features a unique component that suggests a random anime complete with its title and a clickable cover image that redirects to the anime's detailed page on AniList.co. Users have the flexibility to reroll the suggestion, delete titles they are not interested in, and initiate new searches with different filters. The app is designed to enhance user experience with thoughtful additions like error messaging for no-result queries and notifications when the suggestion pool is exhausted.

#### Although this app calls on AniList's API to fetch anime data from their database, it is in no way affiliated with the website. This is a personal project I developed to solve an occasional issue I deal with. Anime Suggestionizer can be considered an UNOFFICIAL randomized anime suggestion app for AniList.
## Installation (Download or Clone)
### Downloading the app
#### If you decide to download this app's executable, please be aware of the following:

- Your browser may give you a warning about the file being potential malware.
- When you run the app for the first time after downloading it, you may receive another warning from your anti-virus/windows about the file being potential malware.

To download this app's executable and use immediately, click here: 
#### [Download Anime Suggestionizer](https://github.com/nicholaszdrzalka/anime-script/releases/tag/v1.0.0)

#### The app is completely safe to download and use. Every line of code is transparently shown through the files in my repository. If you feel more comfortable cloning the repository and running the app locally, please reference the instructions below.

### Cloning the repository
#### To run the Anime Suggestionizer on your system, follow these simple steps:
#### Prerequisites
- Python 3.6 or higher
- pip for installing dependencies

#### Setup
1. Clone the repository to your local machine:

        git clone https://github.com/nicholaszdrzalka/anime-script.git

2. Navigate to the project directory:

        cd anime-script

3. Install the required dependencies:

        pip install -r requirements.txt

4. Running the Application
With the dependencies installed, you can run the application using:

    python customGUI.py
## Features

- Filter Selection: Choose from a variety of filters to tailor the search according to your preferences.
- Trending Anime List: View a dynamically generated list of trending anime based on the selected filters.
- Random Anime Suggestion: Get a random anime suggestion with each search, complete with a title and clickable cover image for more details.
- Interactive List: Delete seen or unwanted anime titles from the list and reroll suggestions as desired.
- Error Handling: Receive notifications for no-result queries and when there are no more suggestions available.
- Single File Executable: For ease of access, the project is packaged into a single file executable using PyInstaller.


## Screenshots

#### Main Screen
![anime_main](https://github.com/nicholaszdrzalka/anime-script/assets/71566683/e1dce38a-3eaa-4149-87f3-4f77f0162b49)

#### Screen after searching
![anime_searched](https://github.com/nicholaszdrzalka/anime-script/assets/71566683/2a9f8913-1a0d-4acc-aacc-93355426bfce)

#### Screen after deleting all titles
![anime_nomore](https://github.com/nicholaszdrzalka/anime-script/assets/71566683/c93000a4-2cf5-4b83-b0bf-71e88b20fe9b)

#### Screen with Error
![anime_error](https://github.com/nicholaszdrzalka/anime-script/assets/71566683/c8349def-8a21-4ad1-acc2-1641a4777e0a)


## Acknowledgements

 - [Custom Tkinter](https://customtkinter.tomschimansky.com/)
 - [Anilist's API GraphQL](https://github.com/AniList/ApiV2-GraphQL-Docs)
 - [Akascape's CTkListbox](https://github.com/Akascape/CTkListbox)
 - [Akascape's CTkScrollableDropdown](https://github.com/Akascape/CTkScrollableDropdown)
