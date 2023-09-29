import json
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
import boto3 #it is used to programatically communicate with aws services
from datetime import datetime

def lambda_handler(event, context):
    
    client_id = os.environ.get("client_id")
    client_secret = os.environ.get("client_secret")
    
    client_credentials_manager = SpotifyClientCredentials(client_id =client_id, client_secret = client_secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    #playlist = sp.user_playlists('spotify')
    
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
    playlist_uri = playlist_link.split("/") [-1].split("?")[0]
    spotify_data = sp.playlist_tracks(playlist_uri)
    
    client = boto3.client("s3")
    filename = "spotify_raw_" + str(datetime.now()) + ".json"
    
    client.put_object(
        Bucket="spotify-etl-project-nasir",
        Key="raw_data/BeforeProcessed/" + filename,
        Body=json.dumps(spotify_data) 
        )
