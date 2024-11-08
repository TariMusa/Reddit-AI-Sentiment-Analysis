import praw
import pandas as pd
from datetime import datetime
import time
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import DoubleType
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
try:
    nltk.data.find('sentiment/vader_lexicon')
    print("Vader lexicon is present.")
except LookupError:
    print("Vader lexicon is missing.")


# Replace with your own credentials
client_id = "m48FnYoOGJ4ZdDJidN1S-g"
client_secret = "7iXt6zFvYRtNYttADS2amHu188dkog"
user_agent = "AI sentiment analysis bot v1.0 by /u/Weary-Vast5850"

# Authenticate with Reddit
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

try:
    # Test by accessing a simple subreddit attribute
    print(reddit.read_only)  # Should print True if successful
except Exception as e:
    print(f"Error: {e}")

print("Rate limit:", reddit.auth.limits)

try:
    # Try to fetch top posts from the "learnprogramming" subreddit
    for submission in reddit.subreddit("learnprogramming").hot(limit=5):
        print(submission.title)
except praw.exceptions.ClientException as e:
    print(f"Client error occurred: {e}")
except praw.exceptions.APIException as e:
    print(f"API error occurred: {e}")
except praw.exceptions.PRAWException as e:
    print(f"General PRAW exception occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Choose the subreddit and fetch posts
subreddit = reddit.subreddit('artificial')
posts = []

# Collect data from top posts or all posts in the subreddit
for post in subreddit.top(limit=5000):  # Collect 5000 posts
    posts.append([post.title, post.selftext, post.score, post.num_comments, post.created_utc])

# Save data to DataFrame
df = pd.DataFrame(posts, columns=["Title", "Text", "Score", "Num_Comments", "Timestamp"])

# Convert timestamp to readable format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

# Save the collected data to CSV
df.to_csv('reddit_ai_posts.csv', index=False)



## Cleaning
def clean_text(text):
    # Remove URLs and mentions (e.g., @usernames)
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # Remove URLs
    text = re.sub(r"@\w+", "", text)  # Remove mentions
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove non-alphabetic characters
    text = text.lower()  # Convert to lowercase
    return text

# Clean the title and text columns
df['Cleaned_Title'] = df['Title'].apply(clean_text)
df['Cleaned_Text'] = df['Text'].apply(clean_text)

# Save cleaned data to CSV
df.to_csv('cleaned_reddit_ai_posts.csv', index=False)


## sentiment analysis
# Initialize SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Function to analyze sentiment
def analyze_sentiment(text):
    sentiment_score = sia.polarity_scores(text)
    return sentiment_score['compound']  # Compound score is the overall sentiment

# Apply sentiment analysis on the cleaned title and text
df['Title_Sentiment'] = df['Cleaned_Title'].apply(analyze_sentiment)
df['Text_Sentiment'] = df['Cleaned_Text'].apply(analyze_sentiment)

# Save the results with sentiment scores
df.to_csv('sentiment_analysis_results.csv', index=False)


# Plot sentiment distribution
plt.figure(figsize=(10,6))
sns.histplot(df['Title_Sentiment'], kde=True, color='blue', bins=50)
plt.title('Sentiment Distribution of Post Titles')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.show()

# Plot sentiment over time (trend)
df['Year_Month'] = df['Timestamp'].dt.to_period('M')
monthly_sentiment = df.groupby('Year_Month')['Title_Sentiment'].mean()

plt.figure(figsize=(12,6))
monthly_sentiment.plot()
plt.title('Average Sentiment Score of AI Posts by Month')
plt.xlabel('Month')
plt.ylabel('Average Sentiment Score')
plt.show()


## Hadoop
# Initialize Spark session
spark = SparkSession.builder.appName("RedditSentimentAnalysis").getOrCreate()

# Load data from HDFS
df = spark.read.csv("hdfs:///user/hadoop/reddit_data/reddit_ai_posts.csv", header=True, inferSchema=True)

# UDF for sentiment analysis
def sentiment_udf(text):
    return analyze_sentiment(text)

# Register the UDF with Spark
sentiment_udf_spark = udf(sentiment_udf, DoubleType())
df = df.withColumn("Title_Sentiment", sentiment_udf_spark(df['Title']))

# Perform further transformations or save results
df.write.csv("hdfs:///user/hadoop/reddit_data/sentiment_results.csv")