# To import textBlob library
from textblob import TextBlob

# this is my test sentence
test_sentence = "This is amazing!"

# creates a TextBlob object
blob = TextBlob(test_sentence)

# Gets the sentiment polarity i.e how positve/negative the statement is
polarity = blob.sentiment.polarity

print(f"This is the sentence: '{test_sentence}'")
print(f"Has a polarity score of: {polarity}")

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
    if score <= -0.5:
        mood = "Sad"
        spotify_query = "sad acoustic songs"
    elif score < 0:
        mood = "Neutral"
        spotify_query = "calm lo-fi beats" 
    elif score < 0.5:
        mood = "Happy"
        spotify_query = "upbeat music"  
    else:
        mood = "Excited"
        spotify_query = "energetic music"

    return {
        "mood" : mood,
        "spotify_query" : spotify_query 
    }


analysis = analyze_mood(0.5)
print(analysis)

# get_mood_from_score(-0.5)


# mood = get_mood_from_score(-0.7)
# print(f"Your mood is: {mood}")
# spotify_query = print(f"{mood} music")