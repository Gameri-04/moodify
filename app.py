from flask import Flask, request, render_template_string
from text_analyzer import analyze_text_sentiment 
from spotify_client import search_spotify_tracks, get_spotify_token


SPOTIFY_CLIENT_ID = "03f71a757307402d8c883ff0cdf6c1a4"
SPOTIFY_CLIENT_SECRET = "d8f061f6823841a484e98af1affa4365"


HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
    <title>Moodify</title>
    <style>
    body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    margin: 0;
    padding: 0;
    min-height: 100vh;
}

.container {
    max-width: 600px;
    margin: auto auto;
    padding: 30px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

h1 {
    font-size: 30px;
    color: #333;
    text-align: center;
    font-family: "Roboto", sans-serif;

}

.h1 {}

textarea {
    text-align: center;
    padding: 15px 0 0 0;
    margin 0 auto;
    border: 2px solid #ddd;
    outline: none;
    border-radius: 8px;
    font-size: 16px;
    resize: none;
    background: #eee;

}

textarea::focus {
    outline: none;
    border: none;
}

.area {
    text-align: center;
    margin: 0 auto;
    display: block;
}

button {
    background: #667eea;
    color: white;
    padding: 12px 30px;
    top: -15px;
    position: relative;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
}

button::placeholder {
    margin: 0 auto;
}

.button {
    margin: 0 auto;
    text-align: center;
    display: block;
}

    </style>
</head>
<body>
    <div class="container">
        <h1 class="h1">How are you feeling today?</h1>
        <form method="POST">
            <textarea name="user_text" rows="2" cols="40" class="area"></textarea>
            <br>
            <div class="button">
                <button type="submit">Analyze My Mood</button>
            </div>
        </form>
    </div>
</body>
</html>
'''

RESULTS_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Moodify - Results</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 600px;
            margin: 20px auto;
            padding: 30px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }

        .mood-form {
            margin-bottom: 30px;
        }

        textarea {
            width: 80%;
            margin: 0 auto;
            padding: 15px 0 0 0;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            resize: none;
            background-color: eee;
            font-family: inherit;
        }

        .area {
            text-align: center;
            margin: 0 auto;
            display: block;
        }

        button {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        /* Results Section */
        .results-container {
            animation: fadeIn 0.6s ease;
            margin-top: 30px;
            padding: 25px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 10px;
            border-left: 5px solid;
        }

        /* Different border colors for each mood */
        .results-sad { border-left-color: #6c757d; }
        .results-neutral { border-left-color: #17a2b8; }
        .results-happy { border-left-color: #28a745; }
        .results-excited { border-left-color: #ff6b6b; }

        .mood-header {
            font-size: 24px;
            margin-bottom: 15px;
            color: #333;
        }

        .song-list {
            margin-top: 20px;
        }

        .song-item {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        @keyframes fadeIn {
            from { 
                opacity: 0; 
                transform: translateY(20px); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0); 
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎵 Moodify - Music for Your Mood</h1>
        
        <div class="mood-form">
            <form method="POST">
                <textarea name="user_text" rows="2" cols="10" placeholder="How are you feeling today?" class="area">{{ user_text }}</textarea>
                <br><br>
                <button type="submit">Analyze My Mood 🎶</button>
            </form>
        </div>

        <div class="results-container results-{{ result.mood.lower() }}">
            <h2 class="mood-header">Detected Mood: {{ result.mood }} 
                {% if result.mood == "Sad" %}😢
                {% elif result.mood == "Neutral" %}😐
                {% elif result.mood == "Happy" %}😊
                {% else %}🎉
                {% endif %}
            </h2>
            
            <p><strong>Your text:</strong> "{{ user_text }}"</p>
            
            <p><strong>Music Recommendation:</strong> "{{ result.spotify_query }}"</p>
            
            {% if songs %}
            <div class="song-list">
                <h3>🎵 Recommended Songs:</h3>
                {% for song in songs %}
                <div class="song-item">
                    <strong>{{ song.name }}</strong> by {{ song.artist }}
                </div>
                {% endfor %}
            </div>
            {% else %}
            <p>No songs found or Spotify connection failed.</p>
            {% endif %}
            
            <br>
            <p><small>Want to try another mood? Just type above and click Analyze! 🔄</small></p>
        </div>
    </div>
</body>
</html>
'''

# Create a Flask app
app = Flask(__name__)

# This defines what happens when someone goes to the homepage ("/")
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_text = request.form['user_text']
        result = analyze_text_sentiment(user_text) # Analyze mood
        token = get_spotify_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
#  Get Spotify token

        if token:
            songs = search_spotify_tracks(result['spotify_query'], token)
        else:
            songs = []  # Fallback if Spotify fails
        
        # Step 4: Show results with real songs
        return render_template_string(RESULTS_TEMPLATE, 
                                   result=result, 
                                   songs=songs, 
                                   user_text=user_text)

        # return f"Your mood is: {result['mood']}. We'll search for: {result['spotify_query']}"
    else:
        return HTML_TEMPLATE 
    

# This runs the app when we execute the script
if __name__ == '__main__':
    app.run(debug=True)