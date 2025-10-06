import requests
import base64
import random

def get_spotify_token(client_id, client_secret):
        credentials = f"{client_id}:{client_secret}"
        credential_bytes = credentials.encode("utf-8")
        encoded_bytes = base64.b64encode(credential_bytes)
        encoded_credentials = encoded_bytes.decode("utf-8")
        # return encoded_credentials

        url = "https://accounts.spotify.com/api/token"
        headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {'grant_type': 'client_credentials'}

        response = requests.post(url=url, headers=headers, data=data)

        if response.status_code == 200:
                token_data = response.json()
                access_token = token_data['access_token']
                return access_token

        else:
                print("Something went wrong")
                return None


def search_spotify_tracks(query, access_token):
        url = "https://api.spotify.com/v1/search"
        headers = {
                'Authorization': f'Bearer {access_token}'
        }

        params = {
                'q' : query,
                'type' : 'track',
                'limit' : 20
        }

        response = requests.get(url=url, headers=headers, params=params)

        if response.status_code == 200:
                data = response.json()
                tracks = data['tracks']['items']

                random.shuffle(tracks)

                tracks = tracks[:10]


                songs = []
                for track in tracks:
                        song_info = {
                        "name" : track['name'],
                        "artist": track['artists'][0]['name'],
                        "link" : track['external_urls']['spotify'],
                        "preview_url": track['preview_url'],
                        "image" : track['album']['images'][0]['url'] if track['album']['images'] else None
                        }
                        songs.append(song_info)

                return songs
        else:
                print(f"Search failed: {response.status_code}")
                return []

# client_id = "03f71a757307402d8c883ff0cdf6c1a4"
# client_secret = "d8f061f6823841a484e98af1affa4365" 

# token = (get_spotify_token(client_id, client_secret))
# print(f"Access token: {token}")
# if token:
#     print(f"Access token: {token}")
#     songs = search_spotify_tracks("happy pop music", token)
#     for song in songs:
#         print(f"🎵 {song['name']} by {song['artist']}")
# else:
#     print("Failed to get token")