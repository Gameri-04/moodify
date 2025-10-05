# To import textBlob library
from textblob import TextBlob
import random

# text = "This is amazing!"

# # creates a TextBlob object
# blob = TextBlob(text)

# # Gets the sentiment polarity i.e how positve/negative the statement is
# score = blob.sentiment.polarity

# print(f"This is the sentence: '{text}'")
# print(f"Has a polarity score of: {score}")

# def get_mood_from_score(score):
#     if score <= -0.5:
#         return "Sad"
#     elif score < 0:
#         return "Neutral" 
#     elif score <= 0.5:
#         return "Happy" 
#     else:
#         return "Excited"

def analyze_mood(score):
    if score <= -0.3:
        mood = "Sad"
        queries = ["indie sad songs", "melancholy acoustic", "emotional piano"]
        spotify_query = random.choice(queries)
    elif score < 0.2:
        mood = "Neutral"
        spotify_query = "calm lo-fi beats" 
        queries = ["lo-fi beats", "ambient study", "chill instrumental"]
        spotify_query = random.choice(queries)
    elif score < 0.6:
        mood = "Excited"
        spotify_query = "energetic music"
        queries = ["high energy dance", "workout music", "party hits"]
        spotify_query = random.choice(queries)     
    else:
        mood = "Happy"
        spotify_query = "upbeat music"  
        queries = ["upbeat pop", "happy indie", "feel good songs"]
        spotify_query = random.choice(queries)  


    return {
        "mood" : mood,
        "spotify_query" : spotify_query 
    }


# analysis = analyze_mood(0.5)
# print(analysis)

# get_mood_from_score(-0.5)


# mood = get_mood_from_score(-0.7)
# print(f"Your mood is: {mood}")
# spotify_query = print(f"{mood} music")