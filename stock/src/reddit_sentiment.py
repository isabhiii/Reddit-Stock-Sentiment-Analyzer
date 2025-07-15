import praw
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv
from textblob import TextBlob
import re

load_dotenv()

class RedditSentimentAnalyzer:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        self.subreddits = 'stocks+investing+wallstreetbets+pennystocks+cryptostreetbets+options+investing+SecurityAnalysis+StockMarket'
        self.time_filters = {
            'hour': 'hour',
            'day': 'day',
            'week': 'week',
            'month': 'month',
            'year': 'year',
            'all': 'all'
        }

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove Reddit-style links
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        # Remove special characters and digits
        text = re.sub(r'[^\w\s]', '', text)
        return text.strip()

    def get_sentiment_score(self, text):
        cleaned_text = self.clean_text(text)
        if not cleaned_text:
            return 0
        
        analysis = TextBlob(cleaned_text)
        return analysis.sentiment.polarity

    def get_reddit_posts(self, stock_symbol, limit=100, time_filter='month', max_comments=10):
        posts = []
        try:
            # Validate time filter
            if time_filter not in self.time_filters:
                time_filter = 'month'  # Default to month if invalid

            for post in self.reddit.subreddit(self.subreddits).search(
                f'{stock_symbol} stock', limit=limit, time_filter=time_filter
            ):
                # Get post comments
                post.comments.replace_more(limit=0)  # Flatten comment tree
                comments = []
                for comment in post.comments.list()[:max_comments]:
                    comment_sentiment = self.get_sentiment_score(comment.body)
                    comments.append({
                        'text': comment.body,
                        'score': comment.score,
                        'sentiment': comment_sentiment,
                        'created_utc': datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                    })
                
                # Combine text for overall sentiment
                full_text = f"{post.title} {post.selftext} " + " ".join([c['text'] for c in comments])
                sentiment_score = self.get_sentiment_score(full_text)
                
                posts.append({
                    'title': post.title,
                    'text': post.selftext,
                    'comments': comments,
                    'score': post.score,
                    'sentiment': sentiment_score,
                    'comment_count': len(comments),
                    'created_utc': datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    'url': f'https://reddit.com{post.permalink}',
                    'subreddit': post.subreddit.display_name
                })
        except Exception as e:
            print(f"Error fetching Reddit posts: {str(e)}")
        return pd.DataFrame(posts)

    def analyze_sentiment(self, stock_symbol, time_filter='month', limit=100, max_comments=10):
        posts_df = self.get_reddit_posts(stock_symbol, limit, time_filter, max_comments)
        
        if len(posts_df) == 0:
            return {
                'success': False,
                'error': f'No Reddit posts found for {stock_symbol}'
            }
        
        avg_sentiment = posts_df['sentiment'].mean()
        
        posts_df['sentiment_category'] = posts_df['sentiment'].apply(
            lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral')
        )
        
        sentiment_counts = posts_df['sentiment_category'].value_counts().to_dict()
        
        # Calculate average comment sentiment
        comment_sentiments = []
        for comments in posts_df['comments']:
            if isinstance(comments, list):
                comment_sentiments.extend([c['sentiment'] for c in comments])
        
        avg_comment_sentiment = sum(comment_sentiments) / len(comment_sentiments) if comment_sentiments else 0
        
        top_posts = posts_df.nlargest(5, 'score').to_dict('records')
        
        return {
            'success': True,
            'average_sentiment': float(avg_sentiment),
            'average_comment_sentiment': float(avg_comment_sentiment),
            'post_count': len(posts_df),
            'total_comments_analyzed': len(comment_sentiments),
            'sentiment_distribution': sentiment_counts,
            'top_posts': top_posts,
            'time_period': time_filter
        }