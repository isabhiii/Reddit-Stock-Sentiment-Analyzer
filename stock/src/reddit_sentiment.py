import asyncpraw
import aiohttp
import asyncio
from textblob import TextBlob
import pandas as pd
import os
from datetime import datetime
import ssl
import certifi

class RedditSentimentAnalyzer:
    def __init__(self):
        self.reddit = asyncpraw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
    
    def analyze_sentiment(self, stock_symbol, time_filter='week', limit=30, max_comments=5):
        # This is the synchronous wrapper for the async method
        try:
            # Create a new event loop for this request
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run the async method in the event loop
            result = loop.run_until_complete(self._analyze_sentiment_async(
                stock_symbol, time_filter, limit, max_comments
            ))
            return result
        finally:
            # Clean up resources
            loop.close()
    
    async def _analyze_sentiment_async(self, stock_symbol, time_filter='week', limit=30, max_comments=5):
        posts = []
        post_data = []
        
        # Get posts
        query = f"{stock_symbol} stock"
        subreddits = ["stocks", "investing", "wallstreetbets", "pennystocks", "cryptostreetbets"]
        
        try:
            # Create SSL context with certifi's certificates
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            
            # Configure client session with SSL context
            conn = aiohttp.TCPConnector(
                ssl=ssl_context,
                verify_ssl=True
            )
            
            # Create a proper async session with timeout and SSL configuration
            timeout = aiohttp.ClientTimeout(total=30)  # 30 seconds timeout
            async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
                # Set the session for Reddit
                self.reddit._core._requestor._http = session
                
                # Get subreddit and search
                subreddit = await self.reddit.subreddit("+".join(subreddits))
                async for submission in subreddit.search(query, sort="relevance", time_filter=time_filter, limit=limit):
                    posts.append(submission)
                
                # Process posts and comments
                if posts:
                    tasks = [self.process_post(post, max_comments) for post in posts]
                    post_results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    for data in post_results:
                        if data and not isinstance(data, Exception):
                            post_data.append(data)
        except Exception as e:
            print(f"Error in Reddit API: {str(e)}")
            return {
                'success': False,
                'error': f'Error with request: {str(e)}',
                'average_sentiment': 0,
                'post_count': 0,
                'sentiment_distribution': {'positive': 0, 'neutral': 0, 'negative': 0},
                'top_posts': [],
                'time_period': time_filter
            }
        
        # Convert to DataFrame for analysis
        if not post_data:
            return {
                'success': False,
                'error': 'No posts found',
                'average_sentiment': 0,
                'post_count': 0,
                'sentiment_distribution': {'positive': 0, 'neutral': 0, 'negative': 0},
                'top_posts': [],
                'time_period': time_filter
            }
            
        posts_df = pd.DataFrame(post_data)
        
        # Calculate sentiment categories
        posts_df['sentiment_category'] = posts_df['sentiment'].apply(
            lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'neutral')
        )
        
        sentiment_counts = posts_df['sentiment_category'].value_counts().to_dict()
        for category in ['positive', 'neutral', 'negative']:
            if category not in sentiment_counts:
                sentiment_counts[category] = 0
        
        # Calculate average sentiment
        avg_sentiment = posts_df['sentiment'].mean()
        
        # Get top posts
        top_posts = posts_df.nlargest(5, 'score').to_dict('records')
        
        return {
            'success': True,
            'average_sentiment': float(avg_sentiment),
            'post_count': len(posts_df),
            'sentiment_distribution': sentiment_counts,
            'top_posts': top_posts,
            'time_period': time_filter
        }
    
    async def process_post(self, submission, max_comments):
        try:
            # Load submission content
            submission_text = submission.selftext if submission.selftext else submission.title
            submission_sentiment = TextBlob(submission_text).sentiment.polarity
            
            # Get comments - Add defensive checks
            try:
                await submission.comments.replace_more(limit=0)
                comments_list = await submission.comments.list()
            except Exception as comment_error:
                print(f"Error getting comments list: {str(comment_error)}")
                comments_list = []
                
            # Safely get comments up to max_comments
            comments = comments_list[:max_comments] if comments_list else []
            
            comment_data = []
            for comment in comments:
                try:
                    comment_text = comment.body
                    comment_sentiment = TextBlob(comment_text).sentiment.polarity
                    comment_data.append({
                        'text': comment_text,
                        'sentiment': comment_sentiment
                    })
                except Exception as comment_error:
                    print(f"Error processing comment: {str(comment_error)}")
                    continue
            
            # Calculate overall sentiment (post + comments)
            all_sentiments = [submission_sentiment] + [c['sentiment'] for c in comment_data]
            overall_sentiment = sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0
            
            return {
                "title": submission.title,
                "text": submission_text,
                "comments": comment_data,
                "score": submission.score,
                "sentiment": overall_sentiment,
                "comment_count": len(comment_data),
                "created_utc": datetime.fromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                "url": f'https://reddit.com{submission.permalink}',
                "subreddit": submission.subreddit.display_name
            }
        except Exception as e:
            print(f"Error processing submission: {str(e)}")
            return None