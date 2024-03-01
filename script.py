import requests

def fetch_trending_anime(season, year):
    query = '''
    query ($season: MediaSeason, $seasonYear: Int) {
        Page(page: 1, perPage: 50) {
            media(season: $season, seasonYear: $seasonYear, type: ANIME, sort: POPULARITY_DESC) {
                title {
                    romaji
                }
                description
                coverImage {
                    large
                }
            }
        }
    }
    '''

    variables = {
        'season': season.upper(),
        'seasonYear': year
    }

    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()
    return data['data']['Page']['media']