Reddit Sentiment Analysis with PRAW, NLTK, and PySpark
This project collects Reddit posts, cleans the text, performs sentiment analysis, and visualizes sentiment trends over time. It uses Python packages such as PRAW (for accessing Reddit’s API), NLTK's VADER (for sentiment analysis), Pandas (for data manipulation), and PySpark (for processing and analyzing data with Apache Spark).

Project Overview
The project connects to Reddit via the PRAW API to collect data from a specific subreddit. It then:

Cleans the text to remove unnecessary characters.
Conducts sentiment analysis using the NLTK VADER lexicon.
Visualizes the distribution and trends of sentiment over time.
Uses Apache Spark for data processing in a distributed environment, making it scalable for large datasets.
Requirements
To run this project, you will need:

Python 3.x
Pandas for data manipulation
PRAW to interact with Reddit’s API
NLTK with the VADER lexicon for sentiment analysis
Matplotlib and Seaborn for data visualization
PySpark for distributed data processing
Install the necessary packages:

bash
Copy code
pip install praw pandas nltk matplotlib seaborn pyspark
Setup
PRAW Authentication
Replace the client_id, client_secret, and user_agent in the code with your Reddit API credentials.

NLTK VADER Lexicon
Ensure the VADER lexicon is downloaded by adding:

python
Copy code
import nltk
nltk.download('vader_lexicon')
Data Collection
The project gathers posts from the specified subreddit (artificial), extracting key information (title, text, score, comments, timestamp). The data is stored in a Pandas DataFrame and saved as a CSV file.

Data Cleaning
Text is cleaned to remove URLs, mentions, and non-alphabetic characters. The cleaned data is stored in a CSV file (cleaned_reddit_ai_posts.csv).

Sentiment Analysis
Using NLTK's VADER SentimentIntensityAnalyzer, sentiment analysis is performed on the cleaned text, producing a compound sentiment score for each post title and text. Results are saved to sentiment_analysis_results.csv.

Data Visualization
Sentiment Distribution
A histogram shows the distribution of sentiment scores across post titles.

Sentiment Trend Over Time
A line plot displays the average monthly sentiment score over time, helping to identify trends.

Apache Spark Integration
For scalability, this project can process the data on Hadoop's HDFS:

Data is loaded into a Spark DataFrame, where sentiment analysis is applied using a Spark UDF.
The results can be saved back to HDFS in CSV format.
Usage
To run the project, execute SentimentAnalysis.py in your Python environment.

bash
Copy code
python SentimentAnalysis.py
Ensure that the Hadoop environment is set up if using HDFS with PySpark.

Files
reddit_ai_posts.csv: Raw Reddit data collected from the subreddit.
cleaned_reddit_ai_posts.csv: Data after cleaning.
sentiment_analysis_results.csv: Data with sentiment scores.
SentimentAnalysis.py: Main script for data collection, cleaning, sentiment analysis, and visualization.
License
This project is licensed under the MIT License.

