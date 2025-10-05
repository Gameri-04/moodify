from textblob import TextBlob
from mood_analyzer import analyze_mood

def analyze_text_sentiment(user_text):
    blob = TextBlob(user_text) # creates TextBlob object
    score = blob.sentiment.polarity # gets polarity of statement
    subjectivity = blob.sentiment.subjectivity

    result = analyze_mood(score) # stores output in result 
    # print(f"DEBUG: Text '{user_text}' → Score: {score}")
    if subjectivity < 0.4:
        return {
            "mood": "Neutral",
            "spotify_query": "calm lo-fi study beats"
        }
    
    return result 
   



print(analyze_text_sentiment("I am so happy today!"))
print(analyze_text_sentiment("This is terrible"))
print(analyze_text_sentiment("I feel okay"))
