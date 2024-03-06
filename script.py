import requests


def fetch_trending_anime(year, season, genre, animeFormat):
    url = "https://graphql.anilist.co"
    query = """
    query ($year: Int, $season: MediaSeason, $genre: String, $format: MediaFormat) {
        Page(page: 1, perPage: 50) {
            media(
                season: $season,
                seasonYear: $year,
                genre: $genre,
                format: $format,
                type: ANIME,
                sort: TRENDING_DESC
            ) {
                id
                title {
                    romaji
                }
                coverImage{
                    large
                }
                siteUrl
            }
        }
    }
    """

    variables = {}
    if year != "Any":
        variables["year"] = int(year)
    if season != "Any":
        variables["season"] = season.upper()
    if genre != "Any":
        variables["genre"] = genre
    if animeFormat != "Any":
        variables["format"] = animeFormat

    try:
        response = requests.post(url, json={"query": query, "variables": variables})
        data = response.json()
        if (
            data
            and "data" in data
            and "Page" in data["data"]
            and "media" in data["data"]["Page"]
        ):
            return [
                {
                    "title": anime["title"]["romaji"],
                    "coverImage": anime["coverImage"]["large"],
                    "anilistUrl": anime["siteUrl"],
                }
                for anime in data["data"]["Page"]["media"]
            ]
        else:
            print("Data is not in the expected format or is missing.")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
