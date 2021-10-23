#Spotify Documentation: https://spotipy.readthedocs.io/en/2.18.0/?highlight=oauth2#module-spotipy.oauth2
from bs4 import BeautifulSoup
import requests
import json
import spotipy                               #library to work with Spotify API
from spotipy.oauth2 import SpotifyOAuth      #Spotify Authorization

#Default variable
NUMBER_OF_SONGS = 50
SPOTIFY_CLIENT_ID = ""          #CLIENT ID
SPOTIFY_CLIENT_SECRET = ""      #CLIENT SECRET ID
SPOTIFY_REDIRECT_URI = ""                     #REDIRECT TO SPOTIFY PROFILE
SPOTIFY_USER_ID = ""                   #USED ID

file = open("token.txt", 'r')               #path f to Spotify token
token_txt = file.read()
token_dic = json.loads(token_txt)
SPOTIFY_TOKEN = token_dic['access_token']


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(         #Params for SpotifyOAuth module  -> Documentation  "oauth2 Module"
        scope="playlist-modify-private", #Create a private playlist on Spotify
        redirect_uri=SPOTIFY_REDIRECT_URI,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path=SPOTIFY_TOKEN
    )
)
user_id = sp.current_user()["id"]
date = input("From which year would you like to check music trends ? \n Type: YYYY-MM-DD: ")


response = requests.get(url= f"https://www.billboard.com/charts/hot-100/{date}")
Website = response.text
soup = BeautifulSoup(Website, "html.parser")
songs = [ songs.getText() for songs in soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")]
authors = [ author.getText() for author in soup.find_all(name="span", class_="chart-element__information__artist text--truncate color--secondary")]

spotify_songs = []
# spotify_author = []
for i in range(NUMBER_OF_SONGS):
    spotify_songs.append(songs[i])
    # spotify_author.append(authors[i])

song_uris = []
year = date.split("-")[0]                   #split YYYY-MM-DD to list of ['YYYY','MM','DD'], so we get YYYY
for song in spotify_songs:
    result_song = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result_song["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"Song: '{song}',  doesn't exist in Spotify. Skipped")

playlist = sp.user_playlist_create(user=SPOTIFY_USER_ID, name=f"{date} Billboard {NUMBER_OF_SONGS}", public=False)
sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)