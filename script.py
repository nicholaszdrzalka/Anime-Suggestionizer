import requests

def fetch_trending_anime(year, season, genre, animeFormat):
    url = 'https://graphql.anilist.co'
    #convert min_rating from 1-10 scale to 0-100 scale
    query = '''
    query ($year: Int, $season: MediaSeason, $genre: String, $animeFormat: MediaFormat) {
        Page(page: 1, perPage: 50) {
            media(
                season: $season,
                seasonYear: $year,
                genre: $genre,
                format: $animeFormat,
                type: ANIME,
                sort: TRENDING_DESC
            ) {
                id
                title {
                    romaji
                }
            }
        }
    }
    '''

    variables = {
        'year': year,
        'season': season.upper(),
        'format': animeFormat
    }
    if genre != "Any":
        variables['genre'] = genre
    # if min_rating > 0:
    #     variables['averageScore_gte'] = min_rating * 10
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
