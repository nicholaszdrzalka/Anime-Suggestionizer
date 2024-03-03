import requests
import json

def fetch_anilist_genres():
    url = 'https://graphql.anilist.co'
    query = '''
    {
      GenreCollection
    }
    '''
    response = requests.post(url, json={'query': query})
    genres = response.json().get("data", {}).get("GenreCollection", [])
    return genres

genres = fetch_anilist_genres()
print("AniList Genres:", genres)