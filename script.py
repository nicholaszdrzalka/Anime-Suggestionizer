import requests

def fetch_trending_anime(year, season):
    url = 'https://graphql.anilist.co'
    query = '''
    query ($year: Int, $season: MediaSeason) {
        Page(page: 1, perPage: 50) {
            media(season: $season, seasonYear: $year, type: ANIME, sort: TRENDING_DESC) {
                title {
                    romaji
                }
            }
        }
    }
    '''

    variables = {
        'year': year,
        'season': season.upper()
    }
    try:
        response = requests.post(url, json={'query': query, 'variables': variables})
        data = response.json()
        if data and 'data' in data and 'Page' in data['data'] and 'media' in data['data']['Page']:
            return [anime['title']['romaji'] for anime in data['data']['Page']['media']]
        else:
            print("Data is not in the expected format or is missing.")
            return[]
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
